from datetime import date
from datetime import *


class scout(object):

    def __init__(self, d, date):
        self.migration_date = date
        for key, value in d.items():
            key = key.replace(' ', '_')
            print(key)
            if isinstance(value, (list, tuple)):
                setattr(self, key, [obj(x) if isinstance(
                    x, dict) else x for x in value])
            else:
                setattr(self, key, obj(value) if isinstance(
                    value, dict) else value)
        self.leeftijd = self.c_age()
        self.m_leeftijd = self.m_age()

    def calc_age(self, refdate=date.today()):
        if refdate is None:
            raise ValueError("refdate can't be empty")
        born = self.Lid_geboortedatum
        format_string = "%d-%m-%Y"
        born = datetime.strptime(born, format_string).date()
        return refdate.year - born.year - ((refdate.month, refdate.day) < (born.month, born.day))

    def naam(self):
        if self.Lid_tussenvoegsel == "":
            return '{} ({}) {}'.format(self.Lid_initialen, self.Lid_voornaam, self.Lid_achternaam)
        else:
            return '{} ({}) {} {}'.format(self.Lid_initialen, self.Lid_voornaam, self.Lid_tussenvoegsel, self.Lid_achternaam)

    def c_age(self):
        return self.calc_age()

    def m_age(self):
        return self.calc_age(refdate=self.migration_date)
