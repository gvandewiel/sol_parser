"""Summary
"""
from sol_parser.parser import Parser
from pprint import pprint

if __name__ == '__main__':
	scouts_list = Parser('Ledenexport.csv')
	for scout in scouts_list:
		print('{} is nu {} jaar op 01-09 {} jaar'.format(scout.naam(), scout.leeftijd, scout.m_leeftijd))
