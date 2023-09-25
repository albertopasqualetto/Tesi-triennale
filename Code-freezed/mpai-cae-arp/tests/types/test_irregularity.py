import pytest
from mpai_cae_arp.audio.standards import EqualizationStandard, SpeedStandard
from mpai_cae_arp.types import (
    Irregularity,
    IrregularityFile,
    IrregularityProperties,
    IrregularityType,
    Source,
)


class TestIrregularityFile:
    property = IrregularityProperties(
        reading_speed=SpeedStandard.II,
        reading_equalisation=EqualizationStandard.CCIR,
        writing_speed=SpeedStandard.III,
        writing_equalisation=EqualizationStandard.IEC,
    )

    irregularity = Irregularity(
        source=Source.AUDIO,
        time_label="00:00:00",
        type=IrregularityType.SPEED_AND_EQUALIZATION,
        properties=property,
    )

    def test_init(self):
        irf = IrregularityFile(irregularities=[self.irregularity])
        irf2 = IrregularityFile(irregularities=[])

        assert irf2.irregularities == []
        assert irf.irregularities == [self.irregularity]
        assert irf.offset is None

    def test_failing_add(self):
        irf = IrregularityFile(irregularities=[])

        with pytest.raises(TypeError):
            irf.add("irregularity")

    def test_to_json(self):
        irf = IrregularityFile(irregularities=[self.irregularity])
        irf2 = IrregularityFile(irregularities=[])

        assert irf.to_json() == {"Irregularities": [self.irregularity.to_json()]}
        assert irf2.to_json() == {"Irregularities": []}


class TestIrregularityProperties:
    prop = IrregularityProperties(
        writing_speed=SpeedStandard.II,
        reading_speed=SpeedStandard.III,
        writing_equalisation=EqualizationStandard.CCIR,
        reading_equalisation=EqualizationStandard.IEC,
    )

    def test_init(self):
        assert self.prop.writing_speed == SpeedStandard.II
        assert self.prop.reading_speed == SpeedStandard.III
        assert self.prop.writing_equalisation == EqualizationStandard.CCIR
        assert self.prop.reading_equalisation == EqualizationStandard.IEC

    def test_to_json(self):
        assert self.prop.to_json() == {
            "ReadingEqualisationStandard": "IEC",
            "ReadingSpeedStandard": 3.75,
            "WritingEqualisationStandard": "IEC1",
            "WritingSpeedStandard": 1.875,
        }

    def test_from_json(self):
        assert IrregularityProperties.from_json(self.prop.to_json()) == self.prop


class TestIrregularity:
    irreg = Irregularity(source=Source.AUDIO, time_label="00:00:00")

    def test_init(self):
        assert self.irreg.source == Source.AUDIO
        assert self.irreg.time_label == "00:00:00"
        assert self.irreg.type is None
        assert self.irreg.properties is None
        assert self.irreg.image_URI is None
        assert self.irreg.audio_block_URI is None

    def test_to_json(self):
        assert self.irreg.to_json() == {
            "IrregularityID": str(self.irreg.id),
            "Source": "a",
            "TimeLabel": "00:00:00",
        }

    def test_from_json(self):
        assert Irregularity.from_json(self.irreg.to_json()) == self.irreg
