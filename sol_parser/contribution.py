from contributie import contr_list
from fpdf import FPDF
import os


class PDF(FPDF):
    """
    PDF class based on fpdf.

    Header contains fixed content
    Footer conains dynamic content to present the correct dates / years
    """

    def header(self):
        """PDF Header."""
        # Logo
        self.image('FL.jpg', 25, 15, 33)
        self.image('Scouting.jpg', 70, 20, 110)

        self.set_font('Arial', 'B', 15)
        # Move "cursor" down
        self.cell(w=0, h=15, ln=1)
        # Title
        self.cell(w=70, ln=0)
        self.cell(w=80, h=20, txt='Don Garcia Moreno', border=0, ln=1, align='C')

        self.set_font('Arial', style='', size=12)
        self.cell(w=0, h=6, txt='p/a J. van Brunschot', border=0, ln=0, align='L')
        self.cell(w=0, h=6, txt='Rabobank IBAN: NL45RABO0133812006', border=0, ln=1, align='R')
        self.cell(w=0, h=6, txt='Neereindseweg 32', border=0, ln=1, align='L')
        self.cell(w=0, h=6, txt='5091 RD Oostelbeers', border=0, ln=1, align='L')
        self.cell(w=0, h=6, txt='tel. 013-5143366', border=0, ln=1, align='L')
        self.cell(w=0, h=6, txt='', ln=1)
        self.cell(w=0, h=6, txt='', ln=1)

    def footer(self):
        """PDF Footer."""
        # Global variables derived from Parser
        season_start = Nota.season_start
        season_end = Nota.season_end

        # Position at 12.5 cm from bottom
        self.set_y(-125)

        # Set font size
        self.set_font('Arial', '', 12)

        # Add footer text
        self.multi_cell(w=0, h=6, align='L', ln=1, txt='Gaarne bovenstaand bedrag overmaken op bankrekening nummer (IBAN):')
        self.set_font('Arial', 'B', 12)
        self.multi_cell(w=0, h=6, align='C', ln=1, txt='NL45RABO0133812006')
        self.set_font('Arial', '', 12)
        self.multi_cell(w=0, h=6, align='C', ln=1, txt='')
        self.multi_cell(w=0, h=6, align='L', ln=1, txt='van bovengenoemde stichting onder vermelding van:')
        self.set_font('Arial', 'I', 12)
        self.multi_cell(w=0, h=6, align='C', ln=1, txt='Contributie {} / {} en het notanummer.'.format(season_start, season_end))
        self.multi_cell(w=0, h=6, align='C', ln=1, txt='\n')
        self.set_font('Arial', '', 12)
        self.multi_cell(w=0,
                        h=6,
                        align='L',
                        ln=1,
                        txt=(
                            'Het bedrag mag in twee termijnen worden voldaan, het eerste voor 1 februari ' + str(season_end) + ', het tweede voor 1 april ' + str(season_end) + '.'
                            'Voor de tweede termijn krijgt u geen herinnering.\n'
                            '\n'
                            '\n'
                            'Nov ' + str(season_start) + ',\n'
                            'Namens de scouting\n'
                            'A. Vroegh, Penningmeester\n'
                            'Tel.: 013-514-1766\n'
                            '\n'
                            'Het derde en volgende lid/leden uit een gezin betaalt de helft van de normaal verschuldigde contributie.'
                        ))


