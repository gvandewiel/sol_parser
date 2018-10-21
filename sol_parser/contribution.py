# from ..contributie import contr_list
from fpdf import FPDF
import os
import unicodedata


def normalize(text):
    """Normalize a string to lowercase.

    To used when performing string comparisson
    """
    return unicodedata.normalize("NFKD", text.casefold())


class PDF(FPDF):
    """
    PDF class based on fpdf.

    Header contains fixed content
    Footer conains dynamic content to present the correct dates / years
    """

    def header(self):
        """PDF Header."""
        # Logo
        data_path = os.path.join(os.path.dirname(__file__),'resources')
        self.image(os.path.join(data_path, 'FL.jpg'), 25, 15, 33)
        self.image(os.path.join(data_path, 'Scouting.jpg'), 70, 20, 110)

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
        self.multi_cell(w=0, h=6, align='L', 
                        txt='Gaarne bovenstaand bedrag overmaken op bankrekening nummer (IBAN):')
        self.set_font('Arial', 'B', 12)
        self.multi_cell(w=0, h=6, align='C', txt='NL45RABO0133812006')
        self.set_font('Arial', '', 12)
        self.multi_cell(w=0, h=6, align='C', txt='')
        self.multi_cell(w=0, h=6, align='L', 
                        txt='van bovengenoesme stichting onder vermelding van:')
        self.set_font('Arial', 'I', 12)
        self.multi_cell(w=0, h=6, align='C', 
                        txt='Contributie {} / {} en het notanummer.'.format(season_start, season_end))
        self.multi_cell(w=0, h=6, align='C', txt='\n')
        self.set_font('Arial', '', 12)
        self.multi_cell(w=0,
                        h=6,
                        align='L',
                        txt=(
                            'Het bedrag mag in twee termijnen worden voldaan, het eerste voor 1 februari ' +
                            str(season_end) + ', het tweede voor 1 april ' + str(season_end) + '.'
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

class Nota():
    """Creates contribution letter for each address."""

    iNotanumber = 0
    season_start = ''
    season_end = ''

    def __init__(self,
                 ss='',
                 se='',
                 cd={},
                 od='pdf',
                 hf=''):
        """Initiation routine for class."""
        # Create output directory
        if not os.path.exists(od):
            os.makedirs(od)

        # Class variables
        type(self).season_start = ss
        type(self).season_end = se

        self.html_file = hf

        # Instance variables
        self.season_start = ss
        self.season_end = se
        self.cd = cd
        self.output_dir = od

        # start html output
        self.html_file.write(self.html_start())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit routine for class."""
        self.html_file.write(self.html_stop())

    def create_nota(self, adres, alist):
        # Instance variables
        self.adres = adres
        self.alist = alist

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

        sub_table = ''
        print('\n==============={:^25}==============='.format(self.adres.capitalize()))
        for lid in self.alist:
            if 'jeugdlid *' in normalize(lid.functie):
                if not self.bjeugdlid:
                    self.bjeugdlid = True
                    type(self).iNotanumber += 1

                    self.pdf.cell(w=100, h=6, txt='Nota voor de ouder(s)/verzorger(s) van:', ln=0, align='L')
                    self.pdf.cell(w=40,  h=6, txt='Notanumber:', ln=0, align='L')
                    self.pdf.cell(w=0,   h=6, txt='{}{}{:03}'.format(self.season_start,self.season_end, type(self).iNotanumber), ln=1, align='R')
                    self.pdf.cell(w=0,   h=6, txt='', ln=1)

                # For members of speltak 'stam' different rates are
                # applied when the have a second 'non-jeugdlid' function.
                # An update of the speltak is applied for later use.
                if 'stam' in normalize(lid.speleenheid):
                    for chk in self.alist:
                        if normalize(chk.naam) == normalize(lid.naam) and 'jeugdlid' not in normalize(chk.functie):
                            lid.speleenheid = "stam_leiding"

                # The same discount is applied when the member has a kid
                # which is a active member (i.e. the boolean bJeugdlid should be true)
                if 'stam' in normalize(lid.speleenheid) and self.bjeugdlid:
                    lid.speleenheid = "stam_leiding"

                # Determine the contribution factor
                # 1 for each scout upto 2 per adres.
                # From the 3rd scout a 50% discout is applied.
                self.cnt += 1
                if self.cnt > 2:
                    self.s_contr = 0.5 * self.cd[lid.speleenheid]
                else:
                    self.s_contr = 1.0 * self.cd[lid.speleenheid]

                self.t_contr += self.s_contr
                print('{:<25}{:<20}{:>6.2f}'.format(lid.naam, lid.speleenheid, self.s_contr))
                sub_table = sub_table + self.accordion_data(lid)
                self.pdf.cell(w=100, h=6, txt=lid.naam, ln=0, align='L')
                self.pdf.cell(w=40,  h=6, txt=lid.speleenheid.capitalize(), ln=0, align='L')
                self.pdf.cell(w=0,   h=6, txt='{}'.format(self.s_contr), ln=1, align='R')

        if self.bjeugdlid:
            self.pdf.cell(w=0, h=0, border='T', ln=1)
            self.pdf.set_font('Arial', 'B', 12)
            self.pdf.cell(w=100, h=6, txt='', ln=0)
            self.pdf.cell(w=40, h=6, txt='Totaal', ln=0, align='L')
            self.pdf.cell(w=0, h=6, txt='{}'.format(self.t_contr), ln=1, align='R')

            # Start accordion table
            self.html_file.write(self.accordion_start(lid))
            # Add additional accordion data
            self.html_file.write(sub_table)
            # Close accordion table
            self.html_file.write(self.accordion_close())

            # Print pdf output
            self.pdf.output(os.path.join(self.output_dir, '{}{}{:03} - {}.pdf'.format(self.season_start,
                                                                                      self.season_end, type(self).iNotanumber, lid.lid_e_mailadres)), 'F')
        else:
            pass
            # print('\t{: <25}{: <20}'.format(lid.naam, lid.speleenheid))

    def html_start(self):
        return '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title></title>
        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        <script src="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
        <style>
            body {
                /* Margin bottom by footer height */
                margin-bottom: 65px;
                font-size: 13px;
            }

            body > .container {
              padding: 65px 15px 0;
            }
        </style>
    </head>
    <body>
        <!-- Fixed navbar -->
        <nav class="navbar navbar-default navbar-fixed-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">Contributielijst ''' + str(self.season_start) + ''' - ''' + str(self.season_end) + '''</a>
            </div>
          </div>
        </nav>

        <div class="container">
            <div class="row">
                <div class="col-xs-12padding-0">
                    <div class="panel-heading row collapsed">
                        <div class="col-xs-3 col-sm-2">
                            <span class="pull-left"><strong>Notanumber</strong></span>
                        </div>
                        <div class="col-xs-4 col-sm-3">
                            <span class="pull-left"><strong>Adres</strong></span>
                        </div>
                        <div class="col-xs-4 col-sm-3">
                            <span class="pull-left"><strong>Achternaam</strong></span>
                        </div>
                        <div class="col-xs-1 col-sm-1 text-nowrap">
                            <div class="pull-right">
                                <span><strong>Contributie</strong></span>
                            </div>
                        </div>
                        <div class="hidden-xs col-sm-3">
                            <span class="pull-left"><strong>E-mail</strong></span>
                        </div>
                    </div>
                    <div class="panel-group" id="accordion">
'''

    def html_stop(self):
        return '''
                            </div> <!-- PANEL -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <footer class="footer navbar-fixed-bottom">
            <div class="container">
                <p class="text-muted" id="loader-icon" style="display:none;" ><strong>Loading data...</strong></p>
            </div>
        </footer>
    </body>
</html>
'''

    def accordion_start(self, lid):
        return '''
                                <div class="post panel panel-default margin-0" id="post_{notanumber}">
                                    <div class="panel-heading row collapsed" data-toggle="collapse" data-parent="#accordion" data-target="#collapse_{notanumber}">
                                        <div class="col-xs-3 col-sm-2">
                                            <span class="pull-left">{notanumber}</span>
                                        </div>
                                        <div class="col-xs-4 col-sm-3">
                                            <span class="pull-left">{address}</span>
                                        </div>
                                        <div class="col-xs-4 col-sm-3">
                                            <span class="pull-left">{lastname}</span>
                                        </div>
                                        <div class="col-xs-1 col-sm-1 text-nowrap">
                                            <div class="pull-right">
                                                <span>{contribution}</span>
                                            </div>
                                        </div>
                                        <div class="hidden-xs col-sm-3">
                                            <span class="pull-left">{email}</span>
                                        </div>
                                    </div>
                                    <div id="collapse_{notanumber}" class="panel-collapse collapse" style="height: 0px;">
                                        <div class="panel-body">
                '''.format(notanumber='{}{}{:03}'.format(self.season_start, self.season_end, type(self).iNotanumber),
                           address=lid.lid_adres,
                           lastname=lid.lid_achternaam,
                           contribution=self.t_contr,
                           email=lid.lid_e_mailadres)

    def accordion_data(self, lid):
        return '''
                                            <div class="row">
                                                <div class="col-sm-2">
                                                </div>
                                                <div class="col-sm-3">
                                                    <span class="pull-left">{naam}</span>
                                                </div>
                                                <div class="col-sm-3">
                                                    <span class="pull-left">{speleenheid}</span>
                                                </div>
                                                <div class="col-sm-1">
                                                    <span class="pull-right">{s_contr}</span>
                                                </div>
                                                <div class="hidden-xs col-sm-3">
                                                </div>
                                            </div>

        '''.format(naam=lid.naam,
                   speleenheid=lid.speleenheid,
                   s_contr=self.s_contr)

    def accordion_close(self):
        return '''
                                        </div>
                                    </div>
                                </div>
        '''
