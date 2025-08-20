from datetime import datetime
from pylatex.utils import bold
from pylatex import (
    Document, HugeText, Package,
    Command, Figure, MediumText,
    LongTable, NoEscape, MiniPage,
    TextBlock, VerticalSpace,FlushLeft,
    FlushRight, NewLine
)

class Anschreiben(Document):
    def __init__(self, indent = False, geometry_options = None, \
            input_data = {}, template = {}):
        super().__init__(indent = indent, geometry_options = \
                geometry_options)

        self.change_length("\TPVertModule", "1mm")
        self.change_length("\TPHorizModule", "1mm")
        self.input_data = input_data;
        self.template = template;

    def fill_document(self):
        self.packages.append(Package('setspace'))
        current_date = datetime.now().strftime("%d.%m.%Y")

        with self.create(MiniPage(width=r"\textwidth")) as page:

            with page.create(TextBlock(100, 140, 0)):
                page.append(bold(self.input_data['name']))
            with page.create(TextBlock(100, 140, 5)):
                page.append(self.input_data["address"])

            with page.create(TextBlock(100, 0, 18)):
                page.append(self.input_data["company"])
            with page.create(TextBlock(100, 0, 20)):
                page.append(self.input_data["caddress"])

            with page.create(TextBlock(100, 150, 50)):
                page.append(current_date)

            with page.create(TextBlock(100, 50, 55)):
                page.append(MediumText(bold(f"Bewerbung als \
                        {self.input_data['position']}")))

            with page.create(TextBlock(100, 0, 70)):
                if self.input_data['gender']:
                    page.append(bold(f"Sehr geehrt{self.input_data['gender']}\
                            {self.input_data['hrname']},"))
                else:
                    page.append(bold(f"Sehr geehrte Damen und Herren,"))

        self.append(VerticalSpace("73mm"))
        self.append(Command('doublespacing'))
        with self.create(FlushLeft()):
                with self.create(LongTable("p{17cm}")) as data_table:
                    for par in self.template['t1'].split('\n'): 
                        data_table.add_row([par])

        with self.create(FlushRight()):
            self.append(self.input_data['name'])
        with self.create(Figure(position="ht")) as signature:
            signature.add_image(self.input_data["signature_file"], \
                    width=NoEscape(r"0.2\linewidth"), \
                    placement=NoEscape(r"\raggedleft"))

    def generate_document(self):
        self.generate_pdf(f"Anschreiben_{self.input_data['name'].replace(' ','_')}",\
                clean_tex=False)
