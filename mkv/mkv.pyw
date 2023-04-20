# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-282-g1fa54006)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import os
import subprocess
import sys
import shutil

selectedFilesToMkv = 1000
browseFilesToMkv = 1001
browseFolderToMkv = 1002
selectAllToMkv = 1003
dBtnToMkv = 1004
fileTypesToMkv = 1005
allToMkv = 1006
convertToMkv = 1007
currentFileToMkv = 1008
pBarToMkv = 1009
selectedFilesToAudio = 1010
browseFilesToAudio = 1011
browseFolderToAudio = 1012
selectAllToAudio = 1013
dBtnToAudio = 1014
fileTypesToAudio = 1015
allToAudio = 1016
convertToAudio = 1017
currentFileToAudio = 1018
pBarToAudio = 1019
selectedFilesCrop = 1020
browseFilesCrop = 1021
browseFolderCrop = 1022
selectAllCrop = 1023
dBtnCrop = 1024
fileTypesCrop = 1025
allCrop = 1026
cTop = 1027
cRight = 1028
cBottom = 1029
cLeft = 1030
cropVideo = 1031
currentFileCrop = 1032
pBarCrop = 1033
true = True
defaultfileTypesList = [".mkv" ,".ts" ,".mp4" ,".avi" ,".webm" ,".flv" ,".ogg" ,".mov" ,".mpeg-2"]
mkvMerge = "C:\Program Files\MKVToolNix\mkvmerge.exe"
mkvpropedit = "C:\Program Files\MKVToolNix\mkvpropedit.exe"

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 760,480 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 760,480 ), wx.Size( 760,480 ) )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook30 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.tomkv = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText3 = wx.StaticText( self.tomkv, wx.ID_ANY, u"Convert video to mkv", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        bSizer4.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel20 = wx.Panel( self.tomkv, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel7 = wx.Panel( self.m_panel20, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel8 = wx.Panel( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel71 = wx.Panel( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

        m_checkList1Choices = []
        self.m_checkList1 = wx.CheckListBox( self.m_panel71, selectedFilesToMkv, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList1Choices, 0 )
        self.m_checkList1.DragAcceptFiles( true )

        bSizer81.Add( self.m_checkList1, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel9 = wx.Panel( self.m_panel71, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer71 = wx.BoxSizer( wx.VERTICAL )

        self.m_button3 = wx.Button( self.m_panel9, browseFilesToMkv, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button11 = wx.Button( self.m_panel9, browseFolderToMkv, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button11, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button15 = wx.Button( self.m_panel9, selectAllToMkv, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button15, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button111 = wx.Button( self.m_panel9, dBtnToMkv, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


        self.m_panel9.SetSizer( bSizer71 )
        self.m_panel9.Layout()
        bSizer71.Fit( self.m_panel9 )
        bSizer81.Add( self.m_panel9, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_panel81 = wx.Panel( self.m_panel71, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        m_checkList11Choices = [u"mkv", u"ts", u"mp4", u"avi", u"webm", u"flv", u"ogg", u"mov", u"mpeg-2"]
        self.m_checkList11 = wx.CheckListBox( self.m_panel81, fileTypesToMkv, wx.DefaultPosition, wx.DefaultSize, m_checkList11Choices, 0 )
        self.m_checkList11.DragAcceptFiles( true )

        bSizer9.Add( self.m_checkList11, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button7 = wx.Button( self.m_panel81, allToMkv, u"check all", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
        bSizer9.Add( self.m_button7, 0, wx.ALL, 5 )


        self.m_panel81.SetSizer( bSizer9 )
        self.m_panel81.Layout()
        bSizer9.Fit( self.m_panel81 )
        bSizer81.Add( self.m_panel81, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel71.SetSizer( bSizer81 )
        self.m_panel71.Layout()
        bSizer81.Fit( self.m_panel71 )
        bSizer8.Add( self.m_panel71, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel8.SetSizer( bSizer8 )
        self.m_panel8.Layout()
        bSizer8.Fit( self.m_panel8 )
        bSizer5.Add( self.m_panel8, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 5 )


        self.m_panel7.SetSizer( bSizer5 )
        self.m_panel7.Layout()
        bSizer5.Fit( self.m_panel7 )
        bSizer7.Add( self.m_panel7, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel20.SetSizer( bSizer7 )
        self.m_panel20.Layout()
        bSizer7.Fit( self.m_panel20 )
        bSizer6.Add( self.m_panel20, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button9 = wx.Button( self.tomkv, convertToMkv, u"Convert to mkv", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer12.Add( self.m_button9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText31 = wx.StaticText( self.tomkv, currentFileToMkv, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        self.m_staticText31.Wrap( -1 )

        bSizer12.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer11.Add( bSizer12, 1, wx.EXPAND, 5 )

        self.m_gauge1 = wx.Gauge( self.tomkv, pBarToMkv, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue( 0 )
        bSizer11.Add( self.m_gauge1, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer6.Add( bSizer11, 1, wx.EXPAND, 5 )


        bSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )


        self.tomkv.SetSizer( bSizer4 )
        self.tomkv.Layout()
        bSizer4.Fit( self.tomkv )
        self.m_notebook30.AddPage( self.tomkv, u"to mkv", True )
        self.toAudio = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer41 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText32 = wx.StaticText( self.toAudio, wx.ID_ANY, u"Convert video to audio", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText32.Wrap( -1 )

        bSizer41.Add( self.m_staticText32, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel201 = wx.Panel( self.toAudio, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer72 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel72 = wx.Panel( self.m_panel201, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer51 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel82 = wx.Panel( self.m_panel72, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        bSizer82 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel711 = wx.Panel( self.m_panel82, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer811 = wx.BoxSizer( wx.HORIZONTAL )

        m_checkList12Choices = []
        self.m_checkList12 = wx.CheckListBox( self.m_panel711, selectedFilesToAudio, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList12Choices, 0 )
        self.m_checkList12.DragAcceptFiles( true )

        bSizer811.Add( self.m_checkList12, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel91 = wx.Panel( self.m_panel711, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer711 = wx.BoxSizer( wx.VERTICAL )

        self.m_button31 = wx.Button( self.m_panel91, browseFilesToAudio, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button112 = wx.Button( self.m_panel91, browseFolderToAudio, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button112, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button151 = wx.Button( self.m_panel91, selectAllToAudio, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button151, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button1111 = wx.Button( self.m_panel91, dBtnToAudio, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button1111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


        self.m_panel91.SetSizer( bSizer711 )
        self.m_panel91.Layout()
        bSizer711.Fit( self.m_panel91 )
        bSizer811.Add( self.m_panel91, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_panel811 = wx.Panel( self.m_panel711, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer91 = wx.BoxSizer( wx.VERTICAL )

        m_checkList111Choices = [u"mkv", u"ts", u"mp4", u"avi", u"webm", u"flv", u"ogg", u"mov", u"mpeg-2"]
        self.m_checkList111 = wx.CheckListBox( self.m_panel811, fileTypesToAudio, wx.DefaultPosition, wx.DefaultSize, m_checkList111Choices, 0 )
        self.m_checkList111.DragAcceptFiles( true )

        bSizer91.Add( self.m_checkList111, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button71 = wx.Button( self.m_panel811, allToAudio, u"check all", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
        bSizer91.Add( self.m_button71, 0, wx.ALL, 5 )


        self.m_panel811.SetSizer( bSizer91 )
        self.m_panel811.Layout()
        bSizer91.Fit( self.m_panel811 )
        bSizer811.Add( self.m_panel811, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel711.SetSizer( bSizer811 )
        self.m_panel711.Layout()
        bSizer811.Fit( self.m_panel711 )
        bSizer82.Add( self.m_panel711, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel82.SetSizer( bSizer82 )
        self.m_panel82.Layout()
        bSizer82.Fit( self.m_panel82 )
        bSizer51.Add( self.m_panel82, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 5 )


        self.m_panel72.SetSizer( bSizer51 )
        self.m_panel72.Layout()
        bSizer51.Fit( self.m_panel72 )
        bSizer72.Add( self.m_panel72, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel201.SetSizer( bSizer72 )
        self.m_panel201.Layout()
        bSizer72.Fit( self.m_panel201 )
        bSizer61.Add( self.m_panel201, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer111 = wx.BoxSizer( wx.VERTICAL )

        bSizer121 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button91 = wx.Button( self.toAudio, convertToAudio, u"Convert to audio", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer121.Add( self.m_button91, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText311 = wx.StaticText( self.toAudio, currentFileToAudio, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        self.m_staticText311.Wrap( -1 )

        bSizer121.Add( self.m_staticText311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer111.Add( bSizer121, 1, wx.EXPAND, 5 )

        self.m_gauge11 = wx.Gauge( self.toAudio, pBarToAudio, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge11.SetValue( 0 )
        bSizer111.Add( self.m_gauge11, 0, wx.EXPAND|wx.ALL, 5 )


        bSizer61.Add( bSizer111, 1, wx.EXPAND, 5 )


        bSizer41.Add( bSizer61, 1, wx.EXPAND, 5 )


        self.toAudio.SetSizer( bSizer41 )
        self.toAudio.Layout()
        bSizer41.Fit( self.toAudio )
        self.m_notebook30.AddPage( self.toAudio, u"toAudio", False )
        self.crop = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer411 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText321 = wx.StaticText( self.crop, wx.ID_ANY, u"crop video", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText321.Wrap( -1 )

        bSizer411.Add( self.m_staticText321, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        bSizer611 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel2011 = wx.Panel( self.crop, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer721 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel721 = wx.Panel( self.m_panel2011, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer511 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel821 = wx.Panel( self.m_panel721, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        bSizer821 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel7111 = wx.Panel( self.m_panel821, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer8111 = wx.BoxSizer( wx.HORIZONTAL )

        m_checkList121Choices = []
        self.m_checkList121 = wx.CheckListBox( self.m_panel7111, selectedFilesCrop, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList121Choices, 0 )
        self.m_checkList121.DragAcceptFiles( true )

        bSizer8111.Add( self.m_checkList121, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel911 = wx.Panel( self.m_panel7111, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer7111 = wx.BoxSizer( wx.VERTICAL )

        self.m_button311 = wx.Button( self.m_panel911, browseFilesCrop, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button1121 = wx.Button( self.m_panel911, browseFolderCrop, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button1121, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button1511 = wx.Button( self.m_panel911, selectAllCrop, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button1511, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button11111 = wx.Button( self.m_panel911, dBtnCrop, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button11111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


        self.m_panel911.SetSizer( bSizer7111 )
        self.m_panel911.Layout()
        bSizer7111.Fit( self.m_panel911 )
        bSizer8111.Add( self.m_panel911, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_panel8111 = wx.Panel( self.m_panel7111, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer911 = wx.BoxSizer( wx.VERTICAL )

        m_checkList1111Choices = [u"mkv", u"ts", u"mp4", u"avi", u"webm", u"flv", u"ogg", u"mov", u"mpeg-2"]
        self.m_checkList1111 = wx.CheckListBox( self.m_panel8111, fileTypesCrop, wx.DefaultPosition, wx.DefaultSize, m_checkList1111Choices, 0 )
        self.m_checkList1111.DragAcceptFiles( true )

        bSizer911.Add( self.m_checkList1111, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button711 = wx.Button( self.m_panel8111, allCrop, u"check all", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
        bSizer911.Add( self.m_button711, 0, wx.ALL, 5 )


        self.m_panel8111.SetSizer( bSizer911 )
        self.m_panel8111.Layout()
        bSizer911.Fit( self.m_panel8111 )
        bSizer8111.Add( self.m_panel8111, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel7111.SetSizer( bSizer8111 )
        self.m_panel7111.Layout()
        bSizer8111.Fit( self.m_panel7111 )
        bSizer821.Add( self.m_panel7111, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel821.SetSizer( bSizer821 )
        self.m_panel821.Layout()
        bSizer821.Fit( self.m_panel821 )
        bSizer511.Add( self.m_panel821, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 5 )


        self.m_panel721.SetSizer( bSizer511 )
        self.m_panel721.Layout()
        bSizer511.Fit( self.m_panel721 )
        bSizer721.Add( self.m_panel721, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer43 = wx.BoxSizer( wx.VERTICAL )


        bSizer721.Add( bSizer43, 1, wx.EXPAND, 5 )


        self.m_panel2011.SetSizer( bSizer721 )
        self.m_panel2011.Layout()
        bSizer721.Fit( self.m_panel2011 )
        bSizer611.Add( self.m_panel2011, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer1111 = wx.BoxSizer( wx.VERTICAL )

        bSizer46 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText15 = wx.StaticText( self.crop, wx.ID_ANY, u"Top", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        bSizer46.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_textCtrl2 = wx.TextCtrl( self.crop, cTop, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer46.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText16 = wx.StaticText( self.crop, wx.ID_ANY, u"Right", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )

        bSizer46.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_textCtrl3 = wx.TextCtrl( self.crop, cRight, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer46.Add( self.m_textCtrl3, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText17 = wx.StaticText( self.crop, wx.ID_ANY, u"Bottom", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )

        bSizer46.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_textCtrl4 = wx.TextCtrl( self.crop, cBottom, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer46.Add( self.m_textCtrl4, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText18 = wx.StaticText( self.crop, wx.ID_ANY, u"Left", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )

        bSizer46.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_textCtrl5 = wx.TextCtrl( self.crop, cLeft, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer46.Add( self.m_textCtrl5, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer1111.Add( bSizer46, 1, wx.EXPAND, 5 )

        bSizer1211 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button911 = wx.Button( self.crop, cropVideo, u"Crop", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer1211.Add( self.m_button911, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText3111 = wx.StaticText( self.crop, currentFileCrop, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3111.Wrap( -1 )

        bSizer1211.Add( self.m_staticText3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer1111.Add( bSizer1211, 1, wx.EXPAND, 5 )

        self.m_gauge111 = wx.Gauge( self.crop, pBarCrop, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge111.SetValue( 0 )
        bSizer1111.Add( self.m_gauge111, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer611.Add( bSizer1111, 1, wx.EXPAND, 5 )


        bSizer411.Add( bSizer611, 1, wx.EXPAND, 5 )


        self.crop.SetSizer( bSizer411 )
        self.crop.Layout()
        bSizer411.Fit( self.crop )
        self.m_notebook30.AddPage( self.crop, u"crop", False )

        bSizer2.Add( self.m_notebook30, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()


        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button3.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToMkv") )
        self.m_button11.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToMkv") )
        self.m_button15.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToMkv") )
        self.m_button111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("ToMkv") )
        self.m_button7.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("ToMkv") )
        self.m_button9.Bind( wx.EVT_BUTTON, self.convertToMkv )
        self.m_button31.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToAudio") )
        self.m_button112.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToAudio") )
        self.m_button151.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToAudio") )
        self.m_button1111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("ToAudio") )
        self.m_button71.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("ToAudio") )
        self.m_button91.Bind( wx.EVT_BUTTON, self.convertToAudio )
        self.m_button311.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("Crop") )
        self.m_button1121.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("Crop") )
        self.m_button1511.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("Crop") )
        self.m_button11111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("Crop") )
        self.m_button711.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("Crop") )
        self.m_button911.Bind( wx.EVT_BUTTON, self.cropVideo )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def deleteFromList( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        allFilesInCheckBoxList = checkBoxListWindow.GetItems()
        selectedFilesFromList = checkBoxListWindow.GetCheckedStrings()
        newList = list(filter(lambda file:str(file) not in selectedFilesFromList,allFilesInCheckBoxList))
        checkBoxListWindow.SetItems(newList)

    def openFilesSelector( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        openFileDialog = wx.FileDialog(self, "Select files", "", "", "All files (*.*)|*.*",
           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE)
        openFileDialog.ShowModal()
        checkBoxListWindow.Set(openFileDialog.GetFilenames())
        openFileDialog.Destroy()

    def selectFolder( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        fileTypes = eval(f"fileTypes{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        fileTypesList = wx.FindWindowById(fileTypes)
        openDirDialog = wx.DirDialog(self, "Choose folder",style=wx.DD_DIR_MUST_EXIST)
        openDirDialog.ShowModal()
        selectedDir = openDirDialog.GetPath()
        filesInDir = os.listdir(selectedDir)
        absFilesInDir = [f"{selectedDir}\\" + x for x in filesInDir]
        selectedFileTypes = fileTypesList.GetCheckedStrings()
        # print(selectedFileTypes)
        if not len(selectedFileTypes):
            selectedFileTypes = tuple(defaultfileTypesList)
        filterFilesInDir = list(filter(lambda file: str(file).endswith(selectedFileTypes),absFilesInDir))
        checkBoxListWindow.Set(filterFilesInDir)
        # print(filterFilesInDir)

        # self.m_checkList1.Set(openFileDialog.GetFilenames())
        openDirDialog.Destroy()


    def selectAll( self, event ):
        selectAll = eval(f"selectAll{event}")
        selectedFiles = eval(f"selectedFiles{event}")
        thisButton = wx.FindWindowById(selectAll)
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        indexes = checkBoxListWindow.GetCount()
        selectedItems = checkBoxListWindow.GetCheckedItems()
        if indexes and indexes != len(selectedItems):
            checkBoxListWindow.SetCheckedItems(range(indexes))
            thisButton.SetLabel("Select none")
        else:
            checkBoxListWindow.SetCheckedItems([])
            thisButton.SetLabel("Select all")

    def checkAllTypes( self, event ):
        fileTypes = eval(f"fileTypes{event}")
        all = eval(f"all{event}")
        thisButton = wx.FindWindowById(all)
        checkBoxListFileTypes = wx.FindWindowById(fileTypes)
        indexes = checkBoxListFileTypes.GetCount()
        selectedItems = checkBoxListFileTypes.GetCheckedItems()
        if indexes and indexes != len(selectedItems):
            checkBoxListFileTypes.SetCheckedItems(range(indexes))
            thisButton.SetLabel("Check none")
        else:
            checkBoxListFileTypes.SetCheckedItems([])
            thisButton.SetLabel("Check all")

    def convertToMkv(self, event):
        checkBoxListWindow = wx.FindWindowById(selectedFilesToMkv)
        currentFile = wx.FindWindowById(currentFileToMkv)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarToMkv)
        # print(indexes)
        if indexes:
            allFiles = checkBoxListWindow.GetItems()
            duplicateFiles = list(allFiles)
            for index, file in enumerate(allFiles):
                currentFile.SetLabel(str(file))
                selectedDir = os.path.dirname(file)
                fName = os.path.basename(file)
                fNameNoExt = os.path.splitext(fName)[0]
                if not os.path.exists((f"{selectedDir}\\mkvmerge_old")):
                    os.makedirs((f"{selectedDir}\\mkvmerge_old"))
                mkvmerge_old = (f"{selectedDir}\mkvmerge_old\{fName}")
                shutil.move(file, mkvmerge_old)
                mkvCommand = f"\"{mkvMerge}\" --output \"{selectedDir}\\{fNameNoExt}.mkv\" \"{selectedDir}\\mkvmerge_old\\{fName}\""
                presentage = int(100*(index+1)/indexes)
                print(presentage)
                pBar.SetValue((presentage))
                runCommand(mkvCommand)
                duplicateFiles.remove(duplicateFiles[0])
                checkBoxListWindow.Set(duplicateFiles)
        currentFile.SetLabel("")
        
    def convertToAudio( self, event ):
        checkBoxListWindow = wx.FindWindowById(selectedFilesToAudio)
        currentFile = wx.FindWindowById(currentFileToAudio)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarToAudio)
        # print(indexes)
        if indexes:
            allFiles = checkBoxListWindow.GetItems()
            duplicateFiles = list(allFiles)
            for index, file in enumerate(allFiles):
                currentFile.SetLabel(str(file))
                selectedDir = os.path.dirname(file)
                fName = os.path.basename(file)
                fNameNoExt = os.path.splitext(fName)[0]
                if not os.path.exists((f"{selectedDir}\\mkvmerge_audio")):
                    os.makedirs((f"{selectedDir}\\mkvmerge_audio"))
                audioCommand = f"\"{mkvMerge}\" --output \"{selectedDir}\\mkvmerge_audio\\{fNameNoExt}.mka\" --no-video --language 1:und  \"{selectedDir}\\{fName}\""
                presentage = int(100*(index+1)/indexes)
                pBar.SetValue((presentage))
                runCommand(audioCommand)
                duplicateFiles.remove(duplicateFiles[0])
                checkBoxListWindow.Set(duplicateFiles)
        currentFile.SetLabel("")

    def cropVideo( self, event ):
        checkBoxListWindow = wx.FindWindowById(selectedFilesCrop)
        currentFile = wx.FindWindowById(currentFileCrop)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarCrop)
        cTopWindow = wx.FindWindowById(cTop)
        cLeftWindow = wx.FindWindowById(cLeft)
        cRightWindow = wx.FindWindowById(cRight)
        cBottomWindow = wx.FindWindowById(cBottom)
        cTopValue = int(cTopWindow.GetLineText(0))
        cLeftValue = int(cLeftWindow.GetLineText(0))
        cRightValue = int(cRightWindow.GetLineText(0))
        cBottomValue = int(cBottomWindow.GetLineText(0))
        # print(indexes)
        if indexes:
            allFiles = checkBoxListWindow.GetItems()
            duplicateFiles = list(allFiles)
            for index, file in enumerate(allFiles):
                currentFile.SetLabel(str(file))
                selectedDir = os.path.dirname(file)
                fName = os.path.basename(file)
                fNameNoExt = os.path.splitext(fName)[0]
                fNameExt = os.path.splitext(fName)[1]
                if not str(fNameExt).lower() ==".mkv":
                    if not os.path.exists((f"{selectedDir}\\mkvmerge_old")):
                        os.makedirs((f"{selectedDir}\\mkvmerge_old"))
                    mkvmerge_old = (f"{selectedDir}\mkvmerge_old\{fName}")
                    shutil.move(file, mkvmerge_old)
                    mkvCommand = f"\"{mkvMerge}\" --output \"{selectedDir}\\{fNameNoExt}.mkv\" \"{selectedDir}\\mkvmerge_old\\{fName}\""
                    runCommand(mkvCommand)
                
                if cTopValue + cBottomValue + cLeftValue + cRightValue:
                    mkvCropCommand = f"\"{mkvpropedit}\" \"{selectedDir}\\{fNameNoExt}.mkv\" --edit track:v1 --set pixel-crop-top={int(cTopValue)} --set pixel-crop-left={int(cLeftValue)}  --set pixel-crop-right={int(cRightValue)} --set pixel-crop-bottom={int(cBottomValue)}"
                else:
                    mkvCropCommand = f"\"{mkvpropedit}\" \"{selectedDir}\\{fNameNoExt}.mkv\" --edit track:v1 --delete pixel-crop-top --delete pixel-crop-left  --delete pixel-crop-right --delete pixel-crop-bottom"
                
                presentage = int(100*(index+1)/indexes)
                pBar.SetValue((presentage))
                runCommand(mkvCropCommand)
                duplicateFiles.remove(duplicateFiles[0])
                checkBoxListWindow.Set(duplicateFiles)
        currentFile.SetLabel("")


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        super().__init__()
        self.m_checkList1 = window

    def OnDropFiles(self, x, y, filenames):
        oldfiles = self.m_checkList1.GetCheckedStrings()
        allFiles = list(oldfiles) + filenames
        allFiles = list(dict.fromkeys(allFiles))
        self.m_checkList1.Set(allFiles)
        return True

def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output = ""
    for line in p.stdout:
        line = line.decode(
            errors="replace" if (sys.version_info) < (
                3, 5) else "backslashreplace"
        ).rstrip()
        output += line
        print(line)
        window.Refresh() if window else None  # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)

wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False)
frame = MyFrame1(None)

frame.Show(True)
app.MainLoop()