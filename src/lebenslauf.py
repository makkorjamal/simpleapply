import yaml
import os
from collections import namedtuple
import validators
from pylatex import (
    Document, HugeText, LargeText,
    Package, Tabularx, Center,
    Tabular, MultiRow, MultiColumn,
    Command, Figure, MediumText,
    NoEscape, NewLine, VerticalSpace,
    FlushLeft
)
from pylatex.utils import bold

class Lebenslauf(Document):
    def __init__(self,
                 template_data = None,
                 input_data = None,
                 geometry_options = None
                 ):
        super().__init__(documentclass='article',
                         fontenc=None,
                         lmodern=False,
                         document_options='a4paper', 
                         geometry_options = geometry_options
                         )
        self.template_data = template_data
        self.input_data = input_data
        self.geometry_options = geometry_options

        self.packages.append(Package('fontspec'))
        self.packages.append(Package('graphicx'))
        self.packages.append(Package('multirow'))
        self.preamble.append(Package('arydshln'))
        self.preamble.append(Command('geometry', 
                                     'top=2cm, bottom=2cm, left=2cm, right=2cm'))
        fontpath = os.path.join(self.input_data['fontpath'])
        fontname = self.input_data["fontname"]
        font_command = NoEscape(
        r'''
        \setmainfont[
            Path = ''' + fontpath + r''',
            Extension = .otf,
            UprightFont = *
        ]{''' + fontname + r'''}
        ''')
        self.append(Command(font_command))

    def add_timg(self,path, size = "1.0em"):
        """
        add a small image in the personal information field
        """
        try:
            return NoEscape(r"\includegraphics[width="+size+r"]{"+path+r"}")
        except:
            return NoEscape(r"\includegraphics[width="+size+r"]{default}")

    def extract_data(self, data):
        """
        convert the yaml data to Ordered list objects
        """
        if isinstance(data, dict):
            return namedtuple('ResumeObject', data.keys())(**{k: \
                    self.extract_data(v) \
                    for k, v in data.items()})
        elif isinstance(data, list):
            return [self.extract_data(item) for item in data]
        else:
            return data

    def fill_personal(self, field_data):
        """
        Fills the personal data in the first page
        including tiny icons
        """
        with self.create(Center()):
            with self.create(Tabular("l|ll")) as ptable:
                for c in field_data: 
                    cfield = c._fields[0] 
                    cval = getattr(c, cfield)
                    ptable.add_row((MultiRow(2, \
                            data=LargeText(f"{cfield.capitalize()}")),\
                            self.add_timg(f"images/{cfield}"),\
                            LargeText(f"{cval}")))

    def fill_professional(self, field_data, fieldname):
        """
        Fills professional information
        like job experience, education etc.
        """
        tsize = "{14cm}"
        self.append(NoEscape(r"\renewcommand{\arraystretch}{3}"))
        self.append(NoEscape(r"\setlength{\tabcolsep}{4pt}"))

        with self.create(FlushLeft()):
            with self.create(Tabularx("l|p"+tsize)) as field:
                field.add_hline()
                field.add_row((MultiColumn(2, align="l", data=HugeText(
                    f"{fieldname}")),))
                field.add_hline()
                for fd in field_data:
                    for i, detail in enumerate(fd.details):
                        if validators.url(detail): details = NoEscape(\
                                r"\url{"+detail+r"}")
                        field.add_row((MultiRow(
                            len(fd.details), 
                            data=MediumText(bold(fd.title))) if i == 0 else ""
                                       , MultiColumn(1, 
                                                     align=NoEscape("p"+tsize), 
                                                     data=MediumText(detail))
                                       ))
                    field.append(NoEscape(r"\cdashline{1-1}"))

    def fill_document(self):

        self.append(VerticalSpace("10mm"))
        self.append(Command('begin', 'center'))
        self.append(HugeText(NoEscape(r"Bewerbung als " + 
                                      self.input_data['position'])))
        self.append(Command('end', 'center'))

        self.append(NoEscape(r"\noindent\rule{\textwidth}{1pt}"))
        self.append(NewLine())
        self.append(VerticalSpace("40mm"))
        with self.create(Figure(position="!ht")) as passphoto:
            passphoto.add_image(os.path.join(self.input_data['imagespath'],"passphoto"), width=NoEscape(
                r"0.5\textwidth"))

        self.append(Command('begin', 'center'))
        self.append(HugeText(NoEscape(r"" + self.input_data['name'])))
        self.append(Command('end', 'center'))
        self.append(VerticalSpace("30mm"))

        for _,v0 in self.template_data.items():
            for i, (k1,v1) in enumerate(v0.items()):
                cdata = self.extract_data(v1)
                if i == 0:
                    self.fill_personal(cdata)
                    self.append(Command(NoEscape(r"newpage")))
                else:
                    self.fill_professional(cdata,k1.capitalize())

        with self.create(Figure(position="ht")) as signature:
            signature.add_image(os.path.join(self.input_data['imagespath']
                                             ,"signature"),
                                width=NoEscape(r"0.2\linewidth"),\
                                        placement=NoEscape(r"\raggedleft"))

    def generate_document(self):
        """
        Generate the CV 
        xelatex is used to handle non standard fonts
        """
        self.generate_pdf(
                f"Lebenslauf_{self.input_data['name'].replace(' ','_')}"\
                ,compiler = 'xelatex', clean_tex=False)
