import re


def convert_math_delimiters_to_dollar_signs(text):
    text = re.sub(r'\\\(\\\)', '', text)
    block_replaced = BlockMathDelimiterReplacer().replace_in(text)
    return InlineMathDelimiterReplacer().replace_in(block_replaced)


class DelimiterReplacer:
    CONTENT_GROUP_NAME = 'content'

    def __init__(self, original, new):
        self.original = original
        self.new = new

    def replace_in(self, text):
        content_pattern = r'(?P<{}>.*?)'.format(self.CONTENT_GROUP_NAME)
        pattern = r'{}{}{}'.format(self.original.opening, content_pattern, self.original.closing)
        return re.sub(
            pattern, self.replace_delimiters_in_match, text, flags=re.DOTALL
        )

    def replace_delimiters_in_match(self, match):
        content = match.group(self.CONTENT_GROUP_NAME)
        if '\n\n' in content:
            return match.group()
        return '{}{}{}'.format(self.new.opening, content, self.new.closing)


class InlineMathDelimiterReplacer(DelimiterReplacer):
    def __init__(self):
        super(InlineMathDelimiterReplacer, self).__init__(
            Delimiters(r'\\\(', r'\\\)'),
            Delimiters(r'$', r'$')
        )


class BlockMathDelimiterReplacer(DelimiterReplacer):
    def __init__(self):
        super(BlockMathDelimiterReplacer, self).__init__(
            Delimiters(r'\\\[', r'\\\]'),
            Delimiters(r'$$', r'$$')
        )


class Delimiters:
    def __init__(self, opening, closing):
        self.opening = opening
        self.closing = closing
