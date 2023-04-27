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
import wx.lib.mixins.inspection
from praytimes import PrayTimes
from datetime import datetime, timedelta
from tendo import singleton
import json
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

try:
    me = singleton.SingleInstance()  # this raises an exception if another instance is running
except singleton.SingleInstanceException:
    app = wx.App(False) 
    msg = "Another instance is already running, quitting."
    caption = "Already running!"
    dlg = wx.MessageDialog(None , msg, caption, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()
    sys.exit(1)

fajrLabel = 1000
fajrTime = 1001
dhuhrLabel = 1002
dhuhrTime = 1003
asrLabel = 1004
asrTime = 1005
maghribLabel = 1006
maghribTime = 1007
ishaLabel = 1008
ishaTime = 1009
todayDate = 1010
nextPrayerName = 1011
nextPrayerTime = 1012
latValue = 1013
longValue = 1014
timeZoneValue = 1015
methodValue = 1016
asrValue = 1017
dhuhrValue = 1018
fajrValue = 1019
maghribValue = 1020
ishaValue = 1021
minimized = 1022
trValue = 1023

prayersList = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
methods = ["MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari"]
asrMethods = ["Standard", "Hanafi"]
timezones = list(range(-12, 12))
menu = ['', ["settings", 'Exit']]
menuMain = ['', ["hide", "settings", 'Exit']]
tooltip = 'prayer times'
secondsInDay = 86400
fontsize = 15
font = ("Arial", fontsize)
appSize = (340, 320)
defaultSettings = {'lat': 29.9, 'long': 31.2, 'timeZone': 2, 'method': 'Egypt', 'fajr': 19.5, 'dhuhr': 0,
                   'asr': 'Standard', 'maghrib': 1, 'isha': 17.5, 'minimized': 1, "trValue": 400}
appdataFolder = f"{os.getenv('APPDATA')}\prayerTimes"
appdataFile = f"{appdataFolder}\config.json"
appdataFolder = f"{os.getenv('APPDATA')}\prayerTimes"
appdataFile = f"{appdataFolder}\config.json"
mainDir = f"{os.path.dirname(__file__)}"
audioFile = f'{mainDir}\\resources\\audio\\Bismillah.wav'
appIcon = f"{mainDir}\\resources\img\prayertimes.png"
settingsIcon = f"{mainDir}\\resources\img\prayertimesSettings.png"

activePrayercolor = wx.Colour(30, 129, 176)

# settings
try:
    if not os.path.exists(appdataFolder):
        os.mkdir(appdataFolder)
    if not os.path.exists(appdataFile):
        open(appdataFile, "x")
    file = open(appdataFile, "r")
except:
    file = open(appdataFile, "r")

try:
    settings = json.load(file)
    # print('load settings from config')
except:
    settings = defaultSettings
    with open(appdataFile, 'w') as file:
        json.dump(defaultSettings, file)
    # print("Load default settings")    

###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 358,375 ), style = wx.RESIZE_BORDER )

        self.SetSizeHints( wx.Size( 358,375 ),wx.Size( 358,375 ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Prayer times", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        self.m_staticText1.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1.Add( self.m_staticText1, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        fajr_row = wx.BoxSizer( wx.HORIZONTAL )

        self.fajr_text = wx.StaticText( self, fajrLabel, u"Fajr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.fajr_text.Wrap( -1 )

        self.fajr_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.fajr_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        fajr_row.Add( self.fajr_text, 1, wx.ALL|wx.EXPAND, 10 )

        self.fajr_time = wx.StaticText( self, fajrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.fajr_time.Wrap( -1 )

        self.fajr_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.fajr_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        fajr_row.Add( self.fajr_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10 )


        bSizer8.Add( fajr_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

        dhuhr_row = wx.BoxSizer( wx.HORIZONTAL )

        self.dhuhr_text = wx.StaticText( self, dhuhrLabel, u"Dhuhr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dhuhr_text.Wrap( -1 )

        self.dhuhr_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.dhuhr_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        dhuhr_row.Add( self.dhuhr_text, 1, wx.ALL|wx.EXPAND, 10 )

        self.dhuhr_time = wx.StaticText( self, dhuhrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.dhuhr_time.Wrap( -1 )

        self.dhuhr_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.dhuhr_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        dhuhr_row.Add( self.dhuhr_time, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALL, 10 )


        bSizer8.Add( dhuhr_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

        asrt_row = wx.BoxSizer( wx.HORIZONTAL )

        self.asr_text = wx.StaticText( self, asrLabel, u"Asr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.asr_text.Wrap( -1 )

        self.asr_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.asr_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        asrt_row.Add( self.asr_text, 1, wx.ALL|wx.EXPAND, 10 )

        self.asr_time = wx.StaticText( self, asrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.asr_time.Wrap( -1 )

        self.asr_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.asr_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        asrt_row.Add( self.asr_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 10 )


        bSizer8.Add( asrt_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

        maghrib_row = wx.BoxSizer( wx.HORIZONTAL )

        self.maghrib_text = wx.StaticText( self, maghribLabel, u"Maghrib", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.maghrib_text.Wrap( -1 )

        self.maghrib_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.maghrib_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        maghrib_row.Add( self.maghrib_text, 1, wx.ALL|wx.EXPAND, 10 )

        self.maghrib_time = wx.StaticText( self, maghribTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.maghrib_time.Wrap( -1 )

        self.maghrib_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.maghrib_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        maghrib_row.Add( self.maghrib_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 10 )


        bSizer8.Add( maghrib_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

        isha_row = wx.BoxSizer( wx.HORIZONTAL )

        self.isha_text = wx.StaticText( self, ishaLabel, u"Isha", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.isha_text.Wrap( -1 )

        self.isha_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.isha_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        isha_row.Add( self.isha_text, 1, wx.ALL|wx.EXPAND, 10 )

        self.isha_time = wx.StaticText( self, ishaTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.isha_time.Wrap( -1 )

        self.isha_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.isha_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        isha_row.Add( self.isha_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 10 )


        bSizer8.Add( isha_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )


        bSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel3.SetMaxSize( wx.Size( -1,100 ) )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText8 = wx.StaticText( self.m_panel3, todayDate, u"00-00-0000, 00:00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer6.Add( self.m_staticText8, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11 = wx.StaticText( self.m_panel3, nextPrayerName, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText11.Wrap( -1 )

        self.m_staticText11.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText11.SetForegroundColour( activePrayercolor )
        self.m_staticText11.SetMinSize( wx.Size( 100,-1 ) )

        bSizer71.Add( self.m_staticText11, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText101 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"after", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText101.Wrap( -1 )

        self.m_staticText101.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer71.Add( self.m_staticText101, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_staticText111 = wx.StaticText( self.m_panel3, nextPrayerTime, u"00:00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText111.Wrap( -1 )

        self.m_staticText111.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer71.Add( self.m_staticText111, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer6.Add( bSizer71, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


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
        
        self.SetTransparent(settings['trValue'])
        self.SetIcon(wx.Icon(appIcon, wx.BITMAP_TYPE_PNG))
        # Make the frame draggable
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_move)


    def on_minimize(self, event):
        if self.IsIconized():
            # hide the frame from the taskbar when minimized
            self.Hide()
        event.Skip()
        
    def on_left_down(self, event):
        # Save the window position and the mouse position
        self.CaptureMouse()
        position = self.GetPosition()
        mouse_position = wx.GetMousePosition()
        try:
            self.delta_x = mouse_position.x - position.x
            self.delta_y = mouse_position.y - position.y
        except:
            pass

    def on_left_up(self, event):
        # Release the mouse
        if self.HasCapture():
            self.ReleaseMouse()

    def on_move(self, event):
        # Move the window by the mouse delta
        try:
            if event.Dragging() and event.LeftIsDown():
                mouse_position = wx.GetMousePosition()
                new_position = (mouse_position.x - self.delta_x, mouse_position.y - self.delta_y)
                self.Move(new_position)
        except:
            pass
            
    def UpdateLayout( self ):
        self.Layout()
        
    def __del__( self ):
        pass

class Settings ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,260 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)

        self.SetSizeHints( wx.Size( 500,260 ), wx.Size( 500,260 ) )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText17.Wrap( -1 )

        self.m_staticText17.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer15.Add( self.m_staticText17, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( bSizer15, 1, wx.EXPAND, 5 )

        bSizer151 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Lat:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )

        bSizer151.Add( self.m_staticText18, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.latValue = wx.SpinCtrlDouble( self, latValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, float(settings["lat"]), 1 )
        self.latValue.SetDigits( 3 )
        bSizer151.Add( self.latValue, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.Long = wx.StaticText( self, wx.ID_ANY, u"Long:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Long.Wrap( -1 )

        bSizer151.Add( self.Long, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.LongValue = wx.SpinCtrlDouble( self, longValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, float(settings["long"]), 1 )
        self.LongValue.SetDigits( 3 )
        bSizer151.Add( self.LongValue, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.timeZone = wx.StaticText( self, wx.ID_ANY, u"TimeZone:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.timeZone.Wrap( -1 )

        bSizer151.Add( self.timeZone, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl1 = wx.SpinCtrl( self, timeZoneValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, -12, 12, int(settings["timeZone"]) )
        bSizer151.Add( self.m_spinCtrl1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( bSizer151, 1, wx.EXPAND, 5 )

        bSizer152 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Method:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )

        bSizer152.Add( self.m_staticText20, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        methodsChoices = [ u"MWL", u"ISNA", u"Egypt", u"Makkah", u"Karachi", u"Tehran", u"Jafari" ]
        self.methods = wx.Choice( self, methodValue, wx.DefaultPosition, wx.DefaultSize, methodsChoices, 0 )
        self.methods.SetSelection( methods.index(settings["method"]) )
        bSizer152.Add( self.methods, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Asr method:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )

        bSizer152.Add( self.m_staticText21, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        m_choice2Choices = [ u"Standard", u"Hanafi" ]
        self.m_choice2 = wx.Choice( self, asrValue, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices,  0)
        self.m_choice2.SetSelection( asrMethods.index(settings["asr"]) )
        bSizer152.Add( self.m_choice2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"Dhuhr:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText28.Wrap( -1 )

        bSizer152.Add( self.m_staticText28, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl2 = wx.SpinCtrl( self, dhuhrValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, int(settings["dhuhr"]) )
        bSizer152.Add( self.m_spinCtrl2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( bSizer152, 1, wx.EXPAND, 5 )

        bSizer153 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"Fajr:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )

        bSizer153.Add( self.m_staticText22, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrlDouble3 = wx.SpinCtrlDouble( self, fajrValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, float(settings["fajr"]), 0.5 )
        self.m_spinCtrlDouble3.SetDigits( 1 )
        bSizer153.Add( self.m_spinCtrlDouble3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"Deg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )

        bSizer153.Add( self.m_staticText24, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Maghrib:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText25.Wrap( -1 )

        bSizer153.Add( self.m_staticText25, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrlDouble5 = wx.SpinCtrlDouble( self, maghribValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, float(settings["maghrib"]), 1 )
        self.m_spinCtrlDouble5.SetDigits( 3 )
        bSizer153.Add( self.m_spinCtrlDouble5, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Deg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText27.Wrap( -1 )

        bSizer153.Add( self.m_staticText27, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Isha:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText23.Wrap( -1 )

        bSizer153.Add( self.m_staticText23, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrlDouble4 = wx.SpinCtrlDouble( self, ishaValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, float(settings["isha"]), 0.5 )
        self.m_spinCtrlDouble4.SetDigits( 1 )
        bSizer153.Add( self.m_spinCtrlDouble4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"Deg", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText26.Wrap( -1 )

        bSizer153.Add( self.m_staticText26, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( bSizer153, 1, wx.EXPAND, 5 )

        bSizer155 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_checkBox1 = wx.CheckBox( self, minimized, u"start minimized", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox1.SetValue(True if int(settings["minimized"]) else False)
        bSizer155.Add( self.m_checkBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, u"Transparency", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText29.Wrap( -1 )

        bSizer155.Add( self.m_staticText29, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
  
        self.m_spinCtrl3 = wx.SpinCtrl( self, trValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 500, settings["trValue"] )
        bSizer155.Add( self.m_spinCtrl3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer14.Add( bSizer155, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        bSizer154 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button1 = wx.Button( self, wx.ID_ANY, u"Default", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer154.Add( self.m_button1, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button2 = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer154.Add( self.m_button2, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer14.Add( bSizer154, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer14 )
        self.Layout()

        self.Centre( wx.BOTH )

        self.SetIcon(wx.Icon(settingsIcon, wx.BITMAP_TYPE_PNG))

        # Connect Events
        self.m_button1.Bind( wx.EVT_BUTTON, self.setDefault )
        self.m_button2.Bind( wx.EVT_BUTTON, self.saveSettings )
        
    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def setDefault( self, event ):
        slat = wx.FindWindowById(latValue)
        slong = wx.FindWindowById(longValue)
        stimeZone = wx.FindWindowById(timeZoneValue)
        smethod = wx.FindWindowById(methodValue)
        sfajr = wx.FindWindowById(fajrValue)
        sdhuhr = wx.FindWindowById(dhuhrValue)
        sasr = wx.FindWindowById(asrValue)
        smaghrib = wx.FindWindowById(maghribValue)
        sisha = wx.FindWindowById(ishaValue)
        sminimized = wx.FindWindowById(minimized)
        strValue = wx.FindWindowById(trValue)
        settings["lat"] = defaultSettings["lat"]
        settings["long"] = defaultSettings["long"]
        settings["timeZone"] = defaultSettings["timeZone"]
        settings["method"] = defaultSettings["method"]
        settings["fajr"] = defaultSettings["fajr"]
        settings["dhuhr"] = defaultSettings["dhuhr"]
        settings["asr"] = defaultSettings["asr"]
        settings["maghrib"] = defaultSettings["maghrib"]
        settings["isha"] = defaultSettings["isha"]
        settings["minimized"] = defaultSettings["minimized"]
        settings["strValue"] = defaultSettings["trValue"]
        # print(slat)
        slat.SetValue(float(defaultSettings["lat"]))
        slong.SetValue(float(defaultSettings["long"]))
        stimeZone.SetValue(defaultSettings["timeZone"])
        smethod.SetSelection(methods.index(defaultSettings["method"]))
        sfajr.SetValue(float(defaultSettings["fajr"]))
        sdhuhr.SetValue(defaultSettings["dhuhr"])
        sasr.SetSelection(asrMethods.index(defaultSettings["asr"]))
        smaghrib.SetValue(defaultSettings["maghrib"])
        sisha.SetValue(float(defaultSettings["isha"]))
        sminimized.SetValue(defaultSettings["minimized"])
        strValue.SetValue(defaultSettings["trValue"])

    def saveSettings( self, event ):
        slat = wx.FindWindowById(latValue)
        slong = wx.FindWindowById(longValue)
        stimeZone = wx.FindWindowById(timeZoneValue)
        smethod = wx.FindWindowById(methodValue)
        sfajr = wx.FindWindowById(fajrValue)
        sdhuhr = wx.FindWindowById(dhuhrValue)
        sasr = wx.FindWindowById(asrValue)
        smaghrib = wx.FindWindowById(maghribValue)
        sisha = wx.FindWindowById(ishaValue)
        sminimized = wx.FindWindowById(minimized)
        strValue = wx.FindWindowById(trValue)

        settings["lat"] = slat.GetValue()
        settings["long"] = slong.GetValue()
        settings["timeZone"] = stimeZone.GetValue()
        settings["method"] = methods[smethod.GetSelection()]
        settings["fajr"] = sfajr.GetValue()
        settings["dhuhr"] = sdhuhr.GetValue()
        settings["asr"] = asrMethods[sasr.GetSelection()]
        settings["maghrib"] = smaghrib.GetValue()
        settings["isha"] = sisha.GetValue()
        settings["trValue"] = strValue.GetValue()
        settings["minimized"] = 1 if sminimized.GetValue() else 0
        with open(appdataFile, 'w') as file:
            json.dump(settings, file)
        setTr(settings['trValue'])
       

def formatPrayerDate(prayer):
    nowDate = datetime.now()
    prayerTxt = str(prayer).split(":")
    hour = int(prayerTxt[0])
    minute = int(prayerTxt[1])
    formatedDate = nowDate.replace(
        hour=hour, minute=minute).strftime("%I:%M %p")
    # print(formatedDate)
    return formatedDate


def nextPrayer():
    now = datetime.now()
    pTimes = getPrayerTimes()
    prayers = [pTimes["fajr"], pTimes["dhuhr"],
               pTimes["asr"], pTimes["maghrib"], pTimes["isha"]]
    nowHrMn = now.strftime("%H:%M")
    prayers.append(str(nowHrMn))
    sortedTimes = sorted(prayers)
    prayerIndex = sortedTimes.index(str(nowHrMn))
    if prayerIndex > 4:
        prayerIndex = 0
    return prayerIndex


def getPrayerTimes(index=1):
    now = datetime.now()
    hour = now.strftime("%H")
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%m"))
    day = int(now.strftime("%d"))
    pT = PrayTimes("Egypt")
    s_dhuhr = settings["dhuhr"]
    pT.adjust({"fajr": settings["fajr"], "dhuhr": f"{s_dhuhr} min",
              "asr": settings["asr"], "maghrib": settings["maghrib"], "isha": settings["isha"]})
    if not index and int(hour) > 12:
        try:
            datetime(year,month,day+1)
            prayerTimesList = pT.getTimes([year, month, day+1], [float(settings["lat"]), float(settings["long"])], settings["timeZone"])
        except:
            try:
                datetime(year,month+1,1)
                prayerTimesList = pT.getTimes([year, month+1, 1], [float(settings["lat"]), float(settings["long"])], settings["timeZone"])
            except:
                prayerTimesList = pT.getTimes([year+1, 1, 1], [float(settings["lat"]), float(settings["long"])], settings["timeZone"])
    else:
        prayerTimesList = pT.getTimes([year, month, day], [float(settings["lat"]), float(settings["long"])], settings["timeZone"])
    return prayerTimesList


def calcNextPrayer(prayer,index):
    d1 = datetime.now()
    d1h = d1.strftime("%H")
    d1m = d1.strftime("%M")
    d1s = d1.strftime("%S")
    totalSec1 = int(d1h)*60*60+int(d1m)*60+int(d1s)
    prayerTxt = str(prayer).split(":")
    d2h = int(prayerTxt[0])
    d2m = int(prayerTxt[1])
    d2s = 0
    totalSec2 = int(d2h)*60*60+int(d2m)*60+int(d2s)
    if not index and int(d1h) > 12:
        difSec = secondsInDay-abs(totalSec1-totalSec2)
    else:
        difSec = abs(totalSec1-totalSec2)
    timeLeft = str(timedelta(seconds=(difSec)))
    return timeLeft

class MyTaskBarIcon(TaskBarIcon):
    def __init__(self, frame,app):
        TaskBarIcon.__init__(self)
        self.frame = frame
        self.app = app
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.autoUpdate)
        self.timer.Start(1000) # update every second
        self.SetIcon(wx.Icon(appIcon, wx.BITMAP_TYPE_PNG), 'Loading...')
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_MENU, self.ExitApp, id=2)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=1)
         
    def CreatePopupMenu(self):
         menu = wx.Menu()
         menu.Append(1, 'Settings')
         menu.Append(2, 'Exit')
         return menu
 
    def OnDoubleClick(self, event):
        if not self.frame.IsShown():
             self.frame.Show()
        else:
             self.frame.Hide()
    
    def OnSettings(self,event):
        settingsFrame = Settings(None)
        settingsFrame.Show()
        
    def ExitApp(self, event):
        # Exit the application cleanly
        self.RemoveIcon()
        # Close any open windows
        self.frame.Close(True)
        self.app.ExitMainLoop()
        self.app.Destroy()
             
    def autoUpdate(self, event):
        calcPrayerTimes()
        fajrCtrl =  wx.FindWindowById(fajrTime).GetLabel()
        dhuhrCtrl =  wx.FindWindowById(dhuhrTime).GetLabel()
        asrCtrl =  wx.FindWindowById(asrTime).GetLabel()
        maghribCtrl =  wx.FindWindowById(maghribTime).GetLabel()
        ishaCtrl =  wx.FindWindowById(ishaTime).GetLabel()
        nextPrayerText =  wx.FindWindowById(nextPrayerName).GetLabel()
        nextPrayerLeft =  wx.FindWindowById(nextPrayerTime).GetLabel()
        l1 = f"fajr:  {fajrCtrl}"
        l2 = f"duhr:  {dhuhrCtrl}"
        l3 = f"asr:  {asrCtrl}"
        l4 = f"maghrib  {maghribCtrl}"
        l5 = f"isha:  {ishaCtrl}"
        l6 = f"{nextPrayerText} is after {nextPrayerLeft}"
        tooltip = f"{l1}\n{l2}\n{l3}\n{l4}\n{l5}\n\n{l6}"
        self.SetIcon(wx.Icon(appIcon), tooltip)


def calcPrayerTimes():
            now = datetime.now()
            nexPrayerIndex = nextPrayer()
            pTimes = getPrayerTimes(nexPrayerIndex)
            fajr = formatPrayerDate(pTimes["fajr"])
            dhuhr = formatPrayerDate(pTimes["dhuhr"])
            asr = formatPrayerDate(pTimes["asr"])
            maghrib = formatPrayerDate(pTimes["maghrib"])
            isha = formatPrayerDate(pTimes["isha"])
            nextprayer = prayersList[nexPrayerIndex]
            TimeCtrl = wx.FindWindowById(todayDate)
            nextPrayerText = wx.FindWindowById(nextPrayerName)
            nextPrayerLeft = wx.FindWindowById(nextPrayerTime)
            # prayer times
            fajrCtrl = wx.FindWindowById(fajrTime)
            fajrLbl = wx.FindWindowById(fajrLabel)
            
            dhuhrCtrl = wx.FindWindowById(dhuhrTime)
            dhuhrLbl = wx.FindWindowById(dhuhrLabel)
            
            asrCtrl = wx.FindWindowById(asrTime)
            asrLbl = wx.FindWindowById(asrLabel)
            
            maghribCtrl = wx.FindWindowById(maghribTime)
            maghribLbl = wx.FindWindowById(maghribLabel)
            
            ishaCtrl = wx.FindWindowById(ishaTime)
            ishaLbl = wx.FindWindowById(ishaLabel)
            # setColor
            fajrCtrl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 0 else wx.BLACK)
            fajrLbl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 0 else wx.BLACK)
            
            dhuhrCtrl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 1 else wx.BLACK)
            dhuhrLbl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 1 else wx.BLACK)
            
            asrCtrl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 2 else wx.BLACK)
            asrLbl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 2 else wx.BLACK)
            
            maghribCtrl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 3 else wx.BLACK)
            maghribLbl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 3 else wx.BLACK)
            
            ishaCtrl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 4 else wx.BLACK)
            ishaLbl.SetForegroundColour(activePrayercolor if nexPrayerIndex == 4 else wx.BLACK)
            # setLabel
            fajrCtrl.SetLabel(fajr)
            dhuhrCtrl.SetLabel(dhuhr)
            asrCtrl.SetLabel(asr)
            maghribCtrl.SetLabel(maghrib)
            ishaCtrl.SetLabel(isha)
            TimeCtrl.SetLabel(str((now.strftime("%d-%m-%Y, %I:%M:%S %p"))))
            leftTilNextPrayer = (calcNextPrayer(pTimes[prayersList[nexPrayerIndex]],nexPrayerIndex))
            nextPrayerText.SetLabel(f"{nextprayer}")
            nextPrayerLeft.SetLabel(f"{leftTilNextPrayer}")
            Rpccallfunction(nexPrayerIndex)

def playAudio():
    mixer.init()
    mixer.music.load(audioFile)
    mixer.music.play()
 
if __name__ == '__main__':
    wx.SizerFlags.DisableConsistencyChecks()
    app = wx.App(False) 
    frame = MyDialog1(None) 
    def Rpccallfunction(val): 
            wx.CallAfter( frame.UpdateLayout ) 
    def setTr(val): 
              frame.SetTransparent(val)
    if not settings["minimized"]:
        frame.Show(True) 
    MyTaskBarIcon(frame,app)
    playAudio()
    app.MainLoop() 