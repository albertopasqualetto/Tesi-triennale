# Packager

## Description
Implements the Technical Specification of [MPAI CAE-ARP](https://mpai.community/standards/mpai-cae/about-mpai-cae/#Figure2) *Packager* AIM, providing:
* Access Copy Files:
  1. Restored Audio Files;
  2. Editing List;
  3. Set of Irregularity Images in a .zip file;
  4. Irregularity File.
* Preservation Master Files:
  1. Preservation Audio File;
  2. Preservation Audio-Visual File where the audio has been replaced with the Audio of the Preservation Audio File
     fully synchronised with the video;
  3. Set of Irregularity Images in a .zip file;
  4. Irregularity File.

## Getting started
The *Packager* is written in Python 3.10 which is therefore required to run the program.

## Installation
[PyYaml](https://pyyaml.org) is required for reading the configuration file. You can install it with:
```
pip install pyyaml
```
[FFmpeg](https://www.ffmpeg.org/) is required for audio and video manipulation. You can install it from the official website or with a package manager.

## Usage
Once the libraries are installed, you should customise the configuration file `config.yaml`.
There are two required parameters:
1. `WORKING_PATH` that specifies the working path where all input files are stored and where all output files will be saved;
2. `PRESERVATION_FILES_NAME` that specifies the name of the preservation files to be considered.

To execute the script without issues, the inner structure of the `WORKING_PATH` directory shall be like:
```
.
├── AccessCopyFiles
│   └── ...
├── PreservationAudioFile
│   ├── File1.wav
│   ├── File2.wav
│   └── ...
├── PreservationAudioVisualFile
│   ├── File1.mp4
│   ├── File2.mp4
│   └── ...
├── PreservationMasterFiles
│   └── ...
└── temp
    ├── File1
    │   ├── AudioAnalyser_IrregullarityFileOutput1.json
    │   ├── AudioAnalyser_IrregullarityFileOutput2.json
    │   ├── AudioBlocks
    │   │   ├── AudioBlock1.jpg
    │   │   ├── AudioBlock2.jpg
    │   │   └── ...
    │   ├── EditingList.json
    │   ├── IrregularityImages
    │   │   ├── IrregularityImage1.jpg
    │   │   ├── IrregularityImage2.jpg
    │   │   └── ...
    │   ├── RestoredAudioFiles
    │   │   ├── RestoredAudioFile1.wav
    │   │   ├── RestoredAudioFile2.wav
    │   │   └── ...
    │   ├── TapeIrregularityClassifier_IrregularityFileOutput1.json
    │   ├── TapeIrregularityClassifier_IrregularityFileOutput2.json
    │   ├── VideoAnalyser_IrregularityFileOutput1.json
    │   └── VideoAnalyser_IrregularityFileOutput2.json
    ├── File2
    │   ├── AudioAnalyser_IrregullarityFileOutput1.json
    │   ├── AudioAnalyser_IrregullarityFileOutput2.json
    │   ├── AudioBlocks
    │   │   ├── AudioBlock1.jpg
    │   │   ├── AudioBlock2.jpg
    │   │   └── ...
    │   ├── EditingList.json
    │   ├── IrregularityImages
    │   │   ├── IrregularityImage1.jpg
    │   │   ├── IrregularityImage2.jpg
    │   │   └── ...
    │   ├── RestoredAudioFiles
    │   │   ├── RestoredAudioFile1.wav
    │   │   ├── RestoredAudioFile2.wav
    │   │   └── ...
    │   ├── TapeIrregularityClassifier_IrregularityFileOutput1.json
    │   ├── TapeIrregularityClassifier_IrregularityFileOutput2.json
    │   ├── VideoAnalyser_IrregularityFileOutput1.json
    │   └── VideoAnalyser_IrregularityFileOutput2.json
    └── ...
```
`PreservationAudioFile` and `PreservationAudioVisualFile` directories contain the input of ARP Workflow, while `AccessCopyFiles` and `PreservationMasterFiles` directories contain its output. `temp` directory is used to store all files exchanged between the AIMs within the Workflow.

Please note that:
* Corresponding input files shall present the same name;
* The name of Irregularity Files given above is ***mandatory***;
* The name of files within `AudioBlocks`, `IrregularityImages` and `RestoredAudioFiles` directories is not relevant to the *Packager*;
* The *Packager* will create directories named as the input files (e.g.: with input files `File1.wav` and `File1.mov`, output files will be contained in `AccessCopyFiles/File1/` and `PreservationMasterFiles/File1/`).

With this structure, `PRESERVATION_FILES_NAME` parameter could be equal to `File1` or `File2`.

You can now launch the *Packager* from the command line with:
```
python3 packager.py
```
Useful log information will be displayed during execution, requiring occasional interaction.

To enable integration in more complex workflows, it is also possible to launch the *Packager* with command line arguments:
```
python3 packager.py [-h] -w WORKING_PATH -f FILES_NAME
```
If you use the `-h` flag:
```
python3 packager.py -h
```
all instructions will be displayed.

## Support
If you require additional information or have any problem, you can contact us at:
* Nadir Dalla Pozza (nadir.dallapozza@unipd.it);
* Niccolò Pretto (niccolo.pretto@unipd.it).

## Authors and acknowledgment
This project was developed by:
* Nadir Dalla Pozza (University of Padova);
* Niccolò Pretto (University of Padova);
* Sergio Canazza (University of Padova).

This project takes advantage of the following libraries:
* [FFmpeg](https://www.ffmpeg.org/);
* [PyYaml](https://pyyaml.org).

Developed with Python IDE [PyCharm Community](https://www.jetbrains.com/pycharm/).

## License
This project is licensed with [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
