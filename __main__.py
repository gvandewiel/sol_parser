"""SOL (Scouting-NL) parser.

Creates contribution letters in the default output folder 'pdf'
within the project root. A different output folder can set by
adding the named keyword argument 'output_dir' to the Nota class.
"""
import sys
import os
from optparse import OptionParser
from configparser import ConfigParser
from sol_parser.parser import ScoutsCollection
from sol_parser.contribution import Contribution
from pprint import pprint
# from sol_parser.membership import Members

def main(args=None):
    """Create adres dictionary which contains all members grouped on adres.
    
    For each adres a contribution letter is generated
    """
    parser = OptionParser()
    parser.add_option("-i", "--in-file",
                      action="store",
                      dest="infile",
                      type='string',
                      default='Ledenexport.csv',
                      help="CSV export file from SOL")
    
    parser.add_option("-c", "--contributie",
                      action="store",
                      dest="contfile",
                      type="string",
                      default="contributie.ini",
                      help="INI file with contribution rates")

    parser.add_option("-o", "--out-file",
                      action="store",
                      dest="outfile",
                      type="string",
                      default='Overzicht_Contributie.html',
                      help="Filename of summary file")

    parser.add_option("-d", "--out-dir-con",
                      action="store",
                      dest="outdir_con",
                      type="string",
                      default='PDF Contributie',
                      help="Directory where the PDF files are stored")

    parser.add_option("-f", "--out-dir-form",
                      action="store",
                      dest="outdir_form",
                      type="string",
                      default='PDF Formulier',
                      help="Directory where the PDF files are stored")

    (options, args) = parser.parse_args()

    application_path = os.path.dirname(sys.argv[0])

    # Input file
    infile = os.path.join(application_path, options.infile)

    # Contributie file
    cf = os.path.join(application_path, options.contfile)

    # Summary file
    sf = os.path.join(application_path, options.outfile)
    
    # Output directory for contribution letters
    odc = os.path.join(application_path, options.outdir_con)

    # Output directory for ScoutsForm
    odf = os.path.join(application_path, options.outdir_form)

    # Parse SOL export file
    members = ScoutsCollection()
    members(infile)

    ScoutsForms(members, od=odf)
    Contribution_Letter(members, cf=cf, sf=sf, od=odc)


def ScoutsForms(members, od=''):
    """Create ScoutsForm

    Iterates over all members in a Scoutscollection

    Args:
        members (ScoutsCollection): Members read from csv file
        od (string): output dirctory where to store the generated forms
    """
    print('Creating ScoutsForm')
    for member in members:
        print('\t{:35}'.format(member.naam))
        member.form(od=od)


def Contribution_Letter(members, cf='', sf='', od=''):
    """Crate Contribution letter for each member

    The members are grouped by address to account for
    discount if an address has more than two members.

    Args:
        members (ScoutsCollection): Members read from csv file
        cf (string): filename of contribution file (*.ini)
        sf (string): filename for the summary file
        od (string): output directory where to store the generated letters
    """
    # Read contributie file and create dict of values
    reader = ConfigParser()
    reader.read(cf)
    
    contributie = dict()
    for k, v in reader.items('contributie'):
        contributie[k] = float(v)

    # Loop over adres list
    print('Creating Contribution Letters')
    c = Contribution(cd=contributie, hf=sf, od=od)
    c.create(members)

if __name__ == '__main__':
    main()
