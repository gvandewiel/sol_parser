"""Functions and classes used for output."""
import fpdf
import os
import sys
from fpdf import FPDF_FONT_DIR, SYSTEM_TTFONTS


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

FPDF_FONT_DIR = os.path.join(resource_path('sol_parser'), 'resources', 'fonts')
SYSTEM_TTFONTS = os.path.join(resource_path('sol_parser'), 'resources', 'fonts')


class PDF(fpdf.FPDF):
    """PDF class based on fpdf."""

    def __init__(self, *args, **kwargs):
        """Subclassed FPDF class"""
        self.member = kwargs.get('member', None)
        super().__init__()
        
        # self.rp = os.path.dirname(os.path.realpath(__file__))
        self.rp = resource_path('sol_parser')
        self.dp = os.path.join(self.rp, 'resources')
        self.fp = os.path.join(self.rp, 'resources', 'fonts')

        self.set_margins(left=25.0, top=25.0, right=15.0)
        self.alias_nb_pages()

    def header(self):
        """PDF Header."""
        # Logo
        self.image(os.path.join(self.dp, 'Scouting_NL_logo_RGB.jpg'), x=self.w - 38.1 - 25, y=12.6, w=38.1, h=35.7)
        self.image(os.path.join(self.dp, 'Logo.png'), x=25, y=12.6, w=38.1, h=35.7)
        print('Trying to add fonts:')
        print(os.path.join(self.fp, 'DejaVuSans.ttf'))
        self.add_font('DejaVuSans', '', os.path.join(self.fp, 'DejaVuSans.ttf'), uni=True)
        self.add_font('DejaVuSans', 'B', os.path.join(self.fp, 'DejaVuSans-Bold.ttf'), uni=True)
        self.add_font('DejaVuSans', 'I', os.path.join(self.fp, 'DejaVuSans-Oblique.ttf'), uni=True)
        
        self.set_font('DejaVuSans', 'B', 11)
        self.set_y(55)

    def nota_end(self, aac=True):
        self.set_y(-135)

        self.font()
        self.cell(w=0, h=6, align='L', ln=1, txt='Namens Stichting Scouting Middelbeers,')
        self.cell(w=0, h=6, align='L', ln=1, txt='D. Schima, Penningmeester')
        self.cell(w=0, h=6, align='L', ln=1, txt='')
        if not aac:
            self.multi_cell(w=0, h=6, align='L', txt='U hoeft geen verdere actie te ondernemen. Het bedrag wordt automatisch, middels automatisch incasso, in 2 delen van uw rekening afgeschreven.')
        else:
            self.cell(w=0, h=6, align='L', ln=1, txt='Gelieve het totaalbedrag voor 1 februari over te boeken op bankrekeningnummer:')
            self.font(style='B')
            self.cell(w=0, h=6, align='C', ln=1, txt='NL45RABO0133812006')
            self.font()
            self.cell(w=0, h=6, align='L', ln=1, txt='t.n.v. Stichting Scouting Don Garcia Moreno te Middelbeers.')
            self.cell(w=0, h=6, align='L', ln=1, txt='Bij betaling graag het notanummer vermelden!')
            self.cell(w=0, h=6, align='L', ln=1, txt='')
            self.font(style="I")
            self.multi_cell(w=0, h=6, align='L', txt='Mocht u nog niet gekozen hebben voor automatische incasso kunt u hiervoor alsnog een machtigingsformulier opvragen via het mailadres:')
            self.cell(w=0, h=6, align='C', ln=1, txt='dieterschima@scoutingdongarciamoreno.nl')
            self.font()

        self.cell(w=0, h=6, align='L', ln=1, txt='')
        self.cell(w=0, h=6, align='L', ln=1, txt='Met vriendelijke groet,')
        self.cell(w=0, h=6, align='L', ln=1, txt='Dieter Schima')
        self.cell(w=0, h=6, align='L', ln=1, txt='Penningmeester Scouting Don Garcia Moreno')

    def footer(self):
        """PDF Footer."""
        self.image(os.path.join(self.dp, 'SN_Blad_small.jpg'), x=0, y=self.h - 38.2, w=self.w, h=38.2)

        self.font(size=9)
        self.set_y(-30)
        self.cell(w=0, h=5, ln=1, align='C', txt='Scouting Don Garcia Moreno - Konijnenberg 2 - 5091 TS Oost West en Middelbeers')
        self.cell(w=0, h=5, ln=1, align='C', txt='tel +31 (0)13 514 17 66 - e-mail contributie@scoutingdongarciamoreno.nl - web www.scoutingdongarciamoreno.nl')
        self.cell(w=0, h=5, ln=1, align='C', txt='Bank NL45RABO0133812006')
        self.font()

    def font(self, fam='DejaVuSans', style='', size=11):
        """Set default font family, style and size"""
        self.set_font(fam, style=style, size=size)

    def f_title(self, txt):
        """Write form title"""
        self.font(style='B')
        self.cell(w=0, h=8, txt=str(txt), border='B', ln=1, align='L')
        self.font()

    def f_subtitle(self, txt, ln=0):
        """Write form subtitle"""
        self.cell(w=65, h=6, txt=str(txt), ln=ln, align='L')

    def f_line(self, item, w=0, ln=1):
        """Print typle of title and attribute to pdf.
        
        Args:
            item (list) = list of tuples of strings
                           Witht title to print and attribute to print as value
        """
        if self.member is not None:
            if item[0] == '':
                self.cell(w=0, h=6, txt='', ln=ln, align='L')
            else:
                self.f_subtitle(str(item[0]))
                try:
                    self.cell(w=w, h=6, txt=str(getattr(self.member, item[1])), ln=ln, align='L')
                except AttributeError:
                    self.cell(w=w, h=6, txt='?', ln=ln, align='L')
        else:
            raise AttributeError('Member not provided.')


