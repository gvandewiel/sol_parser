# from ..contributie import contr_list
from .output import PDF, Summary_Sheet
import os
import unicodedata


def normalize(text):
    """Normalize a string to lowercase.

    To used when performing string comparisson
    """
    return unicodedata.normalize("NFKD", text.casefold())


class Contribution():
    """Creates contribution letter for each address."""

    iNotanumber = 0

    def __init__(self, cd={}, od='pdf', hf=''):
        """Initiation routine for class.

        Args:
            cd (dict): Dictionary with contribution values
            od (string): output directory
            hf (string): filename of html based summary file
        """
        if not os.path.exists(od):
            os.makedirs(od)

        # Instance variables
        self.hf = hf
        if self.hf != '':
            self.sf = Summary_Sheet(hf, self)
        self.cd = cd

        self.output_dir = od

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit routine for class."""
        if self.hf != '':
            self.sf.html_stop()
    '''
    def create(self, members):
        # Group members per address
        address_list = members.group(filter_list=members.addresses, key='lid_adres')
        
        address_list = dict(sorted(address_list.items()))
    '''

    def create(self, address_list):
        # start html output
        if self.hf != '':
            self.sf.html_start()

        # start pdf output (summary)
        self.spdf = PDF('L', 'mm', 'A4')
        self.spdf.add_page()
        self.spdf.set_y(55)
        self.spdf.set_auto_page_break(False)
        self.spdf.font(style='', size=9)

        # Loop over each address and generate 1 letter per address
        cnt = 0
        tcnt = len(address_list)
        for a, d in address_list.items():
            am = d['members']

            cnt += 1
            if (self.spdf.h - self.spdf.get_y()) < (6 + 40 + (len(am) * 6) + 6):
                self.spdf.add_page()
                self.spdf.set_y(55)

            self.spdf.al = self.spdf.get_y()
            self.spdf.font(style='B', size=9)
            self.spdf.cell(w=0, h=6, txt=a, border='B', ln=1)
            self.spdf.font(style='', size=9)

            # Create new nota
            self.create_single(adres=a, members=am, aac=d['aac'])

            self.spdf.cell(w=0, h=4, txt='', border='', ln=1)
            self.spdf.set_y(self.spdf.ll)
            yield (cnt, tcnt)

        # Print summary sheet to pdf
        self.spdf.output(os.path.join(self.output_dir, 'Samenvatting.pdf'), 'F')

        if self.hf != '':
            self.sf.html_stop

    def create_single(self, adres, members, aac):
        # Instance variables
        self.adres = adres
        self.members = members

        # Reset all variables
        self.bjeugdlid = False
        self.cnt = 0.
        self.t_contr = 0.

        ad = ''
        for lid in self.members:
            self.s_contr = 0.
            if 'jeugdlid *' in normalize(lid.functie):
                # If the boolean value bjeuglid is False then no member on address is found
                # that is required to pay contribution.
                if not self.bjeugdlid:
                    # First jeugdlid is found start output for Nota
                    # and increase the integer NotaNumber
                    self.bjeugdlid = True
                    type(self).iNotanumber += 1

                    # Instantiation of PDF output
                    self.pdf = PDF()
                    self.pdf.set_margins(left=25.0, top=25.0)
                    self.pdf.alias_nb_pages()

                    self.pdf.ss = lid.season_start
                    self.pdf.se = lid.season_end
                    
                    self.pdf.add_page()
                    
                    # Title
                    self.pdf.font(style='B', size=15)
                    self.pdf.set_y(65)
                    self.pdf.cell(w=0, h=8, txt='Contributie Don Garcia Moreno', ln=1, align='C')
                    self.pdf.cell(w=0, h=8, txt='', ln=1)

                    # Start PDF output
                    self.pdf.font(style='')
                    self.pdf.set_x(100)
                    self.pdf.font(style="B")
                    self.pdf.cell(w=40, h=6, txt='Notanummer:', ln=0, align='L')
                    self.pdf.cell(w=0, h=6, ln=1, align='R', txt='{}{}{:03}'.format(lid.season_start,
                                                                                    lid.season_end,
                                                                                    type(self).iNotanumber))
                    self.pdf.font()
                    self.pdf.cell(w=0, h=8, txt='', ln=1)
                    self.pdf.cell(w=100, h=6, ln=1, align='L', txt='Nota voor de ouder(s)/verzorger(s) van:')

                # For members of speltak 'stam' different rates are
                # applied when the have a second 'non-jeugdlid' function.
                # An update of the speltak is applied for later use.
                if 'stam' in normalize(lid.speleenheid):
                    for chk in self.members:
                        if normalize(chk.naam) == normalize(lid.naam) and 'jeugdlid' not in normalize(chk.functie):
                            lid.speleenheid = "stam_leiding"

                # The same discount is applied when the member has a kid
                # which is a active member (i.e. the boolean bJeugdlid should be true)
                # if 'stam' in normalize(lid.speleenheid) and self.bjeugdlid:
                #     lid.speleenheid = "stam_leiding"

                # Determine the contribution factor
                # 1 for each scout upto 2 per adres.
                # From the 3rd scout a 50% discout is applied.
                self.cnt += 1
                if self.cnt > 2:
                    self.s_contr = 0.5 * self.cd[normalize(lid.speleenheid)]
                else:
                    self.s_contr = 1.0 * self.cd[normalize(lid.speleenheid)]

                self.t_contr += self.s_contr

                print('{:<35}{:<20}{:>6.2f}'.format(lid.naam, lid.speleenheid, self.s_contr))
                
                if self.hf != '':
                    ad = ad + self.sf.accordion_data(lid.naam, lid.speleenheid, self.s_contr)
                
                self.pdf.cell(w=100, h=6, txt=lid.naam, ln=0, align='L')
                self.pdf.cell(w=40, h=6, txt=lid.speleenheid.capitalize(), ln=0, align='L')
                self.pdf.cell(w=0, h=6, txt='{:.1f}'.format(self.s_contr), ln=1, align='R')

                # Print paying member in summary sheet
                self.spdf.cell(w=75, h=6, txt=lid.naam, ln=0, align='L')
                self.spdf.cell(w=70, h=6, txt=lid.speleenheid.capitalize(), ln=0, align='L')
                self.spdf.cell(w=30, h=6, txt=lid.functie.capitalize(), ln=0, align='L')
                self.spdf.cell(w=0, h=6, txt='{:.1f}'.format(self.s_contr), ln=1, align='R')
                
                self.spdf.ll = self.spdf.get_y()

            else:
                # Print non-paying member in summary sheet
                self.spdf.cell(w=75, h=6, txt=lid.naam, ln=0, align='L')
                self.spdf.cell(w=70, h=6, txt=lid.speleenheid.capitalize(), ln=0, align='L')
                self.spdf.cell(w=30, h=6, txt=lid.functie.capitalize(), ln=0, align='L')
                self.spdf.cell(w=0, h=6, txt='{:.1f}'.format(self.s_contr), ln=1, align='R')
                
                self.spdf.ll = self.spdf.get_y()

        if self.bjeugdlid:
            # Apply additional costs
            if aac:
                self.pdf.cell(w=100, h=6, txt='Adminstratiekosten', ln=0, align='L')
                self.pdf.cell(w=40, h=6, txt='', ln=0, align='L')
                self.pdf.cell(w=0, h=6, txt='{:.1f}'.format(self.cd['adminstratiekosten']), ln=1, align='R')
                self.t_contr += self.cd['adminstratiekosten']

                self.spdf.set_xy(25, self.spdf.ll)
                self.spdf.cell(w=75, h=6, txt='Adminstratiekosten', ln=0, align='L')
                self.spdf.cell(w=70, h=6, txt='', ln=0, align='L')
                self.spdf.cell(w=30, h=6, txt='', ln=0, align='L')
                self.spdf.cell(w=0, h=6, txt='{:.1f}'.format(self.cd['adminstratiekosten']), ln=1, align='R')
                self.spdf.ll = self.spdf.get_y()

            # If boolean bjeugdlid is True finalize the output
            self.pdf.cell(w=0, h=0, border='T', ln=1)
            self.pdf.font(style='B')
            self.pdf.cell(w=100, h=6, txt='', ln=0)
            self.pdf.cell(w=40, h=6, txt='Totaal', ln=0, align='L')
            self.pdf.cell(w=0, h=6, txt='{}'.format(self.t_contr), ln=1, align='R')
            self.pdf.font()

            # Print total contribution on adres line
            self.spdf.font(style='B', size=9)
            self.spdf.set_xy(25 + 75, self.spdf.al)
            self.spdf.cell(w=70,
                           h=6,
                           border='B',
                           txt='{}{}{:03}'.format(lid.season_start, lid.season_end, type(self).iNotanumber),
                           align='L',
                           ln=0)
            
            self.spdf.cell(w=0, h=6, border='B', txt=lid.e_mailadres, align='L', ln=1)

            self.spdf.set_xy(100, self.spdf.al)
            print(self.t_contr)
            self.spdf.cell(w=0, h=6, border='B', txt='{:.1f}'.format(self.t_contr), align='R', ln=1)
            self.spdf.font(style='', size=9)

            # Start accordion table
            if self.hf != '':
                    self.sf.accordion_start(lid)

            # Add accordion data
            if self.hf != '':
                    self.sf.write(ad)

            # Close accordion table
            if self.hf != '':
                    self.sf.accordion_close()

            # Place nota notes
            self.pdf.nota_end(aac=aac)

            # Print pdf output
            self.pdf.output(os.path.join(self.output_dir, '{}{}{:03} - {}.pdf'.format(lid.season_start,
                                                                                      lid.season_end, type(self).iNotanumber, lid.e_mailadres)), 'F')
        else:
            # Print total contribution (=0) on adres line
            self.spdf.font(style='B', size=9)
            self.spdf.set_xy(140, self.spdf.al)
            self.spdf.cell(w=0, h=6, border='B', txt='{}'.format(self.t_contr), align='R', ln=1)
            self.spdf.font(style='', size=9)
