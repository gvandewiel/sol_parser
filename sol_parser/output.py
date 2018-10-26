"""Summary
"""
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
        data_path = os.path.join(os.path.dirname(__file__),'resources')
        font_path = os.path.join('sol_parser','resources','fonts')

        self.image(os.path.join(data_path, 'FL.jpg'), 25, 15, 33)
        self.image(os.path.join(data_path, 'Scouting.jpg'), 70, 20, 110)
        
        self.add_font('DejaVuSans','',os.path.join(font_path,'DejaVuSans.ttf'), uni=True)
        self.add_font('DejaVuSans','B',os.path.join(font_path,'DejaVuSans-Bold.ttf'), uni=True)
        self.add_font('DejaVuSans','I',os.path.join(font_path,'DejaVuSans-Oblique.ttf'), uni=True)
        self.set_font('DejaVuSans', 'B', 15)
        # Move "cursor" down
        self.cell(w=0, h=15, ln=1)
        # Title
        self.cell(w=70, ln=0)
        self.cell(w=80, h=20, txt='Don Garcia Moreno', border=0, ln=1, align='C')

        self.set_font('DejaVuSans', style='', size=12)
        self.cell(w=0, h=6, txt='', ln=1)
        self.cell(w=0, h=6, txt='', ln=1)

    def footer(self):
        """PDF Footer."""
        # Global variables derived from Parser
        # Position at 12.5 cm from bottom
        self.set_y(-125)

        # Set font size
        #self.add_font('Arial','','arial.ttf', uni=True)
        self.set_font('DejaVuSans', '', 12)

        # Add footer text
