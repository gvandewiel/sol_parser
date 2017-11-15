class parser():
    def __init__(self, csvfile):
        with open(csvfile) as csvfile:  
            self.reader = csv.DictReader(csvfile)