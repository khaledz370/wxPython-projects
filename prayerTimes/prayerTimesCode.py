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
         if not self.frame.IsShown():
             self.frame.Show()
 
 
     def OnTaskBarDeactivate(self, event):
         if self.frame.IsShown():
             self.frame.Hide()

wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False) 
frame = MyDialog1(None) 
frame.Show(True) 
app.MainLoop() 