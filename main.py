"""SOL (Scouting-NL) parser.

Creates contribution letters in the default output folder 'pdf'
within the project root. A different output folder can set by
adding the named keyword argument 'output_dir' to the Nota class.
"""
from sol_parser.parser import Parser
from sol_parser.contribution import Nota


if __name__ == '__main__':
    """Create adres dictionary which contains all members grouped on adres.
    For each adres a contribution letter is generated
    """

    # Parse SOL export file
    scouts_list = Parser('Ledenexport.csv')
    season_start = scouts_list.season_start
    season_end = scouts_list.season_end

    # Retrieve all members grouped by adres
    adres_list = scouts_list.group_by_adres()

    # Loop over adres list
    for adres, alist in adres_list.items():
        brief = Nota(adres, alist, season_start, season_end)
        brief.create_nota()
