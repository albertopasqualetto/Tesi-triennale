from enum import Enum
import os
import tempfile
from uuid import uuid4

import numpy as np
import ffmpeg
import scipy

from mpai_cae_arp.audio import AudioWave, Noise
from mpai_cae_arp.files import File, FileType
from mpai_cae_arp.types.irregularity import Irregularity, IrregularityFile, Source
from mpai_cae_arp.time import frames_to_seconds, seconds_to_frames, seconds_to_string, time_to_seconds

TMP_FOLDER = os.path.join(tempfile.gettempdir(), "mpai")
os.makedirs(TMP_FOLDER, exist_ok=True)
TMP_CHANNELS_MAP = os.path.join(TMP_FOLDER, "channels_map.json")


def calculate_offset(audio: AudioWave, video: AudioWave, interval: int = 10) -> int:
    """
    Calculates the offset between two audio files based on their cross-correlation.
    Since the cross-correlation is a computationally expensive operation, the audio files are resampled to 1/4 of their original sampling rate.
    In addition to that, only the specified time interval (starting at 15 seconds) is used for the cross-correlation,
    assuming that after that time the audio and video contain portions of the same content.

    Parameters
    ----------
    audio : AudioWave
        The audio file to be used as reference.
    video : AudioWave
        The audio file to be used as target.
    interval : int, optional
        The interval in seconds to be used for the cross-correlation, by default 10

    Returns
    -------
    int
        The offset in milliseconds.
    """
    audio = audio.get_channel(0)[(audio.samplerate*15):(audio.samplerate*(15+interval))]
    video = video.get_channel(0)[(video.samplerate*15):(video.samplerate*(15+interval))]

    resampled_audio = audio.array[::4]
    resampled_video = video.array[::4]

    corr = scipy.signal.correlate(resampled_audio, resampled_video, mode="full", method="auto") # TODO should fastpath to faster numpy.convolve for 1d inputs when possible
    offset = np.argmax(corr) - len(resampled_audio)
    offset_ms = offset / (audio.samplerate / 4) * 1000

    return round(offset_ms)


class BitDepth(Enum):
    PCM_S8 = "pcm_s8"
    PCM_S16LE = "pcm_s16le"
    PCM_S24LE = "pcm_s24le"
    PCM_S32LE = "pcm_s32le"


def get_audio_from_video(video_src: str, samplerate: int, bit_depth: BitDepth) -> AudioWave:
    """
    Extracts the audio from a video file and returns it as an AudioWave object.
    
    Parameters
    ----------
    video_src : str
        The path to the video file.
    samplerate : int
        The sampling rate of the audio output.
    bit_depth : BitDepth
        The bit depth of the audio output.
        
    Returns
    -------
    AudioWave
        The extracted audio. The number of channels is always 2. The audio is saved as a temporary file.
    """

    # ffmpeg -i video.mov -acodec pcm_s16le -ac 2 audio.wav
    extracted_audio_path = os.path.join(TMP_FOLDER, 'audio.wav')
    
    in_file = ffmpeg.input(video_src)
    out_file = ffmpeg.output(in_file.audio, extracted_audio_path, ac=2, ar=samplerate, acodec=bit_depth.value)
    ffmpeg.run(out_file, quiet=True, overwrite_output=True)

    rate, data = scipy.io.wavfile.read(extracted_audio_path)

    return AudioWave(data, 24, 2, rate)


def get_irregularities_from_audio(audio_src: AudioWave) -> list[Irregularity]:
    input_channels: list[AudioWave] = []

    if audio_src.channels > 1:
        for channel in range(audio_src.channels):
            input_channels.append(audio_src.get_channel(channel))
    else:
        input_channels.append(audio_src)

    channels_map = {}

    irreg_list: list[Irregularity] = []
    for idx, audio in enumerate(input_channels):
        for _, noise_list in audio.get_silence_slices([
            Noise("A", -50, -63),
            Noise("B", -63, -69),
            Noise("C", -69, -72)],
                length=500).items():
            for start, _ in noise_list:
                id = uuid4()
                irreg_list.append(
                    Irregularity(
                        id=id,
                        source=Source.AUDIO,
                        time_label=seconds_to_string(frames_to_seconds(start, audio.samplerate))
                    )
                )
                channels_map[str(id)] = idx

    File(path=TMP_CHANNELS_MAP, format=FileType.JSON).write_content(channels_map)

    return irreg_list


def create_irreg_file(audio_src: str, video_src: str) -> IrregularityFile:

    audio = AudioWave.from_file(audio_src, bufferize=True)
    video = get_audio_from_video(video_src, audio.samplerate, BitDepth.PCM_S24LE)

    offset = calculate_offset(audio, video)
    irregularities = get_irregularities_from_audio(audio)

    irregularities.sort(key=lambda x: time_to_seconds(x.time_label))
    
    return IrregularityFile(irregularities=irregularities, offset=offset)


def merge_irreg_files(
    file1: IrregularityFile,
    file2: IrregularityFile
) -> IrregularityFile:
    """ 
    Merge two IrregularityFiles into one. The offset of the new file is the maximum of the two offsets.
    """

    match file1.offset, file2.offset:
        case None, None:
            offset = 0
        case None, _:
            offset = file2.offset
        case _, None:
            offset = file1.offset
        case _, _:
            offset = max(file1.offset, file2.offset)

    irregularities = file1.irregularities + file2.irregularities
    irregularities.sort(key=lambda x: time_to_seconds(x.time_label))

    new_file = IrregularityFile(
        irregularities=irregularities, offset=offset)

    return new_file


def extract_audio_irregularities(
    audio_src: str | AudioWave,
    irreg_file: IrregularityFile,
    path: str
) -> IrregularityFile:

    if isinstance(audio_src, AudioWave):
        audio = audio_src
    elif os.path.exists(audio_src):
        audio = AudioWave.from_file(audio_src, bufferize=True)
    else:
        raise ValueError("Invalid audio source")

    channels_map = File(path=TMP_CHANNELS_MAP, format=FileType.JSON).get_content()
    os.makedirs(f"{path}/AudioBlocks", exist_ok=True)

    for irreg in irreg_file.irregularities:
        if channels_map.get(str(irreg.id)) is None:
            audio[seconds_to_frames(
                        time_to_seconds(irreg.time_label), audio.samplerate
                    ):seconds_to_frames(
                        time_to_seconds(irreg.time_label), audio.samplerate)+audio.samplerate//2]\
                .save(f"{path}/AudioBlocks/{irreg.id}.wav")
        else:
            audio.get_channel(channels_map[str(irreg.id)])[
                    seconds_to_frames(
                        time_to_seconds(irreg.time_label), audio.samplerate
                    ):seconds_to_frames(
                        time_to_seconds(irreg.time_label), audio.samplerate)+audio.samplerate//2]\
                .save(f"{path}/AudioBlocks/{irreg.id}.wav")
        irreg.audio_block_URI = f"{path}/AudioBlocks/{irreg.id}.wav"   # 500 ms of audio
    os.remove(TMP_CHANNELS_MAP)

    return irreg_file
