import os
from configparser import ConfigParser
from sol_parser.parser import ScoutsCollection
from sol_parser.contribution import Contribution
import time
import wx
import logging

class Example(wx.Frame):
    """."""

    def __init__(self, parent, title):
        """."""
        super(Example, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

    '''
    def InitMenu(self):
        # Create menu bar
        self.menuBar = wx.MenuBar()
        # create check menu
        checkMenu = wx.Menu()
        Item1 = checkMenu.Append(wx.Window.NewControlId(), "Menu 1", "", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.onCheck, Item1)
        Item2 = checkMenu.Append(wx.Window.NewControlId(), "Menu 2", "", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.onCheck, Item2)
        Item3 = checkMenu.Append(wx.Window.NewControlId(), "Menu 3", "", wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.onCheck, Item3)

        # Create a sub menu
        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Import newsfeed list...')
        imp.Append(wx.ID_ANY, 'Import bookmarks...')
        imp.Append(wx.ID_ANY, 'Import mail...')
        # Add the sub menu
        checkMenu.AppendSubMenu(imp, 'I&mport')

        # Create a menu item
        imp_item = wx.MenuItem(checkMenu,wx.ID_ANY,'&Another Import menu')
        # Create a sub menu
        imp2 = wx.Menu()
        imp2.Append(wx.ID_ANY, 'Import newsfeed list...')
        imp2.Append(wx.ID_ANY, 'Import bookmarks...')
        imp2.Append(wx.ID_ANY, 'Import mail...')
        # Set the sub menu
        imp_item.SetSubMenu(imp2)
        # Add item with sub menu to main menu
        checkMenu.Append(imp_item)

        # Attach menu bar to frame
        self.menuBar.Append(checkMenu, "&Check")
        self.SetMenuBar(self.menuBar)
    '''
    def InitUI(self):
        """."""
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(8, 2)
        
        # Read LedenExport file
        self.olf_btn = wx.Button(self.panel,
                                 label="Open LedenExport file",
                                 size=(160, 25))
        self.olf_btn.Bind(wx.EVT_BUTTON, self.open_ledenexport)
        self.sizer.Add(self.olf_btn,
                       pos=(1, 1),
                       span=(1, 1),
                       flag=wx.TOP | wx.RIGHT,
                       border=0)

        self.lbl_1 = wx.TextCtrl(self.panel,
                                 size=(230, 25))
        self.sizer.Add(self.lbl_1,
                       pos=(1, 2),
                       span=(1, 1),
                       flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                       border=0)

        # Read Contributie file
        self.ocf_btn = wx.Button(self.panel,
                                 label="Open Contribution file",
                                 size=(160, 25))
        self.ocf_btn.Bind(wx.EVT_BUTTON, self.open_contributie)
        self.sizer.Add(self.ocf_btn,
                       pos=(2, 1),
                       span=(1, 1),
                       flag=wx.TOP | wx.RIGHT,
                       border=0)

        self.lbl_2 = wx.TextCtrl(self.panel,
                                 size=(230, 25))
        self.sizer.Add(self.lbl_2,
                       pos=(2, 2),
                       span=(1, 1),
                       flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                       border=0)

        # Generate Contributie letters
        self.cont_btn = wx.Button(self.panel,
                                  label="Contributie",
                                  size=(160, 25))
        self.cont_btn.Bind(wx.EVT_BUTTON, self.Contribution_Letter)
        self.cont_btn.Disable()
        self.sizer.Add(self.cont_btn,
                       pos=(3, 1),
                       span=(1, 1),
                       flag=wx.TOP | wx.RIGHT,
                       border=0)

        # Generate ScoutForm
        self.form_btn = wx.Button(self.panel,
                                  label="ScoutsForms",
                                  size=(160, 25))
        self.form_btn.Bind(wx.EVT_BUTTON, self.ScoutsForms)
        self.form_btn.Disable()
        self.sizer.Add(self.form_btn,
                       pos=(4, 1),
                       span=(1, 1),
                       flag=wx.TOP | wx.RIGHT,
                       border=0)

        # Ok button
        self.ok_btn = wx.Button(self.panel,
                                label="Close",
                                size=(160, 25))
        self.ok_btn.Bind(wx.EVT_BUTTON, self.onClose)
        self.sizer.Add(self.ok_btn,
                       pos=(5, 1),
                       span=(1, 1),
                       flag=wx.TOP | wx.RIGHT,
                       border=0)

        # Footer
        footer = wx.StaticText(self.panel,
                               label="Scouting Don Garcia Moreno",
                               size=(420, 25))
        self.sizer.Add(footer,
                       pos=(6, 1),
                       span=(1, 2),
                       flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                       border=0)

        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def onClose(self, event):
        """"""
        self.Close()

    def save_sum(self):
        dlg = wx.FileDialog(self.panel,
                            "Save summary file",
                            os.getcwd(),
                            "Overzicht_Contributie.html",
                            "*.html",
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        dlg.ShowModal()
        self.sf = dlg.GetPath()
        dlg.Close()
        dlg.Destroy()

    def save_cont_dir(self):
        dlg = wx.DirDialog(self.panel,
                           "Choose output directory",
                           os.getcwd(),
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.ShowModal()
        self.odc = dlg.GetPath()
        dlg.Close()
        dlg.Destroy()

    def save_form_dir(self):
        dlg = wx.DirDialog(self.panel,
                           "Choose output directory",
                           os.getcwd(),
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.ShowModal()
        self.odf = dlg.GetPath()
        dlg.Close()
        dlg.Destroy()

    def open_ledenexport(self, event):
        """."""
        fd = wx.FileDialog(self.panel,
                           "Open Ledenexport",
                           os.getcwd(),
                           "Ledenexport.csv",
                           "Ledenexport (*.csv)|*.csv",
                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        fd.ShowModal()
        self.lbl_1.SetValue(fd.GetPath())
        self.form_btn.Enable()
        self.sizer.Layout()

        # Parse SOL export file
        self.members = ScoutsCollection()
        self.members(fd.GetPath())
        
    def open_contributie(self, event):
        """."""
        fd = wx.FileDialog(self.panel,
                           "Open Contributie",
                           os.getcwd(),
                           "contributie.ini",
                           "Contributie (*.ini)|*.ini",
                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        fd.ShowModal()
        self.lbl_2.SetValue(fd.GetPath())
        self.cont_btn.Enable()
        self.sizer.Layout()

        # Read contributie file and create dict of values
        reader = ConfigParser()
        reader.read(fd.GetPath())
        
        self.contributie = dict()
        for k, v in reader.items('contributie'):
            self.contributie[k] = float(v)

    def ScoutsForms(self, event):
        """Create ScoutsForm

        Iterates over all members in a Scoutscollection

        Args:
            members (ScoutsCollection): Members read from csv file
            od (string): output dirctory where to store the generated forms
        """
        self.save_form_dir()

        print('Creating ScoutForm')
        for member in self.members:
            print(member.naam)
            member.form(od=self.odf)

    def Contribution_Letter(self, event):
        """Crate Contribution letter for each member

        The members are grouped by address to account for
        discount if an address has more than two members.

        Args:
            members (ScoutsCollection): Members read from csv file
            cf (string): filename of contribution file (*.ini)
            sf (string): filename for the summary file
            od (string): output directory where to store the generated letters
        """
        self.save_sum()
        self.save_cont_dir()

        print('Creating Contribution Letters')
        c = Contribution(cd=self.contributie, hf=self.sf, od=self.odc)
        c.create(self.members)

def main():
    app = wx.App()
    ex = Example(None, title="SOL PARSER")
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()