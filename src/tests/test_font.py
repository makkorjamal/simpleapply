from pylatex import Document, Package, HugeText
from pylatex.utils import NoEscape

doc = Document(documentclass='article', fontenc=None, lmodern=False)

doc.packages.append(Package('fontspec'))

font_command = NoEscape(r'''
\setmainfont[
    Path = ../fonts/,        % Directory where your font file lives
    Extension = .otf,     % Font file extension
    UprightFont = *       % Use the file name MyFont.ttf as the upright font
]{FontinSmallCaps}
''')
doc.preamble.append(font_command)

doc.append(NoEscape(r'\section*{HugeText(Custom Font from File})'))
doc.append('This paragraph is typeset using the locally stored font file MyFont.ttf.')
doc.append(NoEscape(r'\section*{Custom Font from File}'))
doc.append('This paragraph is typeset using the locally stored font file MyFont.ttf.')
doc.generate_pdf('font_from_file',compiler = 'xelatex', clean_tex=False)
