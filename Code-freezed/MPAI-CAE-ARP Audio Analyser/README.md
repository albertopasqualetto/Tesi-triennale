# Audio Analyzer

[![MPAI CAE-ARP](https://img.shields.io/badge/MPAI%20CAE--ARP-gray?style=for-the-badge&logo=AppleMusic&logoColor=cyan&link=https://mpai.community/standards/mpai-cae/about-mpai-cae/)](https://mpai.community/standards/mpai-cae/about-mpai-cae/)

Implements the Technical Specification of [MPAI CAE-ARP](https://mpai.community/standards/mpai-cae/about-mpai-cae/#Figure2) *Audio Analyser* AIM, providing:
- 2 Irregularity Files
- Audio Files

# TODO

- [x] calculate the video/audio offset

- [ ] Read the input file(s?) and generate a list of audio files
- [x] Split each file different channels
- [x] extract silence from each channel
- [x] generate an irregularity for each silence found
- [x] save the list of irregularities as an irregularity file

- [x] get the irregularity file from video analyzer

- [x] merge the irregularity files
- [x] extract the audio from every irregularity
- [ ] for each audio irregularity, make a classification
- [x] save everything in a single irregularity file

Sample irregularityFile from Audio to Video Analyzer:
```json
{
    "Offset": 0,
    "Irregularities": [
        {
            "IrregularityID": "09859d16-3c73-4bb0-9c74-91b451e34925",
            "Source": "a",
            "TimeLabel": "00:00:00.000",
        },
        {
            "IrregularityID": "09859d16-3c73-4bb0-9c74-91b451e34925",
            "Source": "a",
            "TimeLabel": "00:00:02.000",
        },
        {
            "IrregularityID": "09859d16-3c73-4bb0-9c74-91b451e34925",
            "Source": "a",
            "TimeLabel": "00:00:05.000",
        }
    ]
}
```

Sample irregularityFile from Video to Audio Analyzer:
```json
{
    "Irregularities": [
        {
            "IrregularityID": "09859d16-3c73-4bb0-9c74-91b451e34925",
            "Source": "v",
            "TimeLabel": "00:00:10.000",
        },
        {
            "IrregularityID": "09859d16-3c73-4bb0-9c74-91b451e34925",
            "Source": "v",
            "TimeLabel": "00:00:20.000",
        },
        {
            "IrregularityID": "09859d16-3c73-4bb0-9c74-91b451e34925",
            "Source": "v",
            "TimeLabel": "00:00:30.000",
        }
    ]
}
```