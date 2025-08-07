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
    def __init__(self, geometry_options = None):
        super().__init__(documentclass='article', fontenc=None, lmodern=False,\
                document_options='a4paper', geometry_options = geometry_options)
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

    def add_tiny_img(self,path, size):
        with self.create(Figure(position="!ht")) as tinyimage:
            tinyimage.add_image(path, width=NoEscape(r"" + size))

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

        #Get the data
        with open('lebenslauf.yaml', 'r') as file:
            candidate_data = yaml.safe_load(file)
        candidate_data = self.extract_data(candidate_data)
        experience = candidate_data.candidate.experience
        education = candidate_data.candidate.education
        skills = candidate_data.candidate.skills
        languages = candidate_data.candidate.languages
        hobbies = candidate_data.candidate.hobbies
        #personal details
        position = "Python developer"
        name = "Jamal Makkor"
        # Setup up the CV
        self.append(VerticalSpace("10mm"))
        self.append(Command('begin', 'center'))
        self.append(HugeText(NoEscape(r"Bewerbung als " + position)))
        self.append(Command('end', 'center'))

        self.append(NoEscape(r"\noindent\rule{\textwidth}{1pt}"))
        self.append(NewLine())
        self.append(VerticalSpace("40mm"))
        with self.create(Figure(position="!ht")) as passphoto:
            passphoto.add_image('images/passphoto', width=NoEscape(r"0.5\textwidth"))

        self.append(Command('begin', 'center'))
        self.append(HugeText(NoEscape(r"" + name)))
        self.append(Command('end', 'center'))
        self.append(VerticalSpace("30mm"))
        with self.create(Center()):
            with self.create(Tabular("l|ll")) as ptable:
                ptable.add_row((MultiRow(2, data=LargeText("Address")),\
                        NoEscape(r"\includegraphics[width=0.8em]{images/address}"), LargeText("Elm street, 10000, City, Country")))
                ptable.add_row((MultiRow(2, data=LargeText("Telephone")),\
                        NoEscape(r"\includegraphics[width=0.8em]{images/telephone}"), LargeText("0123456789")))
                ptable.add_row((MultiRow(2, data=LargeText("Email")),\
                        NoEscape(r"\includegraphics[width=0.8em]{images/email}"), LargeText("contact@example.com")))
                ptable.add_row((MultiRow(2, data=LargeText("Website")),\
                        NoEscape(r"\includegraphics[width=0.8em]{images/website}"), LargeText("example.com")))
        #self.append(ptable)
        self.append(Command(NoEscape(r"newpage")))

        #Fill the fields
        self.fill_fields(experience, "Experience")
        self.fill_fields(education, "Education")
        self.fill_fields(skills, "Skills")
        self.fill_fields(skills, "Languages")
        self.fill_fields(skills, "Hobbies")
        with self.create(Figure(position="ht")) as signature:
            signature.add_image("images/signature.png", \
                    width=NoEscape(r"0.2\linewidth"), \
                    placement=NoEscape(r"\raggedleft"))


if __name__ == "__main__":

    geometry_options = {"margin":"1.5in"}
    doc = Lebenslauf(geometry_options = geometry_options)
    doc.fill_document()
    doc.generate_pdf("Lebenslauf",compiler = 'xelatex', clean_tex=False)
    tex = doc.dumps()
