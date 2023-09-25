import tempfile
import pytest
import numpy as np

from mpai_cae_arp.audio.utils import Criterion
from mpai_cae_arp.audio import AudioWave, Noise


class TestNoise:

    noise = Noise('test', 0, 0)

    def test_init(self):
        assert self.noise.label == 'test'
        assert self.noise.db_range == 0
        assert self.noise.db_max == 0
        assert self.noise.db_min == 0

        with pytest.raises(ValueError):
            Noise('test', -20, -10)

    def test_equality(self):
        a = Noise('A', -10, -20)
        b = Noise('B', -20, -30)
        c = Noise('C', -15, -16)
        assert a > b
        assert b < c

        with pytest.raises(TypeError):
            assert a < "test"

    def test_positive_db_limits(self):
        with pytest.raises(ValueError):
            Noise('test', 10, 5)


class TestAudioWave:

    data = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    wave = AudioWave(data, 16, 2, 44100)

    def test_init(self):
        assert self.wave.bit == 16
        assert self.wave.channels == 2
        assert self.wave.samplerate == 44100
        assert np.array_equal(self.wave.array, self.data) is True

    def test_init_from_file(self):
        audio = AudioWave.from_file('tests/test_sound/test.wav')
        assert audio.bit == 16
        assert audio.channels == 1
        assert audio.samplerate == 44100

        audio = AudioWave.from_file('tests/test_sound/test.wav', bufferize=True)
        assert audio.bit == 16
        assert audio.channels == 1
        assert audio.samplerate == 44100

        with pytest.raises(FileNotFoundError):
            AudioWave.from_file('tests/test_sound/test_wrong.wav')

    def test_bufferize(self):
        for chunk in AudioWave.buffer_generator_from_file('tests/test_sound/test.wav',
                                                          1024):
            assert isinstance(chunk, AudioWave)
            assert chunk.bit == 16
            assert chunk.channels == 1
            assert chunk.samplerate == 44100

    def test_read_metadata(self):
        bit, channels, samplerate = AudioWave.read_file_metadata(
            'tests/test_sound/test.wav')
        assert bit == 16
        assert channels == 1
        assert samplerate == 44100

    def test_len(self):
        assert len(self.wave) == 4

    def test_eq(self):
        assert self.wave == self.wave
        assert self.wave != AudioWave(np.array([1, 2, 3, 4]), 16, 2, 44100)
        with pytest.raises(TypeError):
            assert self.wave == 1

    def test_iter(self):
        for val in self.wave:
            assert isinstance(val, np.ndarray)
            assert len(val) == 2

    def test_getitem(self):
        assert isinstance(self.wave[0], AudioWave)
        assert len(self.wave[0]) == 2
        assert np.array_equal(self.wave[0], np.array([1, 2])) is True

    def test_duration(self):
        assert self.wave.duration() == 4 / 44100

    def test_rms(self):
        assert self.wave.rms() == np.array([np.sqrt(21), np.sqrt(30)]).max()
        assert self.wave.rms(Criterion.mean) == np.array([np.sqrt(21),
                                                          np.sqrt(30)]).mean()
        with pytest.raises(ValueError):
            self.wave.rms(Criterion.min)

    def test_db_rms(self):
        assert self.wave.db_rms() <= -72
        assert self.wave[0:1].db_rms() <= -72

    def test_get_raw(self):
        assert isinstance(self.wave.get_raw(), bytes)

    def test_get_channel(self):
        assert isinstance(self.wave.get_channel(0), AudioWave)
        assert np.array_equal(self.wave.get_channel(0).array, np.array([1, 3, 5, 7
                                                                        ])) is True

        with pytest.raises(IndexError):
            self.wave.get_channel(-1)
        with pytest.raises(IndexError):
            self.wave.get_channel(2)

    def test_save(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.wave.save(f'{tmpdirname}/test.wav')
            audio = AudioWave.from_file(f'{tmpdirname}/test.wav')
            assert audio == self.wave

        with pytest.raises(ValueError):
            self.wave.save('test/test.t')

    def test_get_silence(self):
        noise_list = [Noise("test", 0, -20)]
        slices = self.wave.get_silence_slices(noise_list, length=50)
        assert isinstance(slices, dict)
        for val in slices.values():
            assert val == []

        array = np.array([10000 for _ in range(16000)])
        audio = AudioWave(array, 16, 1, 16000)
        assert audio.get_silence_slices(noise_list, length=500) == {
            'test': [(0, 8000), (8000, 16000)]
        }
        assert audio.get_silence_slices([], 50) == {}

        with pytest.raises(ValueError):
            self.wave.get_silence_slices([], length=1.5)
        with pytest.raises(ValueError):
            self.wave.get_silence_slices([], length=0)
