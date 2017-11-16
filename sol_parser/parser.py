"""Summary
Parser class for csv files generated by the Scouts Online (SOL) program provided. y the Dutch Scouts Organisation; Scouting NL.

Class contains functions to calculate the current age and the age at a 'turnover' date; when a certain age is reached at the the turnover date the scout has to migrate to the next group.
"""
from datetime import date
# from datetime import *
from dateutil.relativedelta import relativedelta
from csv import DictReader
from .scout import scout

class Parser():

    """Summary

    Attributes:
        tdate (TYPE): Calculated turnover date
        objLeden (TYPE): Dictionary containig all members from csvfile
    """

    def __init__(self, csvfile):
        """Summary

        Args:
            csvfile (TYPE): Input file to parse (csv format)
        """
        self.objLeden = dict()
        self.migration_date = self.migration_date()

        with open(csvfile) as csvfile:
            try:
                reader = DictReader(csvfile)
                for row in reader:
                    self.objLeden[row['Lidnummer']] = scout(row, self.migration_date)
            finally:
                csvfile.close()

    def __iter__(self):
        return iter(self.objLeden.values())

    def migration_date(self):
        """Summary

        Returns:
            TYPE: Description
        """
        # setup date for checking age
        today = date.today()
        if today.month >= 9 and today.day >= 1:
            # replace day and month for given values
            # Increases current year with 1
            migration_date = today + \
                relativedelta(day=1, month=9, years=1)
        else:
            # replace day and month for given values
            # Keeps the year equal to he current year
            migration_date = today + relativedelta(day=1, month=9)

        return migration_date

    def filter_age(self, age):
        """Summary

        Returns:
            TYPE: Description
        """
        filtered = dict()
        count = 0

        for y in self.objLeden:
            if self.objLeden[y]['chk_leeftijd'] >= age and self.objLeden[y]['Functie'] == "jeugdlid *":
                count = count+1
                filtered[self.objLeden[y]['Lidnummer']] = self.objLeden[y]
        return filtered, count

    def dict(self):
        return self.objLeden

    def print(self):
        obj = self.objLeden
        if type(obj) == dict:
            for k, v in obj.items():
                if hasattr(v, '__iter__'):
                    print(k)
                    dumpclean(v)
                else:
                    print('%s : %s' % (k, v))
        elif type(obj) == list:
            for v in obj:
                if hasattr(v, '__iter__'):
                    dumpclean(v)
                else:
                    print(v)
        else:
            print(obj)
