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
from threading import Timer
from praytimes import PrayTimes
from datetime import datetime, timedelta
from psgtray import SystemTray
from playsound import playsound
import os
import sys
import json
from tendo import singleton

me = singleton.SingleInstance()

fajrLabel = 1000
dhuhrLabel = 1001
asrLabel = 1002
maghribLabel = 1003
ishaLabel = 1004
fajrTime = 1005
dhuhrTime = 1006
asrTime = 1007
maghribTime = 1008
ishaTime = 1009
todayDate = 1010
nextPrayerName = 1011
nextPrayerTime = 1012

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
defaultSettings = {'lat': '29.9', 'long': '31.2', 'timeZone': 2, 'method': 'EGYPT', 'fajr': '19.5', 'dhuhr': '0',
                   'asr': 'Standard', 'maghrib': '1', 'isha': '17.5', 'minimized': 1}
appdataFolder = f"{os.getenv('APPDATA')}\prayerTimes"
appdataFile = f"{appdataFolder}\config.json"
appdataFolder = f"{os.getenv('APPDATA')}\prayerTimes"
appdataFile = f"{appdataFolder}\config.json"

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
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 348,414 ), style = 0 )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Prayer times", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        self.m_staticText1.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText3 = wx.StaticText( self, fajrLabel, u"Fajr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        self.m_staticText3.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer3.Add( self.m_staticText3, 1, wx.ALL, 10 )

        self.m_staticText4 = wx.StaticText( self, dhuhrLabel, u"Dhuhr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer3.Add( self.m_staticText4, 1, wx.ALL, 10 )

        self.m_staticText5 = wx.StaticText( self, asrLabel, u"Asr", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        self.m_staticText5.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer3.Add( self.m_staticText5, 1, wx.ALL, 10 )

        self.m_staticText6 = wx.StaticText( self, maghribLabel, u"Maghrib", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        self.m_staticText6.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText6.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer3.Add( self.m_staticText6, 1, wx.ALL, 10 )

        self.m_staticText7 = wx.StaticText( self, ishaLabel, u"Isha", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        self.m_staticText7.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText7.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer3.Add( self.m_staticText7, 1, wx.ALL, 10 )


        bSizer8.Add( bSizer3, 1, wx.EXPAND|wx.LEFT, 20 )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText14 = wx.StaticText( self, fajrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )

        self.m_staticText14.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText14.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer5.Add( self.m_staticText14, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )

        self.m_staticText141 = wx.StaticText( self, dhuhrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText141.Wrap( -1 )

        self.m_staticText141.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText141.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer5.Add( self.m_staticText141, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )

        self.m_staticText142 = wx.StaticText( self, asrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText142.Wrap( -1 )

        self.m_staticText142.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText142.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer5.Add( self.m_staticText142, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )

        self.m_staticText144 = wx.StaticText( self, maghribTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText144.Wrap( -1 )

        self.m_staticText144.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText144.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer5.Add( self.m_staticText144, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )

        self.m_staticText143 = wx.StaticText( self, ishaTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText143.Wrap( -1 )

        self.m_staticText143.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText143.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        bSizer5.Add( self.m_staticText143, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10 )


        bSizer8.Add( bSizer5, 1, wx.EXPAND, 20 )


        bSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel3.SetMaxSize( wx.Size( -1,100 ) )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText8 = wx.StaticText( self.m_panel3, todayDate, u"00-00-0000, 00:00:00", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer6.Add( self.m_staticText8, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11 = wx.StaticText( self.m_panel3, nextPrayerName, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText11.Wrap( -1 )

        self.m_staticText11.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText11.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
        self.m_staticText11.SetMinSize( wx.Size( 100,-1 ) )

        bSizer71.Add( self.m_staticText11, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText101 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"after", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText101.Wrap( -1 )

        self.m_staticText101.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer71.Add( self.m_staticText101, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText111 = wx.StaticText( self.m_panel3, nextPrayerTime, u"00:00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText111.Wrap( -1 )

        self.m_staticText111.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer71.Add( self.m_staticText111, 0, wx.ALL, 5 )


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

        
        self.SetTransparent(500)
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
        
    def __del__( self ):
        pass


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
    # print(prayers)
    prayers.append(str(nowHrMn))
    sortedTimes = sorted(prayers)
    prayerIndex = sortedTimes.index(str(nowHrMn))
    # print(prayerIndex)
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
    # print(prayer)
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
        self.Bind(wx.EVT_TIMER, self.OnUpdateIcon)
        self.timer.Start(1000) # update every second
        self.SetIcon(wx.Icon(f"{os.path.dirname(__file__)}\\resources\img\prayertimes.png", wx.BITMAP_TYPE_PNG), 'Task bar icon')
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
        print()
        
    def ExitApp(self, event):
        # Exit the application cleanly
        self.RemoveIcon()
        # Close any open windows
        self.frame.Close(True)
        self.app.ExitMainLoop()
        self.app.Destroy()
             
    def OnUpdateIcon(self, event):
        # update the tooltip text with current time
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
        self.SetIcon(wx.Icon(f"{os.path.dirname(__file__)}\\resources\img\prayertimes.png"), tooltip)


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
            # prayer labels
            fajrLbl = wx.FindWindowById(fajrLabel)
            dhuhrLbl = wx.FindWindowById(dhuhrLabel)
            asrLbl = wx.FindWindowById(asrLabel)
            maghribLbl = wx.FindWindowById(maghribLabel)
            ishaLbl = wx.FindWindowById(ishaLabel)
            # prayer times
            fajrCtrl = wx.FindWindowById(fajrTime)
            dhuhrCtrl = wx.FindWindowById(dhuhrTime)
            asrCtrl = wx.FindWindowById(asrTime)
            maghribCtrl = wx.FindWindowById(maghribTime)
            ishaCtrl = wx.FindWindowById(ishaTime)
            # setColor
            fajrLbl.SetForegroundColour(wx.Colour(255,0,0) if nexPrayerIndex == 0 else wx.BLACK)
            dhuhrLbl.SetForegroundColour(wx.Colour(255,0,0) if nexPrayerIndex == 1 else wx.BLACK)
            asrLbl.SetForegroundColour(wx.Colour(255,0,0) if nexPrayerIndex == 2 else wx.BLACK)
            maghribLbl.SetForegroundColour(wx.Colour(255,0,0) if nexPrayerIndex == 3 else wx.BLACK)
            ishaLbl.SetForegroundColour(wx.Colour(255,0,0) if nexPrayerIndex == 4 else wx.BLACK)
            # set label color
            fajrCtrl.SetForegroundColour(fajrLbl.GetForegroundColour())
            dhuhrCtrl.SetForegroundColour(dhuhrLbl.GetForegroundColour())
            asrCtrl.SetForegroundColour(asrLbl.GetForegroundColour())
            maghribCtrl.SetForegroundColour(maghribLbl.GetForegroundColour())
            ishaCtrl.SetForegroundColour(ishaLbl.GetForegroundColour())                  
            # setLabel
            fajrCtrl.SetLabel(fajr)
            dhuhrCtrl.SetLabel(dhuhr)
            asrCtrl.SetLabel(asr)
            maghribCtrl.SetLabel(maghrib)
            ishaCtrl.SetLabel(isha)
            
            # fajrLbl.SetLabel("Fajr")
            # dhuhrLbl.SetLabel("Dhuhr")
            # asrLbl.SetLabel("Asr")
            # maghribLbl.SetLabel("Maghrib")
            # ishaLbl.SetLabel("Isha")
            
            TimeCtrl.SetLabel(str((now.strftime("%d-%m-%Y, %I:%M:%S %p"))))
            leftTilNextPrayer = (calcNextPrayer(pTimes[prayersList[nexPrayerIndex]],nexPrayerIndex))
            nextPrayerText.SetLabel(f"{nextprayer}")
            nextPrayerLeft.SetLabel(f"{leftTilNextPrayer}")
            counterId = Timer(1.0, calcPrayerTimes)
            settings["thread"] = counterId
            counterId.start()
            counterId = ""
Timer(1.0, calcPrayerTimes).start()

if __name__ == '__main__':
    wx.SizerFlags.DisableConsistencyChecks()
    app = wx.App(False) 
    frame = MyDialog1(None) 
    frame.Show(True) 
    MyTaskBarIcon(frame,app)
    app.MainLoop() 