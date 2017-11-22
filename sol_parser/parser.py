"""Parser for SOL (Scouting-NL) output

Parser accepts a single positional argument: reference to a csv file

Class contains functions to calculate the current age and the age at a 'turnover' date; when a certain age is reached at the the turnover date the scout has to migrate to the next group.
"""

from csv import DictReader
from datetime import date
from dateutil.relativedelta import relativedelta
from operator import itemgetter

from .scout import Scout


class Parser():
    """Parser class for SOL csv output

    Attributes:
        migration_date (datetime): Migration date used to calculate which scouts should transfer to the next group when the season ends (at the migration date)
        objLeden (dict): Dictionary containig all members from csvfile
    """

    def __init__(self, csvfile):
        """Initiate class

        Args:
            csvfile (TYPE): Input file to parse (csv format)
        """
        self.objLeden = list()
        self.migration_date = self.migration_date()
        self.season_start, self.season_end = self.season()

        with open(csvfile) as csvfile:
            try:
                reader = DictReader(csvfile)
                for row in reader:
                    self.objLeden.append(Scout(row, self.migration_date))
            finally:
                csvfile.close()

    def __iter__(self):
        """Summary.

        Returns:
            TYPE: Description
        """
        return iter(self.objLeden)

    def migration_date(self):
        """Summary.

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

    def season(self):
        """Summary.

        Returns:
            TYPE: Description
        """
        # Return start and End year of the current season
        today = date.today()
        if today.month >= 9 and today.day >= 1:
            return (today.year, today.year+1)
        else:
            return (today.year-1, today.year)
    
    def filter_age(self, age):
        """Summary.

        Returns:
            TYPE: Description

        Args:
            age (TYPE): Description
        """
        filtered = dict()
        count = 0

        for y in self.objLeden:
            if self.objLeden[y]['chk_leeftijd'] >= age and self.objLeden[y]['Functie'] == "jeugdlid *":
                count = count + 1
                filtered[self.objLeden[y]['Lidnummer']] = self.objLeden[y]
        return filtered, count

    def list(self):
        """Summary.

        Returns:
            TYPE: Description
        """
        return self.objLeden

    def group_by_adres(self, verbose=False):
        """Summary.

        Args:
            verbose (bool, optional): Description

        Returns:
            TYPE: Description
        """
        # Adres dictionary
        adres = dict()
        for scout in self:
            # Check if adres is already in dictionary
            if scout.Lid_adres not in adres:
                # No adres exists; create new adres in dict and add scout
                if verbose:
                    print('Created new adres for {} ({})'.format(scout.naam, scout.Functie))
                adres[scout.Lid_adres] = [scout]
            else:
                # Adres exist; add scout to list
                # A scout can occurs a multitude of times in the list due to different functions
                if verbose:
                    print('\tAdded {} ({}) to {}'.format(scout.naam, scout.Functie, scout.Lid_adres))
                adres[scout.Lid_adres].append(scout)

        # Sort each list in adres based on age (youngest first)
        for key, value in adres.items():
            slist = sorted(value, key=lambda x: x.born, reverse=False)
            adres[key] = slist

        return adres
