from unittest import TestCase

from enunciados.templatetags.format_post import format_post

class FormatPostTests(TestCase):
    def test_should_return_the_same_string_when_there_are_no_code_markers(self):
        text = 'hola como estas'

        result = format_post(text)
        expected = '<p>{}</p>'.format(text)
        self.assertEquals(expected, result)

    def test_should_return_string_surrounded_by_pre_tags(self):
        inner_text = 'hola como estas'
        text = '```{}```'.format(inner_text)

        result = format_post(text)
        expected = '<pre>{}</pre>'.format(inner_text)
        self.assertEquals(expected, result)

    def test_one_unmatched_code_marker_does_not_get_replaced(self):
        text = '```hola como estas'

        result = format_post(text)
        expected = '<p>{}</p>'.format(text)
        self.assertEquals(expected, result)

    def test_should_replace_all_code_markers_when_more_than_one_is_matched(self):
        inner_texts = ['hola como estas?', 'bien vos?', 'bien, acá andamos']
        text = ''.join(map(lambda t: '```' + t + '```', inner_texts))

        result = format_post(text)
        expected = ''.join(map(lambda t: '<pre>' + t + '</pre>', inner_texts))
        self.assertEquals(expected, result)

    def test_should_replace_code_markers_when_separated_by_newlines(self):
        inner_text = 'mucho codigo'
        text = '```\n{}\n```'.format(inner_text)

        result = format_post(text)
        expected = '<pre>\n{}\n</pre>'.format(inner_text)
        self.assertEquals(expected, result)

    def test_should_add_linebreaks_and_paragraphs_outside_code_markers(self):
        text = 'no\nsoy\ncodigo\n\nyo tampoco'

        result = format_post(text)
        expected = '<p>no<br>soy<br>codigo</p>\n\n<p>yo tampoco</p>'
        self.assertEquals(expected, result)

    def test_should_remove_space_only_texts_before_and_after_codemarkers(self):
        inner_text = 'strip for me baby'
        text = '\n\n\t   \t\n```{}```\n  \t\n'.format(inner_text)

        result = format_post(text)
        expected = '<pre>{}</pre>'.format(inner_text)
        self.assertEquals(expected, result)

    def test_should_strip_spaces_before_and_after_codemarkers(self):
        texts = ['primero', 'segundo', 'tercero']
        text = '{}\n\n\t   \t\n```{}```\n  \t\n{}'.format(texts[0], texts[1], texts[2])

        result = format_post(text)
        expected = '<p>{}</p><pre>{}</pre><p>{}</p>'.format(texts[0], texts[1], texts[2])
        self.assertEquals(expected, result)
