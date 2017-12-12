"""SOL (Scouting-NL) parser.

Creates contribution letters in the default output folder 'pdf'
within the project root. A different output folder can set by
adding the named keyword argument 'output_dir' to the Nota class.
"""
from sol_parser.parser import Parser
from sol_parser.contribution import Nota
from sol_parser.membership import Members

if __name__ == '__main__':
    """Create adres dictionary which contains all members grouped on adres.
    For each adres a contribution letter is generated
    """

    # Parse SOL export file
    scouts_list = Parser('Ledenexport.csv')
    season_start = scouts_list.season_start
    season_end = scouts_list.season_end

    # Create list
    # print(scouts_list)
    # Members(scouts_list).generate_list(speltak='scouts')

    # Retrieve all members grouped by adres
    adres_list = scouts_list.group_by_adres()

    html_file = open("output.html", "w")

    # Loop over adres list
    with Nota(season_start, season_end, html_file=html_file, output_dir='pdf') as brief:
        for adres, alist in adres_list.items():
            brief.create_nota(adres, alist)