class Summary_Sheet():
    def __init__(self, outfile='', NotaObj=None):
        self.NotaObj = NotaObj
        self.outfile = outfile

    def html_start(self):
        self.sf = open(self.outfile, "w")

        self.sf.write('<!DOCTYPE html>\n')
        self.sf.write('<html lang="en">\n')
        self.sf.write('    <head>\n')
        self.sf.write('        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        self.sf.write('        <title></title>\n')
        self.sf.write('        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">\n')
        self.sf.write('        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>\n')
        self.sf.write('        <script src="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>\n')
        self.sf.write('        <style>\n')
        self.sf.write('            body {\n')
        self.sf.write('                /* Margin bottom by footer height */\n')
        self.sf.write('                margin-bottom: 65px;\n')
        self.sf.write('                font-size: 13px;\n')
        self.sf.write('            }\n')
        self.sf.write('\n')
        self.sf.write('            body > .container {\n')
        self.sf.write('              padding: 65px 15px 0;\n')
        self.sf.write('            }\n')
        self.sf.write('        </style>\n')
        self.sf.write('    </head>\n')
        self.sf.write('    <body>\n')
        self.sf.write('        <!-- Fixed navbar -->\n')
        self.sf.write('        <nav class="navbar navbar-default navbar-fixed-top">\n')
        self.sf.write('          <div class="container">\n')
        self.sf.write('            <div class="navbar-header">\n')
        self.sf.write('              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">\n')
        self.sf.write('                <span class="sr-only">Toggle navigation</span>\n')
        self.sf.write('                <span class="icon-bar"></span>\n')
        self.sf.write('                <span class="icon-bar"></span>\n')
        self.sf.write('                <span class="icon-bar"></span>\n')
        self.sf.write('              </button>\n')
        self.sf.write('              <a class="navbar-brand" href="#">Contributielijst</a>\n')
        self.sf.write('            </div>\n')
        self.sf.write('          </div>\n')
        self.sf.write('        </nav>\n')
        self.sf.write('\n')
        self.sf.write('        <div class="container">\n')
        self.sf.write('            <div class="row">\n')
        self.sf.write('                <div class="col-xs-12padding-0">\n')
        self.sf.write('                    <div class="panel-heading row collapsed">\n')
        self.sf.write('                        <div class="col-xs-3 col-sm-2">\n')
        self.sf.write('                            <span class="pull-left"><strong>Notanumber</strong></span>\n')
        self.sf.write('                        </div>\n')
        self.sf.write('                        <div class="col-xs-4 col-sm-3">\n')
        self.sf.write('                            <span class="pull-left"><strong>Adres</strong></span>\n')
        self.sf.write('                        </div>\n')
        self.sf.write('                        <div class="col-xs-4 col-sm-3">\n')
        self.sf.write('                            <span class="pull-left"><strong>Achternaam</strong></span>\n')
        self.sf.write('                        </div>\n')
        self.sf.write('                        <div class="col-xs-1 col-sm-1 text-nowrap">\n')
        self.sf.write('                            <div class="pull-right">\n')
        self.sf.write('                                <span><strong>Contributie</strong></span>\n')
        self.sf.write('                            </div>\n')
        self.sf.write('                        </div>\n')
        self.sf.write('                        <div class="hidden-xs col-sm-3">\n')
        self.sf.write('                            <span class="pull-left"><strong>E-mail</strong></span>\n')
        self.sf.write('                        </div>\n')
        self.sf.write('                    </div>\n')
        self.sf.write('                    <div class="panel-group" id="accordion">\n')

    def html_stop(self):
        self.sf.write('                            </div> <!-- PANEL -->\n')
        self.sf.write('                        </div>\n')
        self.sf.write('                    </div>\n')
        self.sf.write('                </div>\n')
        self.sf.write('            </div>\n')
        self.sf.write('        </div>\n')
        self.sf.write('        <footer class="footer navbar-fixed-bottom">\n')
        self.sf.write('            <div class="container">\n')
        self.sf.write('                <p class="text-muted" id="loader-icon" style="display:none;" ><strong>Loading data...</strong></p>\n')
        self.sf.write('            </div>\n')
        self.sf.write('        </footer>\n')
        self.sf.write('    </body>\n')
        self.sf.write('</html>\n')

        self.sf.close()

    def write(self, str):
        self.sf.write(str)

    def accordion_start(self, lid):
        notanumber = '{}{}{:03}'.format(lid.season_start, lid.season_end, type(self.NotaObj).iNotanumber)
        address = lid.lid_adres
        lastname = lid.lid_achternaam
        contribution = self.NotaObj.t_contr
        email = lid.lid_e_mailadres

        self.sf.write('                                <div class="post panel panel-default margin-0" id="post_{}">'.format(notanumber))
        self.sf.write('                                    <div class="panel-heading row collapsed" data-toggle="collapse" data-parent="#accordion" data-target="#collapse_{}">\n'.format(notanumber))
        self.sf.write('                                        <div class="col-xs-3 col-sm-2">\n')
        self.sf.write('                                            <span class="pull-left">{}</span>\n'.format(notanumber))
        self.sf.write('                                        </div>\n')
        self.sf.write('                                        <div class="col-xs-4 col-sm-3">\n')
        self.sf.write('                                            <span class="pull-left">{}</span>\n'.format(address))
        self.sf.write('                                        </div>\n')
        self.sf.write('                                        <div class="col-xs-4 col-sm-3">\n')
        self.sf.write('                                            <span class="pull-left">{}</span>\n'.format(lastname))
        self.sf.write('                                        </div>\n')
        self.sf.write('                                        <div class="col-xs-1 col-sm-1 text-nowrap">\n')
        self.sf.write('                                            <div class="pull-right">\n')
        self.sf.write('                                                <span>{}</span>\n'.format(contribution))
        self.sf.write('                                            </div>\n')
        self.sf.write('                                        </div>\n')
        self.sf.write('                                        <div class="hidden-xs col-sm-3">\n')
        self.sf.write('                                            <span class="pull-left">{}</span>\n'.format(email))
        self.sf.write('                                        </div>\n')
        self.sf.write('                                    </div>\n')
        self.sf.write('                                    <div id="collapse_{}" class="panel-collapse collapse" style="height: 0px;">\n'.format(notanumber))
        self.sf.write('                                        <div class="panel-body">\n')

    def accordion_data(self, naam, speleenheid, s_contr):
        r = ''
        r = r + '                                            <div class="row">\n'
        r = r + '                                                <div class="col-sm-2">\n'
        r = r + '                                                </div>\n'
        r = r + '                                                <div class="col-sm-3">\n'
        r = r + '                                                    <span class="pull-left">{}</span>\n'.format(naam)
        r = r + '                                                </div>\n'
        r = r + '                                                <div class="col-sm-3">\n'
        r = r + '                                                    <span class="pull-left">{}</span>\n'.format(speleenheid)
        r = r + '                                                </div>\n'
        r = r + '                                                <div class="col-sm-1">\n'
        r = r + '                                                    <span class="pull-right">{}</span>\n'.format(s_contr)
        r = r + '                                                </div>\n'
        r = r + '                                                <div class="hidden-xs col-sm-3">\n'
        r = r + '                                                </div>\n'
        r = r + '                                            </div>\n'
        return r

    def accordion_close(self):
        self.sf.write('                                        </div>\n')
        self.sf.write('                                    </div>\n')
        self.sf.write('                                </div>\n')
