"""Parser for SOL (Scouting-NL) output

Parser class for csv files generated by the Scouts Online (SOL) program
provided by the Dutch Scouts Organisation; Scouting NL.

Parser accepts no arguments for init
When the parser is called it accepts a single positional argument:
    reference to a csv file


Class contains functions to calculate the current age and the age at a
'turnover' date; when a certain age is reached at the the turnover date the
scout has to migrate to the next group.
"""

from csv import DictReader
from datetime import date

from dateutil.relativedelta import relativedelta

from .common import normalize, str_check
from .scout import Scout


class ScoutsCollection():
    """Parser class for SOL csv output

    Attributes:
        __migration_date__ (datetime): Migration date used to calculate which
        scouts should transfer to the next group when the season ends
        (at the migration date)

        objLeden (dict): Dictionary containig all members from csvfile
    """

    def __init__(self):
        """Initiate class

        Args:
            csvfile (TYPE): Input file to parse (csv format)
        """
        self.addresses = set()
        self.names = set()
        self.members = list()

        # self.migration_date = self.migration_date()
        # self.season_start, self.season_end = self.season()

    def __call__(self, csvfile):
        """Read CSV file from SOL.

        All unique addresses and names are stored in instance lists.
        All members are stored in the self.members

        Class functions are:
            group()
            filter_age()
        """
        with open(csvfile, encoding="utf-8") as csvfile:
            try:
                reader = DictReader(csvfile)
                reader.fieldnames = [normalize(str_check(fn)) for fn in reader.fieldnames]
                # pprint(reader.fieldnames)
                for row in reader:
                    # self.members.add(Scout(row, self.migration_date))
                    member = Scout(row)

                    member.migration_date = self.__migration_date__()
                    member.season_start, member.season_end = self.__season__()
                    member.m_leeftijd = member.__calc_age__(refdate=member.migration_date)

                    self.names.add(member.naam)
                    self.addresses.add(member.lid_adres)
                    self.members.append(member)
            finally:
                csvfile.close()

    def __iter__(self):
        """Summary.

        Returns:
            TYPE: Description
        """
        return iter(self.members)

    def __migration_date__(self):
        """Summary.

        Returns:
            TYPE: Description
        """
        # setup date for checking age
        today = date.today()
        if today.month >= 9 and today.day >= 1:
            # replace day and month for given values
            # Increases current year with 1
            return today + relativedelta(day=1, month=9, years=1)
        else:
            # replace day and month for given values
            # Keeps the year equal to he current year
            return today + relativedelta(day=1, month=9)

    def __season__(self):
        """Summary.

        Returns:
            TYPE: Description
        """
        # Return start and End year of the current season
        today = date.today()
        if today.month >= 9 and today.day >= 1:
            return (today.year, today.year + 1)
        else:
            return (today.year - 1, today.year)

    def filter_age(self, age):
        """Summary.

        Returns:
            TYPE: Description

        Args:
            age (TYPE): Description
        """
        filtered = dict()
        count = 0

        for y in self.members:
            if self.members[y]['chk_leeftijd'] >= age and self.members[y]['functie'] == "jeugdlid *":
                count = count + 1
                filtered[self.members[y]['lidnummer']] = self.members[y]
        return filtered, count

    def group(self, filter_list, key):
        """Return a list of members.

        Members are grouped by items in filter_list by
        checking is member attribute KEY matches the item in the list.
        The returned list is sorted by age.

        Returns:
            dict: Containing list with members sorted by age

        Args:
            filter_list (list): list with keys for the returned dict
            key (string) : key name of the member attributes to match the
            values defined in filter list
        """
        ret = dict()
        for i in filter_list:
            _ret = dict()
            _ret['members'] = sorted(list(filter(lambda d: getattr(d, key) == i, self.members)),
                                     key=lambda x: x.born,
                                     reverse=False)
            _ret['aac'] = False

            ret[i] = _ret
        return ret
