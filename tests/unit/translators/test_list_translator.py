from mock import Mock
from translators import ListTranslator


class TestListTranslator:
    def setup(self):
        self.item_translator_mock = Mock()
        self.translator = ListTranslator(self.item_translator_mock)

    def test_init(self):
        assert self.translator.item_translator == self.item_translator_mock

    def test_from_json(self):
        item_1_json_mock = Mock()
        item_2_json_mock = Mock()
        json = [item_1_json_mock, item_2_json_mock]

        translated_item_1_mock = Mock()
        translated_item_2_mock = Mock()
        self.item_translator_mock.from_json.side_effect = [
            translated_item_1_mock,
            translated_item_2_mock,
        ]

        result = self.translator.from_json(json)

        assert isinstance(result, list)
        assert result[0] == translated_item_1_mock
        assert result[1] == translated_item_2_mock
