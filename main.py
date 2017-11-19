"""Summary."""
from sol_parser.parser import Parser
from contributie import contr_list
from pprint import pprint
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('FL.jpg', 25, 15, 33)
        self.image('Scouting.jpg', 70, 20, 110)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move "cursor" down
        self.cell(w=0, h=30, ln=1)
        # Title
        self.cell(w=70, ln=0)
        self.cell(w=80, h=20, txt='Don Garcia Moreno', border=0, ln=1, align='C')

        self.set_font('Arial', style='', size=12)
        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='p/a J. van Brunschot', border=0, ln=0, align='L')
        self.cell(w=0, h=6, txt='Rabobank IBAN: NL45RABO0133812006', border=0, ln=1, align='R')
        
        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='Neereindseweg 32', border=0, ln=1, align='L')
        
        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='5091 RD Oostelbeers', border=0, ln=1, align='L')
        
        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='tel. 013-5143366', border=0, ln=1, align='L')
        
        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=12, txt='', ln=1)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-125)
        # Arial italic 8
        self.set_font('Arial', '', 12)

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='Gaarne bovenstaand bedrag overmaken op bankrekening nummer (IBAN):', ln=1)

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='NL45 RABO 0 13 38 12 006', ln=1, align='C')

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='van bovengenoemde stichting onder melding van:', ln=1)

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='Contributie 2017/2018 én de naam of namen van de kinderen.', ln=1)

        self.cell(w=15, h=24, txt='', ln=0)
        self.cell(w=0, h=6, txt='Het bedrag mag in twee termijnen worden voldaan, het eerste voor 1 februari 2018,', ln=1)
        self.cell(w=15, h=6, txt='', ln=0)
        self.cell(w=0, h=6, txt='het tweede voor 1 april 2018. Voor de tweede termijn krijgt u geen herinnering.', ln=1)

        self.cell(w=15, h=24, txt='', ln=0)
        self.cell(w=0, h=6, txt='                18 nov 2017,', ln=1)

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='                Namen de scouting', ln=1)

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='                A. Vroegh, Penningmeester', ln=1)

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, h=6, txt='                Tel.: 013-514-1766', ln=1)

        self.cell(w=0, h=24, txt='', ln=1)

        self.cell(w=15, h=12, txt='', ln=0)
        self.cell(w=0, txt='Het derde en volgende lid/leden uit één gezin betaalt de helft van de normaal verschuldigde contributie.', ln=1)

if __name__ == '__main__':
    """Create adres dictionary which contains all members grouped on adres.
    For each adres a contribution letter is generated
    """
    # Parse SOL export file
    scouts_list = Parser('Ledenexport.csv')

    # Retrieve all members grouped by adres
    adres_list = scouts_list.group_by_adres()

    # Loop over adres list
    iNotanumber = 0
    sseason = ''
    for adres, alist in adres_list.items():

        # Instantiation of inherited class
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)

        bjeugdlid = False
        cnt = 0
        s_contr = 0
        t_contr = 0
        for lid in alist:
            # pprint(vars(lid))
            # break
            if 'jeugdlid' in lid.Functie:
                if not bjeugdlid:
                    bjeugdlid = True
                    iNotanumber += 1
                    pdf.cell(w=15, h=12, txt='', ln=0)
                    pdf.cell(w=0, h=6, txt='Nota voor de ouder(s)/verzorger(s) van:', ln=0, align='L')
                    pdf.cell(w=0, h=6, txt='Notanumber: 20172018{}'.format(iNotanumber), ln=1, align='R')
                    pdf.cell(w=0, h=12, txt='', ln=1)
                # For members of speltak 'stam' different rates are
                # applied when the have a second 'non-jeugdlid' function.
                # An update of the speltak is applied for later use.
                if 'stam' in lid.Speleenheid:
                    for chk in alist:
                        if chk.naam == lid.naam and 'jeugdlid' not in chk.Functie:
                            lid.Speleenheid = "stam_leiding"

                # Determine the contribution factor
                # 1 for each scout upto 2 per adres.
                # From the 3rd scout a 50% discout is applied.
                cnt += 1
                if cnt > 2:
                    s_contr = 0.5 * contr_list[lid.Speleenheid]
                else:
                    s_contr = 1.0 * contr_list[lid.Speleenheid]

                t_contr += s_contr

                pdf.cell(w=15, h=12, txt='', ln=0)
                pdf.cell(w=125, h=6, txt=lid.naam, ln=0, align='L')
                pdf.cell(w=40, h=6, txt=lid.Speleenheid, ln=0, align='L')
                pdf.cell(w=0, h=6, txt='{}'.format(s_contr), ln=1, align='R')
        if bjeugdlid:
            pdf.cell(w=15, h=0, txt='', ln=0)
            pdf.cell(w=0, h=0, border='T', ln=1)

            pdf.set_font('Arial', 'B', 12)
            pdf.cell(w=15, h=12, txt='', ln=0)
            pdf.cell(w=125, h=6, txt='', ln=0)
            pdf.cell(w=40, h=6, txt='Totaal', ln=0, align='L')
            pdf.cell(w=0, h=6, txt='{}'.format(t_contr), ln=1, align='R')
            pdf.output('tuto2.pdf', 'F')
