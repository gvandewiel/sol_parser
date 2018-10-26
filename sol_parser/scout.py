"""Summary
"""
from datetime import *
from datetime import date
import unicodedata
from fpdf import FPDF
import os


class PDF(FPDF):
    """
    PDF class based on fpdf.

    Header contains fixed content
    Footer conains dynamic content to present the correct dates / years
    """

    def header(self):
        """PDF Header."""
        # Logo
        data_path = os.path.join(os.path.dirname(__file__),'resources')
        self.image(os.path.join(data_path, 'FL.jpg'), 25, 15, 33)
        self.image(os.path.join(data_path, 'Scouting.jpg'), 70, 20, 110)
        
        self.add_font('Arial','',os.path.join('sol_parser','resources','arial.ttf'), uni=True)
        self.set_font('Arial', 'B', 15)
        # Move "cursor" down
        self.cell(w=0, h=15, ln=1)
        # Title
        self.cell(w=70, ln=0)
        self.cell(w=80, h=20, txt='Don Garcia Moreno', border=0, ln=1, align='C')

        self.set_font('Arial', style='', size=12)
        self.cell(w=0, h=6, txt='', ln=1)
        self.cell(w=0, h=6, txt='', ln=1)

    def footer(self):
        """PDF Footer."""
        # Global variables derived from Parser
        # Position at 12.5 cm from bottom
        self.set_y(-125)

        # Set font size
        #self.add_font('Arial','','arial.ttf', uni=True)
        self.set_font('Arial', '', 12)

        # Add footer text


def normalize(text):
    return unicodedata.normalize("NFKD", text.casefold())

def str_check(str=''):
    for char in [' ', '/', '-']:
        if char in str:
            str = str.replace(char, '_')
    return str

class Scout(object):
    """Summary

    Attributes:
        leeftijd (TYPE): Description
        m_leeftijd (TYPE): Description
        migration_date (TYPE): Description
        naam (TYPE): Description
    """

    def __init__(self, d):
        """Summary

        Args:
            d (TYPE): Description
            date (TYPE): Description
        """
        for key, value in d.items():
            # Case-normalize key/value pairs, simulataneously replacing spaces
            # dashes and slashes with underscores.
            key = normalize(str_check(key))
            # value = self.__normalize__(value)

            # Update instance attributes with the normalized key/value pairs
            if isinstance(value, (list, tuple)):
                setattr(self, key, [obj(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, obj(value) if isinstance(value, dict) else value)

        self.naam = self.__name__()
        self.leeftijd = self.__calc_age__()
        # self.m_leeftijd = self.__calc_age__(refdate=self.migration_date)

    def __repr__(self):
        return '{:<20}{:>3}'.format(self.naam, self.leeftijd)

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __calc_age__(self, refdate=date.today()):
        """Summary

        Args:
            refdate (TYPE, optional): Description

        Returns:
            TYPE: Description

        Raises:
            ValueError: Description
        """
        if refdate is None:
            raise ValueError("refdate can't be empty")
        born = self.lid_geboortedatum
        format_string = "%d-%m-%Y"
        born = datetime.strptime(born, format_string).date()
        # Add datetime object for sorting purpose
        self.born = born
        return refdate.year - born.year - ((refdate.month, refdate.day) < (born.month, born.day))

    def __name__(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if self.lid_tussenvoegsel == "":
            return '{} {}'.format(self.lid_voornaam, self.lid_achternaam)
        else:
            return '{} {} {}'.format(self.lid_voornaam, self.lid_tussenvoegsel, self.lid_achternaam)

    def form(self, od=''):
        # Instantiation of PDF output
        self.pdf = PDF()
        self.pdf.set_margins(left=10.0, top=25.0)
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        
        #self.pdf.add_font('Arial', '', 'arial.ttf', uni=True)
        self.pdf.set_font('Arial', '', 10)
        
        self.algemeen()
        self.contact()

        # Print pdf output
        if not os.path.exists(od):
            os.makedirs(od)
        self.pdf.output(os.path.join(od, '{}.pdf'.format(self.naam)), 'F')

    def str2pdf(self, item):
        if item[0] == '':
            self.pdf.cell(w=0, h=6, txt='', ln=1, align='L')
        else:
            self.pdf.cell(w=40, h=6, txt=str(item[0]), ln=0, align='L')
            self.pdf.cell(w=0, h=6, txt=str(getattr(self, item[1])), ln=1, align='L')

    def algemeen(self, offset_x=0):
        items = [
            ('Naam', 'naam'),
            ('Voorletters', 'lid_initialen'),
            ('Adres', 'lid_adres'),
            ('Postcode', 'lid_postcode'),
            ('Plaats', 'lid_plaats'),
            ('Geboortedatum', 'lid_geboortedatum'),
            ('Leeftijd', 'leeftijd')
        ]

        self.pdf.cell(w=0, h=8, txt='ALGEMENE INFORMATIE', ln=1, align='C')
        for item in items:
            self.str2pdf(item)

    def contact(self, offset_x=0):
        items = [
            ('Ouder/verzorger 1', 'lid_naam_ouder_verzorger_1'),
            ('Telefoonnumer', 'lid_telefoonnummer_ouder_verzorger_1'),
            ('Mailadres', 'lid_e_mailadres_ouder_verzorger_1'),
            ('', ''),
            ('Ouder/verzorger 2', 'lid_naam_ouder_verzorger_2'),
            ('Telefoonnumer', 'lid_telefoonnummer_ouder_verzorger_2'),
            ('Mailadres', 'lid_e_mailadres_ouder_verzorger_2')
        ]
        self.pdf.set_x(self.pdf.get_x() + offset_x)
        self.pdf.cell(w=0, h=8, txt='CONTACT INFORMATIE', ln=1, align='C')
        for item in items:
            self.pdf.set_x(self.pdf.get_x() + offset_x)
            self.str2pdf(item)

    def overige_info(self):
        print('===== OVERIGE INFORMATIE =====')
        info = self.Overige_informatie.split('|')
        try:
            print('\'avonds laten plassen:\t{}'.format(info[0]))
        except:
            print('\'avonds laten plassen:\t{}'.format('-?-'))

        try:
            print('Zwemdiploma\'s:\t\t{}'.format(info[1]))
        except:
            print('Zwemdiploma\'s:\t\t{}'.format('-?-'))

        try:
            print('Medicijnen:\t\t{}'.format(info[2]))
        except:
            print('Medicijnen:\t\t{}'.format('-?-'))

        try:
            print('Allergieen:\t\t{}'.format(info[3]))
        except:
            print('Allergieen:\t\t{}'.format('-?-'))

        try:
            print('Opmerkingen:\t\t{}'.format(info[4]))
        except:
            print('Opmerkingen:\t\t{}'.format('-?-'))

