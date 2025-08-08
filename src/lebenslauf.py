import yaml
from collections import namedtuple
from pylatex import (
    Document,
    HugeText,
    LargeText,
    Package,
    Tabularx,
    Center,
    Tabular,
    MultiRow,
    MultiColumn,
    Command,
    Figure,
    MediumText,
    NoEscape,
    NewLine,
    VerticalSpace,
)
from pylatex.utils import bold

class Lebenslauf(Document):
    def __init__(self, template_data = None, input_data = None, geometry_options = None):
        super().__init__(documentclass='article', fontenc=None, lmodern=False,\
                document_options='a4paper', geometry_options = geometry_options)
        self.template_data = template_data
        self.template_data = template_data
        self.input_data = input_data
        self.geometry_options = geometry_options

        self.packages.append(Package('fontspec'))
        self.packages.append(Package('graphicx'))
        self.packages.append(Package('multirow'))
        self.preamble.append(Package('arydshln'))
        self.preamble.append(Command('geometry', 'top=2cm, bottom=2cm, left=2cm, right=2cm'))
        font_command = NoEscape(
        r'''
        \setmainfont[
            Path = fonts/,
            Extension = .otf,
            UprightFont = *
        ]{Fontin}
        ''')
        self.append(Command(font_command))

    def add_timg(self,path, size = "0.8em"):
        return NoEscape(r"\includegraphics[width="+size+r"]{"+path+r"}")

    def extract_data(self, data):

        if isinstance(data, dict):
            return namedtuple('ResumeObject', data.keys())(**{k: self.extract_data(v) for k, v in data.items()})
        elif isinstance(data, list):
            return [self.extract_data(item) for item in data]
        else:
            return data

    def fill_fields(self, field_data, fieldname):
        tsize = "{14cm}"
        self.append(NoEscape(r"\renewcommand{\arraystretch}{3}"))
        self.append(NoEscape(r"\setlength{\tabcolsep}{4pt}"))
        field = Tabularx("l|p"+tsize)
        field.add_hline()
        field.add_row((MultiColumn(2, align="l", data=HugeText(f"{fieldname}")),))
        field.add_hline()
        for fd in field_data:
            for i, detail in enumerate(fd.details):
                if i == 0:
                    field.add_row((MultiRow(len(fd.details), data=MediumText(bold(fd.title))), 
                                         MultiColumn(1, align=NoEscape("p"+tsize), data=MediumText(detail))
                                         ))
                else:
                    field.add_row(("", MultiColumn(1, align=NoEscape("p"+tsize), data=MediumText(detail))))
            field.append(NoEscape(r"\cdashline{1-1}"))

        self.append(Command('begin', 'flushleft'))
        self.append(field)
        self.append(Command('end', 'flushleft'))

    def fill_document(self):

        counter = self.input_data['num_of_personal_info']
        for i, (k,v) in enumerate(self.input_data.items()):
            if (i > 0 and i < counter):
                print(k,v)
        #Get the data
        print(self.template_data)
        self.append(VerticalSpace("10mm"))
        self.append(Command('begin', 'center'))
        self.append(HugeText(NoEscape(r"Bewerbung als " + self.input_data['position'])))
        self.append(Command('end', 'center'))

        self.append(NoEscape(r"\noindent\rule{\textwidth}{1pt}"))
        self.append(NewLine())
        self.append(VerticalSpace("40mm"))
        with self.create(Figure(position="!ht")) as passphoto:
            passphoto.add_image('images/passphoto', width=NoEscape(r"0.5\textwidth"))

        self.append(Command('begin', 'center'))
        self.append(HugeText(NoEscape(r"" + self.input_data['name'])))
        self.append(Command('end', 'center'))
        self.append(VerticalSpace("30mm"))
        with self.create(Center()):
            with self.create(Tabular("l|ll")) as ptable:
                for i, (k,v) in enumerate(self.input_data.items()):
                    if (i > 1 and i <= counter):
                        ptable.add_row((MultiRow(2, data=LargeText(f"{k}")),\
                                self.add_timg(f"images/{k}"),\
                                LargeText(f"{v.replace("\n","")}")))
        self.append(Command(NoEscape(r"newpage")))

        #Fill the fields
        for k,v in self.template_data.items():
            self.fill_fields(v, k)

        with self.create(Figure(position="ht")) as signature:
            signature.add_image("images/signature.png", \
                    width=NoEscape(r"0.2\linewidth"), \
                    placement=NoEscape(r"\raggedleft"))

    def generate_document(self):
        self.generate_pdf("Lebenslauf",compiler = 'xelatex', clean_tex=False)
