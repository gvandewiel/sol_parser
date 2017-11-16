"""Summary
"""
from datetime import date
from datetime import *
from dateutil.relativedelta import relativedelta


class Parser():

    """Summary

    Attributes:
        chk_date (TYPE): Description
        objLeden (TYPE): Description
        reader (TYPE): Description
    """

    def __init__(self, csvfile):
        """Summary

        Args:
            csvfile (TYPE): Description
        """
        self.objLeden = dict()
        self.chk_date = turnover_date()

        with open(csvfile) as csvfile:
            try:
                self.reader = csv.DictReader(csvfile)
                for row in reader:
                    row['leeftijd'] = calculate_age(
                        row['Lid geboortedatum'], date.today())
                    row['chk_leeftijd'] = calculate_age(
                        row['Lid geboortedatum'], self.chk_date)
                    objLeden[row['Lidnummer']] = row
            finally:
                csvfile.close()

    def turnover_date():
        """Summary

        Returns:
            TYPE: Description
        """
        # setup date for checking age
        turnover_date = date.today()
        if turnover_date.month >= 9 and turnover_date.day >= 1:
            turnover_date = turnover_date + \
                relativedelta(day=1, month=9, years=1)
        else:
            turnover_date = turnover_date + relativedelta(day=1, month=9)

        return turnover_date

    def find_rsa():
        """Summary

        Returns:
            TYPE: Description
        """
        rsa = dict()
        new_rsa = 0

        for y in objLeden:
            if objLeden[y]['chk_leeftijd'] >= 14 and objLeden[y]['Functie'] == "jeugdlid *":
                new_rsa = new_rsa+1
                rsa[objLeden[y]['Lidnummer']] = objLeden[y]
        return rsa, new_rsa