def html_start(html_file):
    """Begin of html file.

    Args:
        html_file (TYPE): Reference to html output file
    """
    html_file.write('<!DOCTYPE html>')
    html_file.write('<html lang="en">')
    html_file.write('    <head>')
    html_file.write('        <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_file.write('        <title></title>')
    html_file.write('        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">')
    html_file.write('        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>')
    html_file.write('        <script src="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>')
    html_file.write('    </head>')
    html_file.write('    <body>')
    html_file.write('        <div class="container">')
    html_file.write('            <table class="table-striped">')
    html_file.write('                <thead>')
    html_file.write('                    <tr>')
    html_file.write('                        <th class="col-xs-2">Notanummer</th>')
    html_file.write('                        <th class="col-xs-2">Adres</th>')
    html_file.write('                        <th class="col-xs-3">Achternaam</th>')
    html_file.write('                        <th class="col-xs-1">Contributie</th>')
    html_file.write('                        <th class="col-xs-2">Email</th>')
    html_file.write('                   </tr>')
    html_file.write('               </thead>')
    html_file.write('               <tbody>')


def html_end(html_file):
    """End of HTML file.

    Args:
        html_file (TYPE): Reference to html output file
    """
    html_file.write('               </tbody>')
    html_file.write('            </table>')
    html_file.write('        </div>')
    html_file.write('    </body>')
    html_file.write('</html>')

    html_file.close()


class Nota():
    iNotanumber = 0
    season_start = ''
    season_end = ''

    def __init__(self, adres, alist, season_start, season_end, output_dir='pdf'):
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Class variables
        type(self).season_start = season_end
        type(self).season_end = season_end

        # Instance variables
        self.season_start = season_start
        self.season_end = season_end
        self.adres = adres
        self.alist = alist
        self.output_dir = output_dir

        # Instantiation of PDF output
        self.pdf = PDF()
        self.pdf.set_margins(left=25.0, top=25.0)
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        self.pdf.set_font('Arial', '', 12)

        # Reset all variables
        self.bjeugdlid = False
        self.cnt = 0
        self.s_contr = 0
        self.t_contr = 0

    def create_nota(self):
        for lid in self.alist:
            if 'jeugdlid' in lid.Functie:
                if not self.bjeugdlid:
                    self.bjeugdlid = True
                    type(self).iNotanumber += 1

                    self.pdf.cell(w=100, h=6, txt='Nota voor de ouder(s)/verzorger(s) van:', ln=0, align='L')
                    self.pdf.cell(w=40, h=6, txt='Notanumber:', ln=0, align='L')
                    self.pdf.cell(w=0, h=6, txt='{}{}{:03}'.format(self.season_start, self.season_end, type(self).iNotanumber), ln=1, align='R')
                    self.pdf.cell(w=0, h=6, txt='', ln=1)

                # For members of speltak 'stam' different rates are
                # applied when the have a second 'non-jeugdlid' function.
                # An update of the speltak is applied for later use.
                if 'stam' in lid.Speleenheid:
                    for chk in self.alist:
                        if chk.naam == lid.naam and 'jeugdlid' not in chk.Functie:
                            lid.Speleenheid = "stam_leiding"

                # Determine the contribution factor
                # 1 for each scout upto 2 per adres.
                # From the 3rd scout a 50% discout is applied.
                self.cnt += 1
                if self.cnt > 2:
                    self.s_contr = 0.5 * contr_list[lid.Speleenheid]
                else:
                    self.s_contr = 1.0 * contr_list[lid.Speleenheid]

                self.t_contr += self.s_contr

                self.pdf.cell(w=100, h=6, txt=lid.naam, ln=0, align='L')
                self.pdf.cell(w=40, h=6, txt=lid.Speleenheid.capitalize(), ln=0, align='L')
                self.pdf.cell(w=0, h=6, txt='{}'.format(self.s_contr), ln=1, align='R')

        if self.bjeugdlid:
            self.pdf.cell(w=0, h=0, border='T', ln=1)
            self.pdf.set_font('Arial', 'B', 12)
            self.pdf.cell(w=100, h=6, txt='', ln=0)
            self.pdf.cell(w=40, h=6, txt='Totaal', ln=0, align='L')
            self.pdf.cell(w=0, h=6, txt='{}'.format(self.t_contr), ln=1, align='R')

            print(lid.Lid_adres)

            # html_file.write('<tr>')
            # html_file.write('   <td class="col-xs-2">{}{}{:03}</td>'.format(self.season_start, self.season_end, type(self).iNotanumber))
            # html_file.write('   <td class="col-xs-2">{}</td>'.format(lid.Lid_adres))
            # html_file.write('   <td class="col-xs-3">{}</td>'.format(lid.Lid_achternaam))
            # html_file.write('   <td class="col-xs-1 text-right">{}</td>'.format(self.t_contr))
            # html_file.write('   <td class="col-xs-3">{}</td>'.format(lid.Lid_e_mailadres))
            # html_file.write('</tr>')
            self.pdf.output(os.path.join(self.output_dir, '{}{}{:03} - {}.pdf'.format(self.season_start, self.season_end, type(self).iNotanumber, lid.Lid_e_mailadres)), 'F')
