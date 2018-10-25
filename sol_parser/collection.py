"""Summary
"""


class ScoutsCollection(object):
    def __init__(self):
        self.addresses = set()
        self.names = set()
        self.members = list()

    def add(self, obj):
        self.names.add(obj.naam)
        self.addresses.add(obj.lid_adres)
        self.members.append(obj)

    def group_by_adres(self, verbose=False):
        """Summary.

        Args:
            verbose (bool, optional): Description

        Returns:
            TYPE: Description
        """
        # Adres dictionary
        adres = dict()
        for scout in self.members:
            # Check if adres is already in dictionary
            if normalize(scout.lid_adres) not in adres:
                # No adres exists; create new adres in dict and add scout
                if verbose:
                    print('Created new adres for {:<25} ({:<25})'.format(scout.naam, scout.functie))
                adres[normalize(scout.lid_adres)] = [scout]
            else:
                # Adres exist; add scout to list
                # A scout can occurs a multitude of times in the list due to different functions
                if verbose:
                    print('\tAdded {:<25} ({:<25}) to {:<25}'.format(scout.naam, scout.functie, normalize(scout.lid_adres)))
                adres[normalize(scout.lid_adres)].append(scout)

        # Sort each list in adres based on age (youngest first)
        for key, value in adres.items():
            slist = sorted(value, key=lambda x: x.born, reverse=False)
            adres[key] = slist

        return adres

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
            if self.objLeden[y]['chk_leeftijd'] >= age and self.objLeden[y]['functie'] == "jeugdlid *":
                count = count + 1
                filtered[self.objLeden[y]['lidnummer']] = self.objLeden[y]
        return filtered, count

    def list(self):
        """Summary.

        Returns:
            TYPE: Description
        """
        return self.objLeden
