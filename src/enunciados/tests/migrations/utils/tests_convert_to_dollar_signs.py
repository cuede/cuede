import unittest
from enunciados.migrations.utils.math_delimiters import convert_math_delimiters_to_dollar_signs


class ConvertToDollarSignsTest(unittest.TestCase):
    def test_empty_text_should_not_change(self):
        text = ''
        self.assertEquals(text, convert_math_delimiters_to_dollar_signs(text))

    def test_opening_and_closing_latex_block_math_delimiters_should_be_replaced_with_two_dollar_signs_each(self):
        text = '\\[\\]'
        self.assertEquals('$$$$', convert_math_delimiters_to_dollar_signs(text))

    def test_opening_and_closing_latex_block_math_delimiters_with_character_between_them_should_be_replaced_with_two_dollar_signs_each(self):
        text = '\\[ \\]'
        self.assertEquals('$$ $$', convert_math_delimiters_to_dollar_signs(text))

    def test_only_one_block_math_delimiter_does_not_get_replaced(self):
        text = '\\['
        self.assertEquals(text, convert_math_delimiters_to_dollar_signs(text))

    def test_block_delimiters_with_only_one_endline_between_them_should_be_replaced_with_two_dollar_signs_each(self):
        text = '\\[\n\\]'
        self.assertEquals('$$\n$$', convert_math_delimiters_to_dollar_signs(text))

    def test_block_delimiters_with_more_than_one_consecutive_endline_between_them_should_not_be_replaced(self):
        text = '\\[\n\n\\]'
        self.assertEquals(text, convert_math_delimiters_to_dollar_signs(text))

    def test_block_delimiters_with_text_before_and_more_than_one_consecutive_endline_between_them_should_not_be_replaced(self):
        text = 'hola\\[\n\n\\]'
        self.assertEquals(text, convert_math_delimiters_to_dollar_signs(text))

    def test_block_delimiters_with_more_than_one_non_consecutive_endline_between_them_should_be_replaced(self):
        content = '\nasldjasdjsaldsad\n'
        text = '\\[{}\\]'.format(content)
        self.assertEquals('$${}$$'.format(content), convert_math_delimiters_to_dollar_signs(text))

    def test_opening_and_closing_latex_inline_math_delimiters_with_nothing_between_them_should_be_removed(self):
        text = '\\(\\)'
        self.assertEquals('', convert_math_delimiters_to_dollar_signs(text))

    def test_opening_and_closing_latex_inline_math_delimiters_with_character_between_them_should_be_replaced_with_one_dollar_sign_each(self):
        text = '\\( \\)'
        self.assertEquals('$ $', convert_math_delimiters_to_dollar_signs(text))

    def test_opening_and_closing_latex_inline_math_delimiters_with_nothing_between_them_with_more_text_should_be_removed(self):
        prefix = 'prefix'
        suffix = 'suffix'
        text = prefix + '\\(\\)' + suffix
        self.assertEquals(prefix + suffix, convert_math_delimiters_to_dollar_signs(text))

    def test_two_pairs_of_block_delimiters_get_replaced(self):
        text = '\\[\\]\\[\\]'
        self.assertEquals('$$$$$$$$', convert_math_delimiters_to_dollar_signs(text))

    def test_two_pairs_of_inline_delimiters_get_replaced(self):
        text = '\\( \\)\\( \\)'
        self.assertEquals('$ $$ $', convert_math_delimiters_to_dollar_signs(text))

    @unittest.skip(
        'No hay ningún VersionTexto en producción que le pase esto al 17/05/2020, '
        'y haría que mi código fuese más feo.'
    )
    def test_inline_math_delimiters_are_not_replaced_if_appearing_between_block_math_delimiters(self):
        text = '\\[\\( \\)\\]'
        self.assertEquals('$$\\(\\)$$', convert_math_delimiters_to_dollar_signs(text))

    @unittest.skip(
        'No hay ningún VersionTexto en producción que le pase esto al 17/05/2020, '
        'y haría que mi código fuese más feo.'
    )
    def test_block_math_delimiters_are_not_replaced_if_appearing_between_inline_math_delimiters(self):
        text = '\\(\\[\\]\\)'
        self.assertEquals('$\\[\\]$', convert_math_delimiters_to_dollar_signs(text))

    @unittest.skip(
        'No hay ningún VersionTexto en producción que le pase esto al 17/05/2020, '
        'y haría que mi código fuese más feo.'
    )
    def test_first_inline_delimiter_wins_when_overlapping_mathmodes(self):
        text = '\\(\\[\\)\\]'
        self.assertEquals('$\\[$\\]', convert_math_delimiters_to_dollar_signs(text))

    @unittest.skip(
        'No hay ningún VersionTexto en producción que le pase esto al 17/05/2020, '
        'y haría que mi código fuese más feo.'
    )
    def test_first_block_delimiter_wins_when_overlapping_mathmodes(self):
        text = '\\[\\(\\]\\)'
        self.assertEquals('$$\\($$\\)', convert_math_delimiters_to_dollar_signs(text))




