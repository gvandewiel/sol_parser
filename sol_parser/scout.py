"""Summary"""
import os
from datetime import datetime
from datetime import date
from pprint import pprint
from .output import PDF
from .common import normalize, str_check


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
        """Print Scout"""
        return '{:<20}{:>3}'.format(self.naam, self.leeftijd)

    def __iter__(self):
        """Iterater for Scouts attributes"""
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
        """Create ScoutsForm"""
        self.pdf = PDF(self)
        self.pdf.set_margins(left=15.0, right=15.0, top=25.0)
        self.pdf.alias_nb_pages()
        self.pdf.add_page()

        self.pdf.f_title('Algemene Informatie')

        self.pdf.f_line(('Naam', 'naam'))
        self.pdf.f_line(('Voorletters', 'lid_initialen'))
        self.pdf.f_line(('Adres', 'lid_adres'))
        
        self.pdf.f_line(('Postcode & Plaats', 'lid_postcode'), w=45, ln=0)
        self.pdf.cell(w=0, h=6, txt=str(getattr(self, 'lid_plaats')), ln=1, align='L')

        self.pdf.f_line(('Geboortedatum', 'lid_geboortedatum'), w=45, ln=0)
        self.pdf.cell(w=0, h=6, txt='{:<3} op {}'.format(self.m_leeftijd, self.migration_date), ln=1, align='L')

        self.pdf.f_title('Op welke manieren kunnen wij u bereiken:')

        items = [
            ('Wij krijgen we aan de lijn', 'lid_naam_ouder_verzorger_1'),
            ('GSM Nummer 1', 'lid_telefoonnummer_ouder_verzorger_1'),
            ('Mailadres', 'lid_e_mailadres_ouder_verzorger_1'),
            ('', ''),
            ('Wij krijgen we aan de lijn', 'lid_naam_ouder_verzorger_2'),
            ('Telefoonnumer', 'lid_telefoonnummer_ouder_verzorger_2'),
            ('Mailadres', 'lid_e_mailadres_ouder_verzorger_2')
        ]

        for item in items:
            self.pdf.f_line(item)

        self.pdf.f_title('Huisarts en verzekering')
        self.pdf.font(style='I')
        self.pdf.multi_cell(w=0, h=6, txt='Door het invullen van dit formulier geeft ons toestemming om een arts te bezoeken indien wij dit nodig achten. Heeft u hier problemen mee dit graag duidelijk aangeven op het formulier.', align='L')

        items = [
            ('Huisarts', ''),
            ('Ziektekostenverzekering', 'lid_ziektekostenverzekeraar'),
            ('Polisnummer', 'lid_ziektekostenpolis_nummer')
        ]

        for item in items:
            self.pdf.f_line(item)

        self.pdf.f_title('Overige Informatie')

        info = self.overige_informatie.split('|')
        if len(info) >= 5:
                sp = info[0]
                zd = info[1]
                med = info[2]
                al = info[3]
                rem = info[4]
        else:
                sp = '-'
                zd = '-'
                med = '-'
                al = '-'
                rem = '-'

        self.pdf.f_subtitle('Zwemdiploma\'s')
        self.pdf.cell(w=0, h=6, txt=zd, ln=1, align='L')

        self.pdf.f_title('Medicijnen & Allergieën')
        self.pdf.multi_cell(w=0, h=6, txt='{}\n{}'.format(med.strip(), al.strip()), align='L')

        self.pdf.f_title('Zijn er nog andere zaken over uw zoon/dochter die belangrijk zijn om te weten:')
        self.pdf.multi_cell(w=0, h=6, txt='{}\n{}'.format(sp.strip(), rem.strip()), align='L')

        # Print pdf output
        if not os.path.exists(od):
            os.makedirs(od)
        self.pdf.output(os.path.join(od, '{}.pdf'.format(self.naam)), 'F')
