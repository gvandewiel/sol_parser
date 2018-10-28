"""Functions and classes used for output."""
from fpdf import FPDF
import os


class PDF(FPDF):
    """PDF class based on fpdf."""

    def __init__(self, member=None):
        """Subclassed FPDF class"""
        super().__init__()
        self.member = member

    def header(self):
        """PDF Header."""
        # Logo
        data_path = os.path.join(os.path.dirname(__file__), 'resources')
        font_path = os.path.join('sol_parser', 'resources', 'fonts')

        self.image(os.path.join(data_path, 'FL.jpg'), 25, 15, 33)
        self.image(os.path.join(data_path, 'Scouting.jpg'), 70, 20, 110)
        
        self.add_font('DejaVuSans', '', os.path.join(font_path, 'DejaVuSans.ttf'), uni=True)
        self.add_font('DejaVuSans', 'B', os.path.join(font_path, 'DejaVuSans-Bold.ttf'), uni=True)
        self.add_font('DejaVuSans', 'I', os.path.join(font_path, 'DejaVuSans-Oblique.ttf'), uni=True)
        self.set_font('DejaVuSans', 'B', 15)
        
        # Move "cursor" down
        self.cell(w=0, h=15, ln=1)
        
        # Title
        self.cell(w=70, ln=0)
        self.cell(w=80, h=20, txt='Don Garcia Moreno', border=0, ln=1, align='C')

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

    def footer(self):
        """PDF Footer."""
        # Global variables derived from Parser
        # Position at 12.5 cm from bottom
        self.set_y(-125)
        # Add footer text


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
