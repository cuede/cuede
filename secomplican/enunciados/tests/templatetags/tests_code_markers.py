from unittest import TestCase

from enunciados.templatetags.code_markers import code_markers

class CodeMarkersTests(TestCase):
    def test_should_return_the_same_string_when_there_are_no_code_markers(self):
        text = 'hola como estas'

        result = code_markers(text)
        self.assertEquals(text, result)

    def test_should_return_string_surrounded_by_pre_tags(self):
        inner_text = 'hola como estas'
        text = '```{}```'.format(inner_text)

        result = code_markers(text)
        expected = '<pre>{}</pre>'.format(inner_text)
        self.assertEquals(expected, result)

    def test_one_unmatched_code_marker_does_not_get_replaced(self):
        text = '```hola como estas'

        result = code_markers(text)
        self.assertEquals(text, result)

    def test_should_replace_all_code_markers_when_more_than_one_is_matched(self):
        inner_texts = ['hola como estas?', 'bien vos?', 'bien, acá andamos']
        text = ''.join(map(lambda t: '```' + t + '```', inner_texts))

        result = code_markers(text)
        expected = ''.join(map(lambda t: '<pre>' + t + '</pre>', inner_texts))
        self.assertEquals(expected, result)

    def test_should_replace_code_markers_when_separated_by_newlines(self):
        inner_text = 'mucho codigo'
        text = '```\n{}\n```'.format(inner_text)

        result = code_markers(text)
        expected = '<pre>\n{}\n</pre>'.format(inner_text)
        self.assertEquals(expected, result)
