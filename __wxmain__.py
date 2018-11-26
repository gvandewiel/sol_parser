import os
import sys
from configparser import ConfigParser
from sol_parser.parser import ScoutsCollection
from sol_parser.contribution import Contribution
import wx
import wx.lib.scrolledpanel
from pubsub import pub
# from wx.lib.pubsub import pub
from pprint import pprint
import threading


# Thread class that executes processing
class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window, action):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.action = action
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread. Simulation of
        # a long process (well, 10s here) as a simple loop - you will
        # need to structure your processing so that you periodically
        # peek at the abort variable
        if self.action == 'cont':
            print('Creating Contribution Letters')
            c = Contribution(cd=self._notify_window.contributie, hf='', od=self._notify_window.odc)
            a = c.create(self._notify_window.address_list)

            while True:
                try:
                    _ret = next(a)
                    percent = int((_ret[0] / _ret[1]) * 100)
                    wx.CallAfter(pub.sendMessage, "update_cp", msg=percent)
                    
                    if self._want_abort:
                        wx.CallAfter(pub.sendMessage, "update_cp", msg=0)
                        wx.CallAfter(pub.sendMessage, "WorkerDone", msg='')
                        break
                except StopIteration:
                    wx.CallAfter(pub.sendMessage, "update_cp", msg=0)
                    self._notify_window.cont_btn.SetLabel("Contributie")
                    wx.CallAfter(pub.sendMessage, "WorkerDone", msg='')
                    break
            return

        if self.action == 'form':
            cnt = 0
            tcnt = len(self._notify_window.members.members)

            for member in self._notify_window.members:
                cnt += 1
                print(member)
                percent = int((cnt / tcnt) * 100)
                member.form(od=self._notify_window.odf)
                wx.CallAfter(pub.sendMessage, "update_fp", msg=percent)

                if self._want_abort:
                    wx.CallAfter(pub.sendMessage, "update_fp", msg=0)
                    wx.CallAfter(pub.sendMessage, "WorkerDone", msg='')
                    break
            # Done
            wx.CallAfter(pub.sendMessage, "update_fp", msg=0)
            self._notify_window.form_btn.SetLabel("ScoutsForm")
            wx.CallAfter(pub.sendMessage, "WorkerDone", msg='')

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        print('abort pressed')
        self._want_abort = 1


