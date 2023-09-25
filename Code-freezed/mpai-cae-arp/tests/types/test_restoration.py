import tempfile
import pytest
import json
from mpai_cae_arp.audio.standards import EqualizationStandard, SpeedStandard
from mpai_cae_arp.types.restoration import Restoration, EditingList


class TestRestoration:

    data_dict = {
        "id": "00000000-0000-0000-0000-000000000000",
        "preservation_audio_file_start": "00:00:00.000",
        "preservation_audio_file_end": "00:00:10.000",
        "restored_audio_file_URI": "https://www.google.com",
        "reading_backwards": False,
        "applied_speed_standard": 15,
        "applied_sample_frequency": 44100,
        "applied_equalization_standard": "IEC1"
    }

    my_rest = Restoration(id="00000000-0000-0000-0000-000000000000",
                          preservation_audio_file_start="00:00:00.000",
                          preservation_audio_file_end="00:00:10.000",
                          reading_backwards=False,
                          applied_sample_frequency=44100,
                          applied_speed_standard=SpeedStandard.V,
                          applied_equalization_standard=EqualizationStandard.CCIR,
                          restored_audio_file_URI="https://www.google.com")

    def test_init_from_dict(self):
        assert Restoration(**self.data_dict) == self.my_rest

    def test_init_from_object(self):
        assert Restoration(**self.my_rest.model_dump()) == self.my_rest

    def test_init_from_json(self):
        assert Restoration.model_validate_json(self.my_rest.model_dump_json()) == self.my_rest

    def test_json_serialize(self):
        assert '"id":"00000000-0000-0000-0000-000000000000"' in self.my_rest.model_dump_json()
        assert '"RestorationID":"00000000-0000-0000-0000-000000000000"' in self.my_rest.model_dump_json(
            by_alias=True)


class TestEditingList:

    data_dict = {
        "original_speed_standard": 15,
        "original_equalization_standard": "IEC1",
        "original_sample_frequency": 44100,
        "restorations": [{
            "id": "00000000-0000-0000-0000-000000000000",
            "preservation_audio_file_start": "00:00:00.000",
            "preservation_audio_file_end": "00:00:10.000",
            "restored_audio_file_URI": "https://www.google.com",
            "reading_backwards": False,
            "applied_speed_standard": 15,
            "applied_sample_frequency": 44100,
            "applied_equalization_standard": "IEC1"
        }]
    }

    rest = Restoration(preservation_audio_file_start="00:00:00.000",
                       preservation_audio_file_end="00:00:10.000",
                       restored_audio_file_URI="https://www.google.com",
                       reading_backwards=False,
                       applied_speed_standard=SpeedStandard.V,
                       applied_sample_frequency=44100,
                       applied_equalization_standard=EqualizationStandard.CCIR)

    my_editing_list: EditingList = EditingList(
        original_speed_standard=SpeedStandard.V,
        original_equalization_standard=EqualizationStandard.CCIR,
        original_sample_frequency=44100,
        restorations=[])\
            .add(Restoration(
                id="00000000-0000-0000-0000-000000000000",
                preservation_audio_file_start="00:00:00.000",
                preservation_audio_file_end="00:00:10.000",
                restored_audio_file_URI="https://www.google.com",
                reading_backwards=False,
                applied_speed_standard=SpeedStandard.V,
                applied_sample_frequency=44100,
                applied_equalization_standard=EqualizationStandard.CCIR
            )
        )

    def test_init_from_dict(self):
        assert EditingList(**self.data_dict) == self.my_editing_list

    def test_init_from_object(self):
        assert EditingList(**self.my_editing_list.model_dump()) == self.my_editing_list

    def test_init_from_json(self):
        assert EditingList.model_validate_json(
            self.my_editing_list.model_dump_json()) == self.my_editing_list

    def test_add(self):
        tmp: EditingList = self.my_editing_list.model_copy(deep=True)
        tmp.add(self.rest)

        assert len(tmp.restorations) == 2

    def test_remove(self):
        tmp: EditingList = self.my_editing_list\
                            .model_copy(deep=True)\
                            .remove(self.my_editing_list.restorations[0])

        assert len(tmp.restorations) == 0

        with pytest.raises(ValueError):
            tmp.remove(self.rest)

    def test_remove_by_id(self):
        tmp: EditingList = self.my_editing_list\
                            .model_copy(deep=True)\
                            .remove_by_id(self.my_editing_list.restorations[0].id)

        assert len(tmp.restorations) == 0

        with pytest.raises(ValueError):
            tmp.remove_by_id(self.rest.id)

    def test_save_as_json_file(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        
        self.my_editing_list.save_as_json_file(tmp.name)
        with open(tmp.name, 'r') as f:
            tmp_content = json.load(f)
            assert self.my_editing_list.model_dump(mode='json', by_alias=True) == tmp_content
