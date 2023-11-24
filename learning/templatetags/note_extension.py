from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re
import markdown as md

class NoteExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(NotePreprocessor(md), 'note_preprocessor', 25)

class NotePreprocessor(Preprocessor):
    RE = re.compile(r'^:::note\[(.+?)\]\n([\s\S]+?)\n:::$', re.MULTILINE)

    def run(self, lines):
        text = '\n'.join(lines)
        while self.RE.search(text):
            text = self.RE.sub(self._handle_match, text)
        return text.split('\n')

    def _handle_match(self, match):
        title = match.group(1).strip()
        body = md.markdown(match.group(2).strip(), extensions=['fenced_code', 'codehilite', 'tables'])
        return f'<div class="note">\n<h5>{title}</h5>\n{body}\n</div>'