class SolGUI(wx.Frame):
    """."""

    def __init__(self, parent, title, app_path):
        """."""
        super(SolGUI, self).__init__(parent,
                                     title=title,
                                     size=(540, 240),
                                     style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # create a pubsub listener
        pub.subscribe(self.update_cp, "update_cp")
        pub.subscribe(self.update_fp, "update_fp")
        pub.subscribe(self.worker_done, "WorkerDone")
        self.worker = None
        self.app_path = app_path
        self.InitUI()
        self.Centre()

        self.check_defaults()

    def worker_done(self, msg):
        self.worker = None

    def update_cp(self, msg):
        """Update the progress bar."""
        self.cp.SetValue(msg)
    
    def update_fp(self, msg):
        """Update the progress bar."""
        self.fp.SetValue(msg)

    def InitUI(self):
        """."""
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(8, 3)
        
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
                                 size=(350, 25))
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
                                 size=(350, 25))
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

        # Progress bar
        self.maxPercent = 100
        self.cp = wx.Gauge(self.panel, range=100, size=(350, 25), style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.sizer.Add(self.cp,
                       pos=(3, 2),
                       span=(1, 1),
                       flag=wx.TOP | wx.LEFT | wx.BOTTOM,
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

        # Progress bar
        self.maxPercent = 100
        self.fp = wx.Gauge(self.panel, range=100, size=(350, 25), style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.sizer.Add(self.fp,
                       pos=(4, 2),
                       span=(1, 1),
                       flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                       border=0)

        # Close button
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

    def onClose(self, event):
        """"""
        self.Close()

    def OpenWndw(self, event):
        secondWindow = AdressGUI(parent=None, id=-1, title="Voeg administratie kosten toe")
        secondWindow.Show()

    def save_sum(self):
        dlg = wx.FileDialog(self.panel,
                            "Save summary file",
                            self.app_path,
                            "Overzicht_Contributie.html",
                            "*.html",
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            self.sf = dlg.GetPath()
            dlg.Close()
            dlg.Destroy()
            return True
        else:
            return False

    def save_cont_dir(self):
        dlg = wx.DirDialog(self.panel,
                           "Choose output directory",
                           self.app_path,
                           wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.odc = dlg.GetPath()
            dlg.Close()
            dlg.Destroy()
            return True
        else:
            return False

    def save_form_dir(self):
        dlg = wx.DirDialog(self.panel,
                           "Choose output directory",
                           self.app_path,
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.odf = dlg.GetPath()
            dlg.Close()
            dlg.Destroy()
            return True
        else:
            return False

    def check_defaults(self):
        if os.path.exists(os.path.join(self.app_path, 'Ledenexport.csv')):
            self.lbl_1.SetValue(os.path.join(self.app_path, 'Ledenexport.csv'))

            # Parse SOL export file
            self.members = ScoutsCollection()
            self.members(self.lbl_1.GetValue())

            # Enable buttons
            self.form_btn.Enable()
            self.sizer.Layout()

        if os.path.exists(os.path.join(self.app_path, 'contributie.ini')):
            self.lbl_2.SetValue(os.path.join(self.app_path, 'contributie.ini'))
            
            # Read contributie file and create dict of values
            reader = ConfigParser()
            reader.read(self.lbl_2.GetValue())
            
            self.contributie = dict()
            for k, v in reader.items('contributie'):
                self.contributie[k] = float(v)

            # Enable buttons
            self.cont_btn.Enable()
            self.sizer.Layout()

    def open_ledenexport(self, event):
        """."""
        fd = wx.FileDialog(self.panel,
                           "Open Ledenexport",
                           self.app_path,
                           "Ledenexport.csv",
                           "Ledenexport (*.csv)|*.csv",
                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        fd.ShowModal()
        self.lbl_1.SetValue(fd.GetPath())
        self.form_btn.Enable()
        self.sizer.Layout()

        # Parse SOL export file
        self.members = ScoutsCollection()
        self.members(self.lbl_1.GetValue())
        
    def open_contributie(self, event):
        """."""
        fd = wx.FileDialog(self.panel,
                           "Open Contributie",
                           self.app_path,
                           "contributie.ini",
                           "Contributie (*.ini)|*.ini",
                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        fd.ShowModal()
        self.lbl_2.SetValue(fd.GetPath())
        self.cont_btn.Enable()
        self.sizer.Layout()

        # Read contributie file and create dict of values
        reader = ConfigParser()
        reader.read(self.lbl_2.GetValue())
        
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
        
        if not self.worker:
            if self.save_form_dir():
                self.worker = WorkerThread(self, 'form')
                self.form_btn.SetLabel("Abort")
        else:
            self.worker.abort()
            self.worker.join()
            self.form_btn.SetLabel("ScoutsForms")

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

        if not self.worker:
            wndw2 = AdressGUI(self)
            wndw2.ShowModal()
            wndw2.Destroy()

            if self.save_cont_dir():
                self.worker = WorkerThread(self, 'cont')
                self.cont_btn.SetLabel("Abort")
        else:
            self.worker.abort()
            self.worker.join()
            self.cont_btn.SetLabel("Contributie")


class AdressGUI(wx.Dialog):
    def __init__(self, parent):
        # Create a frame
        wx.Frame.__init__(self, None, -1, "Voeg administratie kosten toe", size=(600, 200), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # Retrieve main window object
        self.parent = parent
        # Retrieve members from parent object
        members = self.parent.members

        from collections import OrderedDict
        # Group members per address
        address_list = members.group(filter_list=members.addresses, key='lid_adres')
        self.parent.address_list = OrderedDict(sorted(address_list.items()))

        # Build dialog
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, size=(600, 50), pos=(0, 0), style=wx.SIMPLE_BORDER)
        panel1.SetBackgroundColour('#FDDF99')

        panel2 = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(600, 130), pos=(0, 30), style=wx.SIMPLE_BORDER)
        panel2.SetupScrolling()
        panel2.SetBackgroundColour('#FFFFFF')
        
        self.ids = []
        for lbl in self.parent.address_list:
            self.add_cb(panel2, lbl)
        panel2.SetSizer(self.sizer)

    def add_cb(self, panel, obj):
        # Checkbox for automatic incasso
        self.cb = wx.CheckBox(panel,
                              label=obj,
                              size=(580, 25))
        self.cb.Bind(wx.EVT_CHECKBOX, self.onChecked)
        self.sizer.Add(self.cb)
        self.ids.append(self.cb.GetId())

    def onChecked(self, e):
        cb = e.GetEventObject()
        lbl = cb.GetLabel()
        self.parent.address_list[lbl]['aac'] = cb.GetValue()


def main():
    app = wx.App(False)
    app_path = os.path.dirname(sys.argv[0])
    if app_path == '':
        app_path = os.getcwd()

    ex = SolGUI(None, title="SOL PARSER", app_path=app_path)
    ex.Show()
    app.MainLoop()
    print('Finished main loop')

if __name__ == '__main__':
    main()

#if __name__ == '__main__':
#    app = wx.App()
#    frame = AdressGUI(parent=None, id=-1, title="Voeg administratie kosten toe")
#    frame.Show()
#    app.MainLoop()