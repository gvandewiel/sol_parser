"""Summary
"""
from sol_parser.parser import Parser

if __name__ == '__main__':
    scouts_list = Parser('Ledenexport.csv')
    for scout in scouts_list:
        scout.algemeen()
        print('\n')
        scout.contact()
        print('\n')
        scout.overige_info()
        print('\n')
        print('\n')
