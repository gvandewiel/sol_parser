"""SOL (Scouting-NL) parser.

Creates contribution letters in the default output folder 'pdf'
within the project root. A different output folder can set by
adding the named keyword argument 'output_dir' to the Nota class.
"""
import sys, os
from optparse import OptionParser
from configparser import ConfigParser
from sol_parser.parser import Parser
from sol_parser.contribution import Nota
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

    parser.add_option("-d", "--out-dir",
                      action="store",
                      dest="outdir",
                      type="string",
                      default='Contributie PDF',
                      help="Directory where the PDF files are stored")

    (options, args) = parser.parse_args()

    application_path = os.path.dirname(sys.argv[0])

    # Input file
    infile = os.path.join(application_path, options.infile)

    # Contributie file
    cont_file = os.path.join(application_path, options.contfile)

    # Summary file
    outpath = os.path.join(application_path, options.outfile)
    
    # Output directory
    outdir = os.path.join(application_path, options.outdir)

    # Read contributie file and create dict of values
    reader = ConfigParser()
    reader.read(cont_file)
    
    contributie = dict()
    for k, v in reader.items('contributie'):
        print('  {} = {}'.format(k, v))
        contributie[k] = float(v)
    
    # Parse SOL export file
    scouts_list = Parser(infile)
    season_start = scouts_list.season_start
    season_end = scouts_list.season_end

    # Create list
    # print(scouts_list)
    # Members(scouts_list).generate_list(speltak='scouts')

    # Retrieve all members grouped by adres
    adres_list = scouts_list.group_by_adres()
    
    # Loop over adres list
    html_file = open(outpath, "w")
    with Nota(ss=season_start, se=season_end, cd=contributie, hf=html_file, od=outdir) as brief:
        for adres, alist in adres_list.items():
            brief.create_nota(adres, alist)

if __name__ == '__main__':
    main()