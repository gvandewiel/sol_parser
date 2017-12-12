"""Summary
"""
from datetime import *
from datetime import date
import unicodedata


def normalize(text):
    return unicodedata.normalize("NFKD", text.casefold())


class Scout(object):
    """Summary

    Attributes:
        leeftijd (TYPE): Description
        m_leeftijd (TYPE): Description
        migration_date (TYPE): Description
        naam (TYPE): Description
    """

    def __init__(self, d, date):
        """Summary

        Args:
            d (TYPE): Description
            date (TYPE): Description
        """
        self.migration_date = date
        for key, value in d.items():
            # Case-normalize key/value pairs, simulataneously replacing spaces
            # dashes and slashes with underscores.
            key = normalize(self.__attr_check__(text=key))
            # value = self.__normalize__(value)

            # Update dictionary with the normalized key/value pairs
            if isinstance(value, (list, tuple)):
                setattr(self, key, [obj(x) if isinstance(
                    x, dict) else x for x in value])
            else:
                setattr(self, key, obj(value) if isinstance(
                    value, dict) else value)

        self.naam = self.__name__()
        self.leeftijd = self.__calc_age__()
        self.m_leeftijd = self.__calc_age__(refdate=self.migration_date)

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __attr_check__(self, text=''):
        for ch in [' ', '/', '-']:
            if ch in text:
                text = text.replace(ch, '_')
        return text

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

    def algemeen(self):
        print('===== ALGEMEEN =====')
        print('Naam:\t\t\t{}'.format(self.naam))
        print('Voorletters:\t\t{}'.format(self.lid_initialen))
        print('Adres:\t\t\t{}'.format(self.lid_adres))
        print('Postcode, plaats:\t{}, {}'.format(self.lid_postcode, self.lid_plaats))
        print('Geboortedatum:\t\t{}'.format(self.lid_geboortedatum))
        print('Leeftijd:\t\t{}'.format(self.leeftijd,))
        print('Leeftijd overvliegen:\t{}'.format(self.m_leeftijd))

    def contact(self):
        print('===== CONTACT INFORMATIE =====')
        print('Ouder/verzorger 1:\t{}'.format(self.lid_naam_ouder_verzorger_1))
        print('Telefoonnumer:\t\t{}'.format(self.lid_telefoonnummer_ouder_verzorger_1))
        print('Mailadres:\t\t{}'.format(self.lid_mailadres_ouder_verzorger_1))
        print('')
        print('Ouder/verzorger 2:\t{}'.format(self.lid_naam_ouder_verzorger_2))
        print('Telefoonnumer:\t\t{}'.format(self.lid_telefoonnummer_ouder_verzorger_2))
        print('Mailadres:\t\t{}'.format(self.lid_mailadres_ouder_verzorger_2))

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
