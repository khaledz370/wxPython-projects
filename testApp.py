import wx.adv

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My App')
        
        # Set up a menu for the taskbar icon
        self.popup_menu = wx.Menu()
        self.popup_menu.Append(0, 'Restore')
        self.popup_menu.Append(1, 'Exit')
        
        # Set up the taskbar icon
        self.taskbar_icon = wx.adv.TaskBarIcon()
        self.taskbar_icon.SetIcon(wx.Icon('icon.ico'), 'My App')
        self.taskbar_icon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_restore_event)

    def on_restore_event(self, event):
        self.Show(True)

    def on_close(self, event):
        self.Show(False)
    
    def on_taskbar_icon(self, event):
        if event.GetId() == 0:
            self.Show(True)
        else:
            self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
