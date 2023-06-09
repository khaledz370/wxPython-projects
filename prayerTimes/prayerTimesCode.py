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
import json
from tendo import singleton

me = singleton.SingleInstance()

fajrTime = 1000
dhuhrTime = 1001
asrTime = 1002
maghribTime = 1003
ishaTime = 1004
todayDate = 1005
nextPrayerName = 1006
nextPrayerTime = 1007

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
    print('load settings from config')
except:
    settings = defaultSettings
    with open(appdataFile, 'w') as file:
        json.dump(defaultSettings, file)
    print("Load default settings")    

        

        
        self.SetTransparent(150)
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
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        self.frame = frame
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
        # Schedule the release of resources and exit of main loop on the event loop
        wx.CallAfter(self.ReleaseResources)

    def ReleaseResources(self):
        # Release resources associated with the wx.App object
        wx.GetApp().ExitMainLoop()
        wx.GetApp().Destroy()
        # Exit the Python interpreter (optional)
        sys.exit()
             
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
            fajrCtrl =  wx.FindWindowById(fajrTime)
            dhuhrCtrl =  wx.FindWindowById(dhuhrTime)
            asrCtrl =  wx.FindWindowById(asrTime)
            maghribCtrl =  wx.FindWindowById(maghribTime)
            ishaCtrl =  wx.FindWindowById(ishaTime)
            TimeCtrl =  wx.FindWindowById(todayDate)
            nextPrayerText =  wx.FindWindowById(nextPrayerName)
            nextPrayerLeft =  wx.FindWindowById(nextPrayerTime)
            fajrCtrl.SetLabel(fajr)
            dhuhrCtrl.SetLabel(dhuhr)
            asrCtrl.SetLabel(asr)
            maghribCtrl.SetLabel(maghrib)
            ishaCtrl.SetLabel(isha)
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
    MyTaskBarIcon(frame)
    app.MainLoop() 