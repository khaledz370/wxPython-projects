# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-282-g1fa54006)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from wx.adv import TaskBarIcon


fajrTime = 1000
dhuhrTime = 1001
asrTime = 1002
maghribTime = 1003
ishaTime = 1004
todayDate = 1005
nextPrayerName = 1006
nextPrayerTime = 1007

###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 464,316 ) )
        self.taskbar_icon = MyTaskBarIcon(self)

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Prayer times", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Fajr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        bSizer3.Add( self.m_staticText3, 1, wx.ALL, 5 )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Dhuhr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        bSizer3.Add( self.m_staticText4, 1, wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Asr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        bSizer3.Add( self.m_staticText5, 1, wx.ALL, 5 )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Maghrib", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        bSizer3.Add( self.m_staticText6, 1, wx.ALL, 5 )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Isha", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        bSizer3.Add( self.m_staticText7, 1, wx.ALL, 5 )


        bSizer8.Add( bSizer3, 1, wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText14 = wx.StaticText( self, fajrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )

        bSizer5.Add( self.m_staticText14, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_staticText141 = wx.StaticText( self, dhuhrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText141.Wrap( -1 )

        bSizer5.Add( self.m_staticText141, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_staticText142 = wx.StaticText( self, asrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText142.Wrap( -1 )

        bSizer5.Add( self.m_staticText142, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_staticText144 = wx.StaticText( self, maghribTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText144.Wrap( -1 )

        bSizer5.Add( self.m_staticText144, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_staticText143 = wx.StaticText( self, ishaTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText143.Wrap( -1 )

        bSizer5.Add( self.m_staticText143, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )


        bSizer8.Add( bSizer5, 1, wx.EXPAND, 5 )


        bSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel3.SetMaxSize( wx.Size( -1,100 ) )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText8 = wx.StaticText( self.m_panel3, todayDate, u"00-00-0000, 00:00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        bSizer6.Add( self.m_staticText8, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText10 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"next prayer is", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        bSizer7.Add( self.m_staticText10, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_staticText11 = wx.StaticText( self.m_panel3, nextPrayerName, u"nextPrayer", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        bSizer7.Add( self.m_staticText11, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer6.Add( bSizer7, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText9 = wx.StaticText( self.m_panel3, nextPrayerTime, u"after 00:00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        bSizer6.Add( self.m_staticText9, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.m_panel3.SetSizer( bSizer6 )
        self.m_panel3.Layout()
        bSizer6.Fit( self.m_panel3 )
        bSizer4.Add( self.m_panel3, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.m_panel2.SetSizer( bSizer4 )
        self.m_panel2.Layout()
        bSizer4.Fit( self.m_panel2 )
        bSizer2.Add( self.m_panel2, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )
    def __del__( self ):
        pass
    
    # Make the frame draggable
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_move)

    def on_left_down(self, event):
        # Save the window position and the mouse position
        self.CaptureMouse()
        position = self.GetPosition()
        mouse_position = wx.GetMousePosition()
        self.delta_x = mouse_position.x - position.x
        self.delta_y = mouse_position.y - position.y

    def on_left_up(self, event):
        # Release the mouse
        if self.HasCapture():
            self.ReleaseMouse()

    def on_move(self, event):
        # Move the window by the mouse delta
        if event.Dragging() and event.LeftIsDown():
            mouse_position = wx.GetMousePosition()
            new_position = (mouse_position.x - self.delta_x, mouse_position.y - self.delta_y)
            self.Move(new_position)


class MyTaskBarIcon(TaskBarIcon):
     def __init__(self, frame):
         TaskBarIcon.__init__(self)
 
         self.frame = frame
 
        #  self.SetIcon(wx.Icon('../icon.ico', wx.BITMAP_TYPE_PNG), 'Task bar icon')
 
         #------------
         
         self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=1)
         self.Bind(wx.EVT_MENU, self.OnTaskBarDeactivate, id=2)
         self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=3)
 
     #-----------------------------------------------------------------------
         
     def CreatePopupMenu(self):
         menu = wx.Menu()
         menu.Append(1, 'Show')
         menu.Append(2, 'Hide')
         menu.Append(3, 'Close')
 
         return menu
 
 
     def OnTaskBarClose(self, event):
         self.frame.Close()
 
 
     def OnTaskBarActivate(self, event):
         if not self.dialog.IsShown():
             self.frame.Show()
 
 
     def OnTaskBarDeactivate(self, event):
         if self.frame.IsShown():
             self.frame.Hide()

wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False) 
frame = MyDialog1(None) 
frame.Show(True) 
app.MainLoop() 