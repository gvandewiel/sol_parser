class scout(object):
    def __init__(self, d, date):
        self.migration_date = date
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

    def calc_age(self, refdate = date.today()):
        if refdate is None:
            raise ValueError("refdate can't be empty")
        born = self.Lid_geboortedatum
        format_string = "%d-%m-%Y"
        born = datetime.strptime(born, format_string).date()
        return refdate.year - born.year - ((refdate.month, refdate.day) < (born.month, born.day))

    def current_age(self):
        return calc_age()
        
    def m_age(self):
        return calc_age(refdate = self.migration_date)