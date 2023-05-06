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
import shutil
import json
import threading

true = True
defaultfileTypesList = [".mkv" ,".ts" ,".mp4" ,".avi" ,".webm" ,".flv" ,".ogg" ,".mov" ,".mpeg-2"]
# defaultfileTypesFillter = "(*.mkv)|*.mkv|(*.mp4)|*.mp4|(*.ts)|*.ts|(*.flv)|*.flv|(*.avo)|*.avo|(*.webm)|*.webm|(*.ogg)|*.ogg|(*.mov)|*.mov|(*.mpeg-2)|*.mpeg-2"
defaultFileTypeFillter = "Videos|*.mkv;*.ts;*.mp4;*.avi;*.webm;*.flv;*.ogg;*.mov;*.mpeg-2|All files (*.*)|*.*"
mkvMerge = "C:\Program Files\MKVToolNix\mkvmerge.exe"
mkvpropedit = "C:\Program Files\MKVToolNix\mkvpropedit.exe"

selectedFilesToMkv = 1000
browseFilesToMkv = 1001
browseFolderToMkv = 1002
selectAllToMkv = 1003
dBtnToMkv = 1004
fileTypesToMkv = 1005
allToMkv = 1006
runToMkv = 1007
currentFileToMkv = 1008
pBarToMkv = 1009
selectedFilesToAudio = 1010
browseFilesToAudio = 1011
browseFolderToAudio = 1012
selectAllToAudio = 1013
dBtnToAudio = 1014
fileTypesToAudio = 1015
allToAudio = 1016
runToAudio = 1017
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
runCrop = 1031
currentFileCrop = 1032
pBarCrop = 1033
selectedFilesOptions = 1034
browseFilesOptions = 1035
browseFolderOptions = 1036
selectAllOptions = 1037
dBtnOptions = 1038
fileTypesOptions = 1039
allOptions = 1040
optionsFile = 1041
runOptions = 1042
currentFileOptions = 1043
pBarOptions = 1044
tabContainer = 1045
clearListToAudio = 1047
clearListCrop = 1048
mkvmergeTomkv = 1049
mkvmergeOptions = 1050
mkvmergeOldFolderOptions = 1051
mkvmergeOldFolderToMkv = 1052

mainDir = f"{os.path.dirname(__file__)}"
settingsIcon = f"{mainDir}\\mkv.ico"


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 664,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 660,600 ), wx.Size( 660,600 ))

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook30 = wx.Notebook( self, tabContainer, wx.DefaultPosition, wx.DefaultSize, 0 )
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
        bSizer81 = wx.BoxSizer( wx.VERTICAL )

        m_checkList1Choices = []
        self.m_checkList1 = wx.CheckListBox( self.m_panel71, selectedFilesToMkv, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList1Choices, wx.HSCROLL )
        self.m_checkList1.DragAcceptFiles( true )
        self.m_checkList1.SetMinSize( wx.Size( -1,230 ) )

        bSizer81.Add( self.m_checkList1, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel9 = wx.Panel( self.m_panel71, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button3 = wx.Button( self.m_panel9, browseFilesToMkv, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button11 = wx.Button( self.m_panel9, browseFolderToMkv, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button11, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button15 = wx.Button( self.m_panel9, selectAllToMkv, u"Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button15, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button15.Disable()
        
        self.m_button111 = wx.Button( self.m_panel9, dBtnToMkv, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.m_button111.Disable()

        self.m_panel9.SetSizer( bSizer71 )
        self.m_panel9.Layout()
        bSizer71.Fit( self.m_panel9 )
        bSizer81.Add( self.m_panel9, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


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
        
        bSizer42 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button211 = wx.Button( self.m_panel20, mkvmergeTomkv, u"mkvmerge old", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer42.Add( self.m_button211, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticText13 = wx.StaticText( self.m_panel20, mkvmergeOldFolderToMkv, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
        self.m_staticText13.Wrap( -1 )
        self.m_staticText13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

        bSizer42.Add( self.m_staticText13, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizer7.Add( bSizer42, 0, wx.EXPAND, 5 )
        self.m_panel20.SetSizer( bSizer7 )
        self.m_panel20.Layout()
        bSizer7.Fit( self.m_panel20 )
        bSizer6.Add( self.m_panel20, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button9 = wx.Button( self.tomkv, runToMkv, u"Convert to mkv", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer12.Add( self.m_button9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.m_button9.Disable()

        self.m_staticText31 = wx.StaticText( self.tomkv, currentFileToMkv, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        self.m_staticText31.Wrap( -1 )

        bSizer12.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )

        self.m_gauge1 = wx.Gauge( self.tomkv, pBarToMkv, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue( 0 )
        bSizer11.Add( self.m_gauge1, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer6.Add( bSizer11, 0, wx.EXPAND, 5 )


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
        bSizer51 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel82 = wx.Panel( self.m_panel72, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        bSizer82 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel711 = wx.Panel( self.m_panel82, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer811 = wx.BoxSizer( wx.VERTICAL )

        m_checkList12Choices = []
        self.m_checkList12 = wx.CheckListBox( self.m_panel711, selectedFilesToAudio, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList12Choices, wx.HSCROLL )
        self.m_checkList12.DragAcceptFiles( true )
        self.m_checkList12.SetMinSize( wx.Size( -1,230 ) )

        bSizer811.Add( self.m_checkList12, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel91 = wx.Panel( self.m_panel711, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer711 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer711.SetMinSize( wx.Size( -1,40 ) )
        self.m_button31 = wx.Button( self.m_panel91, browseFilesToAudio, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button112 = wx.Button( self.m_panel91, browseFolderToAudio, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button112, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button151 = wx.Button( self.m_panel91, selectAllToAudio, u"Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button151, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button151.Disable()
        
        self.m_button1111 = wx.Button( self.m_panel91, dBtnToAudio, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button1111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.m_button1111.Disable()

        self.m_panel91.SetSizer( bSizer711 )
        self.m_panel91.Layout()
        bSizer711.Fit( self.m_panel91 )
        bSizer811.Add( self.m_panel91, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


        self.m_panel711.SetSizer( bSizer811 )
        self.m_panel711.Layout()
        bSizer811.Fit( self.m_panel711 )
        bSizer82.Add( self.m_panel711, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_panel82.SetSizer( bSizer82 )
        self.m_panel82.Layout()
        bSizer82.Fit( self.m_panel82 )
        bSizer51.Add( self.m_panel82, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 5 )

        self.m_panel72.SetSizer( bSizer51 )
        self.m_panel72.Layout()
        bSizer51.Fit( self.m_panel72 )
        bSizer72.Add( self.m_panel72, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.clearList1 = wx.CheckBox( self.m_panel201, clearListToAudio, u"Clear list after complete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer72.Add( self.clearList1, 0, wx.ALL, 5 )

        self.m_panel201.SetSizer( bSizer72 )
        self.m_panel201.Layout()
        bSizer72.Fit( self.m_panel201 )
        bSizer61.Add( self.m_panel201, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer111 = wx.BoxSizer( wx.VERTICAL )

        bSizer121 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer121.SetMinSize( wx.Size( -1,30 ) )
        self.m_button91 = wx.Button( self.toAudio, runToAudio, u"Convert to audio", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer121.Add( self.m_button91, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.m_button91.Disable()

        self.m_staticText311 = wx.StaticText( self.toAudio, currentFileToAudio, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        self.m_staticText311.Wrap( -1 )

        bSizer121.Add( self.m_staticText311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer111.Add( bSizer121, 0, wx.EXPAND, 5 )

        self.m_gauge11 = wx.Gauge( self.toAudio, pBarToAudio, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge11.SetValue( 0 )
        bSizer111.Add( self.m_gauge11, 0, wx.EXPAND|wx.ALL, 5 )


        bSizer61.Add( bSizer111, 0, wx.EXPAND, 5 )


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
        bSizer8111 = wx.BoxSizer( wx.VERTICAL )

        m_checkList121Choices = []
        self.m_checkList121 = wx.CheckListBox( self.m_panel7111, selectedFilesCrop, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList121Choices, wx.HSCROLL )
        self.m_checkList121.DragAcceptFiles( true )
        self.m_checkList121.SetMinSize( wx.Size( -1,200 ) )

        bSizer8111.Add( self.m_checkList121, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel911 = wx.Panel( self.m_panel7111, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer7111 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer7111.SetMinSize( wx.Size( -1,40 ) )
        self.m_button311 = wx.Button( self.m_panel911, browseFilesCrop, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button1121 = wx.Button( self.m_panel911, browseFolderCrop, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button1121, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button1511 = wx.Button( self.m_panel911, selectAllCrop, u"Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button1511, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button1511.Disable()

        self.m_button11111 = wx.Button( self.m_panel911, dBtnCrop, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button11111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.m_button11111.Disable()

        self.m_panel911.SetSizer( bSizer7111 )
        self.m_panel911.Layout()
        bSizer7111.Fit( self.m_panel911 )
        bSizer8111.Add( self.m_panel911, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


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

        self.clearList2 = wx.CheckBox( self.m_panel2011, clearListCrop, u"Clear list after complete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer721.Add( self.clearList2, 0, wx.ALL, 5 )

        self.m_panel2011.SetSizer( bSizer721 )
        self.m_panel2011.Layout()
        bSizer721.Fit( self.m_panel2011 )
        bSizer611.Add( self.m_panel2011, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer1111 = wx.BoxSizer( wx.VERTICAL )

        bSizer46 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer46.SetMinSize( wx.Size( -1,30 ) )
        self.m_staticText15 = wx.StaticText( self.crop, wx.ID_ANY, u"Top", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        bSizer46.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl4 = wx.SpinCtrl( self.crop, cTop, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl4, 1, wx.ALL, 5 )

        self.m_staticText16 = wx.StaticText( self.crop, wx.ID_ANY, u"Right", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )

        bSizer46.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl3 = wx.SpinCtrl( self.crop, cRight, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl3, 1, wx.ALL, 5 )

        self.m_staticText17 = wx.StaticText( self.crop, wx.ID_ANY, u"Bottom", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )

        bSizer46.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl2 = wx.SpinCtrl( self.crop, cBottom, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl2, 1, wx.ALL, 5 )

        self.m_staticText18 = wx.StaticText( self.crop, wx.ID_ANY, u"Left", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )

        bSizer46.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl1 = wx.SpinCtrl( self.crop, cLeft, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl1, 1, wx.ALL, 5 )


        bSizer1111.Add( bSizer46, 0, wx.EXPAND, 5 )

        bSizer1211 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer1211.SetMinSize( wx.Size( -1,30 ) )
        self.m_button911 = wx.Button( self.crop, runCrop, u"Crop", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer1211.Add( self.m_button911, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
        self.m_button911.Disable()

        self.m_staticText3111 = wx.StaticText( self.crop, currentFileCrop, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3111.Wrap( -1 )

        bSizer1211.Add( self.m_staticText3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer1111.Add( bSizer1211, 0, wx.EXPAND, 5 )

        self.m_gauge111 = wx.Gauge( self.crop, pBarCrop, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge111.SetValue( 0 )
        bSizer1111.Add( self.m_gauge111, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer611.Add( bSizer1111, 0, wx.EXPAND, 5 )


        bSizer411.Add( bSizer611, 1, wx.EXPAND, 5 )


        self.crop.SetSizer( bSizer411 )
        self.crop.Layout()
        bSizer411.Fit( self.crop )
        self.m_notebook30.AddPage( self.crop, u"crop", False )
        self.mkvOptions = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4111 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText3211 = wx.StaticText( self.mkvOptions, wx.ID_ANY, u"mkv options", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3211.Wrap( -1 )

        bSizer4111.Add( self.m_staticText3211, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        bSizer6111 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel20111 = wx.Panel( self.mkvOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer7211 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel7211 = wx.Panel( self.m_panel20111, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer5111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel8211 = wx.Panel( self.m_panel7211, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        bSizer8211 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel71111 = wx.Panel( self.m_panel8211, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer81111 = wx.BoxSizer( wx.VERTICAL )

        m_checkList1211Choices = []
        self.m_checkList1211 = wx.CheckListBox( self.m_panel71111, selectedFilesOptions, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList1211Choices, wx.HSCROLL )
        self.m_checkList1211.DragAcceptFiles( true )
        self.m_checkList1211.SetMinSize( wx.Size( -1,150 ) )

        bSizer81111.Add( self.m_checkList1211, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel9111 = wx.Panel( self.m_panel71111, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel9111.SetMinSize( wx.Size( -1,40 ) )

        bSizer71111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button3111 = wx.Button( self.m_panel9111, browseFilesOptions, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71111.Add( self.m_button3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button11211 = wx.Button( self.m_panel9111, browseFolderOptions, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71111.Add( self.m_button11211, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_button15111 = wx.Button( self.m_panel9111, selectAllOptions, u"Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71111.Add( self.m_button15111, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button15111.Disable()

        self.m_button111111 = wx.Button( self.m_panel9111, dBtnOptions, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71111.Add( self.m_button111111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.m_button111111.Disable()

        self.m_panel9111.SetSizer( bSizer71111 )
        self.m_panel9111.Layout()
        bSizer71111.Fit( self.m_panel9111 )
        bSizer81111.Add( self.m_panel9111, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        self.m_panel71111.SetSizer( bSizer81111 )
        self.m_panel71111.Layout()
        bSizer81111.Fit( self.m_panel71111 )
        bSizer8211.Add( self.m_panel71111, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel8211.SetSizer( bSizer8211 )
        self.m_panel8211.Layout()
        bSizer8211.Fit( self.m_panel8211 )
        bSizer5111.Add( self.m_panel8211, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 5 )


        self.m_panel7211.SetSizer( bSizer5111 )
        self.m_panel7211.Layout()
        bSizer5111.Fit( self.m_panel7211 )
        bSizer7211.Add( self.m_panel7211, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer421 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button2111 = wx.Button( self.m_panel20111, mkvmergeOptions, u"mkvmerge old", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer421.Add( self.m_button2111, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticText131 = wx.StaticText( self.m_panel20111, mkvmergeOldFolderOptions, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_staticText131.Wrap( -1 )
        self.m_staticText131.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

        bSizer421.Add( self.m_staticText131, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizer7211.Add( bSizer421, 0, wx.EXPAND, 5 )

        self.m_panel20111.SetSizer( bSizer7211 )
        self.m_panel20111.Layout()
        bSizer7211.Fit( self.m_panel20111 )
        bSizer6111.Add( self.m_panel20111, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer11111 = wx.BoxSizer( wx.VERTICAL )

        bSizer461 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_filePicker1 = wx.FilePickerCtrl( self.mkvOptions, optionsFile, wx.EmptyString, u"Select options file", u"*.json*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer461.Add( self.m_filePicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


        bSizer11111.Add( bSizer461, 0, wx.EXPAND, 5 )

        bSizer12111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button9111 = wx.Button( self.mkvOptions, runOptions, u"Run", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer12111.Add( self.m_button9111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.m_button9111.Disable()

        self.m_staticText31111 = wx.StaticText( self.mkvOptions, currentFileOptions, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText31111.Wrap( -1 )

        bSizer12111.Add( self.m_staticText31111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer11111.Add( bSizer12111, 0, wx.EXPAND, 5 )

        self.m_gauge1111 = wx.Gauge( self.mkvOptions, pBarOptions, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge1111.SetValue( 0 )
        bSizer11111.Add( self.m_gauge1111, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer6111.Add( bSizer11111, 0, wx.EXPAND, 5 )


        bSizer4111.Add( bSizer6111, 1, wx.EXPAND, 5 )


        self.mkvOptions.SetSizer( bSizer4111 )
        self.mkvOptions.Layout()
        bSizer4111.Fit( self.mkvOptions )
        self.m_notebook30.AddPage( self.mkvOptions, u"mkvOptions", False )

        bSizer2.Add( self.m_notebook30, 1, wx.EXPAND |wx.ALL, 5 )

        self.SetIcon(wx.Icon(settingsIcon, wx.BITMAP_TYPE_ICO))
        
        self.SetSizer( bSizer2 )
        self.Layout()


        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button3.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToMkv") )
        self.m_button11.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToMkv") )
        self.m_button15.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToMkv") )
        self.m_button211.Bind( wx.EVT_BUTTON, lambda event: self.setMkvMergeFolder("ToMkv") )
        self.m_button111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("ToMkv") )
        self.m_button9.Bind( wx.EVT_BUTTON, lambda event: self.processThread("self.runToMkv "))
        self.m_button31.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToAudio") )
        self.m_button112.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToAudio") )
        self.m_button151.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToAudio") )
        self.m_button1111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("ToAudio") )
        self.m_button91.Bind( wx.EVT_BUTTON, lambda event: self.processThread("self.runToAudio") )
        self.m_button311.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("Crop") )
        self.m_button1121.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("Crop") )
        self.m_button1511.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("Crop") )
        self.m_button11111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("Crop") )
        self.m_button911.Bind( wx.EVT_BUTTON, lambda event: self.processThread("self.runCrop") )
        self.m_button3111.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("Options") )
        self.m_button11211.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("Options") )
        self.m_button15111.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("Options") )
        self.m_button2111.Bind( wx.EVT_BUTTON, lambda event: self.setMkvMergeFolder("Options") )
        self.m_button111111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("Options") )
        self.m_button9111.Bind( wx.EVT_BUTTON, lambda event: self.processThread("self.runOptions") )

    def __del__( self ):
        pass
    
    def processThread( self, event ):
        process= eval(event)
        t = threading.Thread(target=process)
        t.daemon = True # set thread as daemon to terminate when main thread ends
        t.start()

    # Virtual event handlers, override them in your derived class
    def deleteFromList( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        allFilesInCheckBoxList = checkBoxListWindow.GetItems()
        selectedFilesFromList = checkBoxListWindow.GetCheckedStrings()
        newList = list(filter(lambda file:str(file) not in selectedFilesFromList,allFilesInCheckBoxList))
        checkBoxListWindow.SetItems(newList)
        selectAll = eval(f"selectAll{event}")
        thisButton = wx.FindWindowById(selectAll)
        buttonId = eval(f"run{event}")
        selectAllId = eval(f"selectAll{event}")
        delBtnId = eval(f"dBtn{event}")
        delBtnWindow = wx.FindWindowById(delBtnId)
        buttonWindow = wx.FindWindowById(buttonId)
        selectAllWindow = wx.FindWindowById(selectAllId)
        if len(checkBoxListWindow.GetItems()):
            buttonWindow.Enable()
            selectAllWindow.Enable()
            if len(checkBoxListWindow.GetCheckedItems()):
                delBtnWindow.Enable()
            else:
                delBtnWindow.Disable() 
        else:
            delBtnWindow.Disable() 
            buttonWindow.Disable() 
            selectAllWindow.Disable() 

    def openFilesSelector( self, event ):
        try:
            selectedFiles = eval(f"selectedFiles{event}")
            checkBoxListWindow = wx.FindWindowById(selectedFiles)
            oldFiles = checkBoxListWindow.GetItems() 
            openFileDialog = wx.FileDialog(self, "Select files", wildcard=defaultFileTypeFillter,
               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE)
            openFileDialog.ShowModal()
            selectedFiles = openFileDialog.GetFilenames()
            allFiles = oldFiles + selectedFiles
            allFiles = list(filter(lambda file: str(file).endswith(tuple(defaultfileTypesList)),allFiles))
            checkBoxListWindow.Set(allFiles)
            openFileDialog.Destroy()
            buttonId = eval(f"run{event}")
            selectAllId = eval(f"selectAll{event}")
            delBtnId = eval(f"dBtn{event}")
            delBtnWindow = wx.FindWindowById(delBtnId)
            buttonWindow = wx.FindWindowById(buttonId)
            selectAllWindow = wx.FindWindowById(selectAllId)
            if len(checkBoxListWindow.GetItems()):
                buttonWindow.Enable()
                selectAllWindow.Enable()
                if len(checkBoxListWindow.GetCheckedItems()):
                    delBtnWindow.Enable()
                else:
                    delBtnWindow.Disable() 
            else:
                delBtnWindow.Disable() 
                buttonWindow.Disable() 
                selectAllWindow.Disable() 
        except Exception as e:
            print(e)

    def selectFolder( self, event ):
        try:
            selectedFiles = eval(f"selectedFiles{event}")
            checkBoxListWindow = wx.FindWindowById(selectedFiles)
            openDirDialog = wx.DirDialog(self, "Choose folder",style=wx.DD_DIR_MUST_EXIST)
            openDirDialog.ShowModal()
            selectedDir = openDirDialog.GetPath()
            filesInDir = os.listdir(selectedDir)
            absFilesInDir = [f"{selectedDir}\\" + x for x in filesInDir]
            filterFilesInDir = list(filter(lambda file: str(file).endswith(tuple(defaultfileTypesList)),absFilesInDir))
            checkBoxListWindow.Set(filterFilesInDir)
            openDirDialog.Destroy()
            buttonId = eval(f"run{event}")
            selectAllId = eval(f"selectAll{event}")
            delBtnId = eval(f"dBtn{event}")
            delBtnWindow = wx.FindWindowById(delBtnId)
            buttonWindow = wx.FindWindowById(buttonId)
            selectAllWindow = wx.FindWindowById(selectAllId)
            if len(checkBoxListWindow.GetItems()):
                buttonWindow.Enable()
                selectAllWindow.Enable()
                if len(checkBoxListWindow.GetCheckedItems()):
                    delBtnWindow.Enable()
                else:
                    delBtnWindow.Disable() 
            else:
                delBtnWindow.Disable() 
                buttonWindow.Disable() 
                selectAllWindow.Disable() 
        except Exception as e:
            print(e)
            
    def setMkvMergeFolder( self, event ):
        try:
            openDirDialog = wx.DirDialog(self, "Choose folder",style=wx.DD_DIR_MUST_EXIST)
            openDirDialog.ShowModal()
            selectedDir = openDirDialog.GetPath()
            dirTxt = wx.FindWindowById(eval(f"mkvmergeOldFolder{event}"))
            dirTxt.SetLabel(str(selectedDir))
            style = dirTxt.GetWindowStyleFlag()
            style  &= ~wx.ALIGN_RIGHT
            openDirDialog.Destroy()
        except Exception as e:
            print(e)


    def selectAll( self, event ):
        try:
            selectedFiles = eval(f"selectedFiles{event}")
            checkBoxListWindow = wx.FindWindowById(selectedFiles)
            indexes = checkBoxListWindow.GetCount()
            selectedItems = checkBoxListWindow.GetCheckedItems()
            if indexes and indexes != len(selectedItems):
                checkBoxListWindow.SetCheckedItems(range(indexes))
            else:
                checkBoxListWindow.SetCheckedItems([])
            delBtnId = eval(f"dBtn{event}")
            delBtnWindow = wx.FindWindowById(delBtnId)
            if len(checkBoxListWindow.GetItems()):
                if len(checkBoxListWindow.GetCheckedItems()):
                    delBtnWindow.Enable()
                else:
                    delBtnWindow.Disable() 
            else:
                delBtnWindow.Disable() 
        except Exception as e:
            print(e)

    def runToMkv(self):
        try:
            checkBoxListWindow = wx.FindWindowById(selectedFilesToMkv)
            currentFile = wx.FindWindowById(currentFileToMkv)
            indexes = checkBoxListWindow.GetCount()
            convertTomkvWindow = wx.FindWindowById(runToMkv)
            pBar = wx.FindWindowById(pBarToMkv)
            mkvmergeDirWindow = wx.FindWindowById(mkvmergeOldFolderToMkv)
            if indexes:
                allFiles = checkBoxListWindow.GetItems()
                drive, path = os.path.splitdrive(os.path.dirname(allFiles[0]))
                if not os.path.isdir(mkvmergeDirWindow.GetLabel()):
                    mkvmergeDir = drive
                else:
                    mkvmergeDir = mkvmergeDirWindow.GetLabel()
                duplicateFiles = list(allFiles)
                convertTomkvWindow.Disable()
                for index, file in enumerate(allFiles):
                    currentFile.SetLabel(str(file))
                    selectedDir = os.path.dirname(file)
                    fName = os.path.basename(file)
                    fNameNoExt = os.path.splitext(fName)[0]
                    if not os.path.exists((f"{mkvmergeDir}\\mkvmerge_old\\{path}")):
                        os.makedirs((f"{mkvmergeDir}\\mkvmerge_old\\{path}"))
                    mkvmerge_old = (f"{mkvmergeDir}\mkvmerge_old\\{path}\\{fName}")
                    shutil.move(file, mkvmerge_old)
                    mkvCommand = f"\"{mkvMerge}\" --output \"{selectedDir}\\{fNameNoExt}.mkv\" \"{mkvmergeDir}\\mkvmerge_old\\{path}\\{fName}\""
                    presentage = int(100*(index+1)/indexes)
                    # print(presentage)
                    pBar.SetValue((presentage))
                    runCommand(mkvCommand)
            currentFile.SetLabel("")
            pBar.SetValue(0)
            checkBoxListWindow.SetItems([])
        except Exception as e:
            print(e)
        
    def runToAudio( self ):
        try:
            checkBoxListWindow = wx.FindWindowById(selectedFilesToAudio)
            currentFile = wx.FindWindowById(currentFileToAudio)
            convertToAudioWindow = wx.FindWindowById(runToAudio)
            indexes = checkBoxListWindow.GetCount()
            pBar = wx.FindWindowById(pBarToAudio)
            clearListCheckbox = wx.FindWindowById(clearListToAudio)
            isClearChecked = clearListCheckbox.GetValue()
            # print(indexes)
            if indexes:
                allFiles = checkBoxListWindow.GetItems()
                duplicateFiles = list(allFiles)
                convertToAudioWindow.Disable()
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
            currentFile.SetLabel("")
            pBar.SetValue(0)
            if isClearChecked:
                checkBoxListWindow.SetItems([])
            else:
                convertToAudioWindow.Enable()
        except Exception as e:
            print(e)

    def runCrop( self ):
        try:
            checkBoxListWindow = wx.FindWindowById(selectedFilesCrop)
            currentFile = wx.FindWindowById(currentFileCrop)
            convertCropWindow = wx.FindWindowById(runCrop)
            indexes = checkBoxListWindow.GetCount()
            pBar = wx.FindWindowById(pBarCrop)
            cTopWindow = wx.FindWindowById(cTop)
            cLeftWindow = wx.FindWindowById(cLeft)
            cRightWindow = wx.FindWindowById(cRight)
            cBottomWindow = wx.FindWindowById(cBottom)
            cTopValue = int(cTopWindow.GetTextValue())
            cLeftValue = int(cLeftWindow.GetTextValue())
            cRightValue = int(cRightWindow.GetTextValue())
            cBottomValue = int(cBottomWindow.GetTextValue())
            clearListCheckbox = wx.FindWindowById(clearListCrop)
            isClearChecked = clearListCheckbox.GetValue()
            # print(indexes)
            if indexes:
                allFiles = checkBoxListWindow.GetItems()
                convertCropWindow.Disable()
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
                    mkvCropCommand = f"\"{mkvpropedit}\" \"{selectedDir}\\{fNameNoExt}.mkv\" --edit track:v1 --delete pixel-crop-top --delete pixel-crop-left  --delete pixel-crop-right --delete pixel-crop-bottom"
                    runCommand(mkvCropCommand)
                    mkvCropCommand = f"\"{mkvpropedit}\" \"{selectedDir}\\{fNameNoExt}.mkv\" --edit track:v1 --set pixel-crop-top={int(cTopValue)} --set pixel-crop-left={int(cLeftValue)}  --set pixel-crop-right={int(cRightValue)} --set pixel-crop-bottom={int(cBottomValue)}"    
                    presentage = int(100*(index+1)/indexes)
                    pBar.SetValue((presentage))
                    runCommand(mkvCropCommand)
            currentFile.SetLabel("")
            pBar.SetValue(0)
            if isClearChecked:
                checkBoxListWindow.SetItems([])
            else:
                convertCropWindow.Enable()
        except Exception as e:
            print(e)
        
    def runOptions( self ):
        try:
            optionJson = wx.FindWindowById(optionsFile)
            checkBoxListWindow = wx.FindWindowById(selectedFilesOptions)
            convertOptionsWindow = wx.FindWindowById(runOptions)
            currentFile = wx.FindWindowById(currentFileOptions)
            indexes = checkBoxListWindow.GetCount()
            pBar = wx.FindWindowById(pBarOptions)
            jsonFile = optionJson.GetPath()
            if os.path.exists(jsonFile):
                jsonVar = open(jsonFile)
                fileOptions = list(json.load(jsonVar))
                try:
                    removeIndex = fileOptions.index('--output')
                    del fileOptions[removeIndex] # remove --output line
                    del fileOptions[removeIndex] # remove file line
                except ValueError:
                    print(e)  # item not in list
                try:
                    removeIndex = fileOptions.index('(')
                    del fileOptions[removeIndex] # remove ( line
                    del fileOptions[removeIndex] # remove what's between () line
                    del fileOptions[removeIndex] # remove ) line
                except Exception as e:
                    print(e) # item not in list
                if fileOptions[0] != "--ui-language":
                    currentFile.SetLabel("wrong json file")
                    return
                selectedJsonDir = os.path.dirname(jsonFile)
                with open(f'{selectedJsonDir}\\options.json', 'w') as f:
                    json.dump(fileOptions, f)
                jsonFile = f'{selectedJsonDir}\\options.json'
                if indexes:
                    allFiles = checkBoxListWindow.GetItems()
                    mkvmergeDirWindow = wx.FindWindowById(mkvmergeOldFolderOptions)
                    drive, path = os.path.splitdrive(os.path.dirname(allFiles[0]))
                    if not os.path.isdir(mkvmergeDirWindow.GetLabel()):
                        mkvmergeDir = drive
                    else:
                        mkvmergeDir = mkvmergeDirWindow.GetLabel()
                    duplicateFiles = list(allFiles)
                    convertOptionsWindow.Disable()
                    for index, file in enumerate(allFiles):
                        currentFile.SetLabel(str(file))
                        selectedDir = os.path.dirname(file)
                        fName = os.path.basename(file)
                        fNameNoExt = os.path.splitext(fName)[0]
                        if not os.path.exists((f"{mkvmergeDir}\\mkvmerge_old\\{path}")):
                            os.makedirs((f"{mkvmergeDir}\\mkvmerge_old\\{path}"))
                        mkvmerge_old = (f"{mkvmergeDir}\mkvmerge_old\\{path}\\{fName}")
                        shutil.move(file, mkvmerge_old)
                        mkvCommand = f"\"{mkvMerge}\" @{jsonFile} -o \"{selectedDir}\\{fNameNoExt}.mkv\" \"{mkvmergeDir}\\mkvmerge_old\\{path}\\{fName}\""
                        presentage = int(100*(index+1)/indexes)
                        # print(presentage)
                        pBar.SetValue((presentage))
                        runCommand(mkvCommand)
                    currentFile.SetLabel("")
                    pBar.SetValue(0)
                    checkBoxListWindow.SetItems([])
        except Exception as e:
            print(e)
        
class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window,tab):
        super().__init__()
        self.m_checkList1 = window
        self.tab = tab

    def OnDropFiles(self, x, y, filenames):
        allFiles = filenames
        fileTypesList = defaultfileTypesList
        if os.path.isdir(filenames[0]):
            allFiles = []
            for root, dirs, files in os.walk(filenames[0]):
                for file in files:
                    allFiles.append(os.path.join(root, file))
            filenames = allFiles
        windowId = eval(f"selectedFiles{self.tab}")
        buttonId = eval(f"run{self.tab}")
        checkBoxList = wx.FindWindowById(windowId)
        oldfiles = checkBoxList.GetItems()
        allFiles = list(oldfiles) + filenames
        allFiles = list(dict.fromkeys(allFiles))
        if self.tab == "ToMkv":
            if ".mkv" in fileTypesList:
                fileTypesList.remove(".mkv")
        allFiles = list(filter(lambda file: str(file).endswith(tuple(fileTypesList)),allFiles))
        fileTypesList.append(".mkv")
        checkBoxList.Set(allFiles)
        if len(allFiles):
            buttonWindow = wx.FindWindowById(buttonId)
            buttonWindow.Enable()
        return True

def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,encoding='utf-8'
    )
    output = ""
    retval = p.wait(timeout)
    return (retval, output)

def fileTypeFormat(listOfTypes):
    finalString = ""
    if len(listOfTypes):
        for type in listOfTypes:
            # newStr = f"(*{type})|*{type}"
            # finalString = f"{finalString}|{newStr}" 
            newStr = f"*.{type}"
            finalString = f"{finalString} {newStr}" 
    # print(finalString[1:])
    return finalString
            

wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False)
frame = MyFrame1(None)
wx.FindWindowById(tabContainer).SetSelection(0)
frame.m_checkList1.SetDropTarget(MyFileDropTarget(frame.m_checkList1,"ToMkv"))
frame.m_checkList12.SetDropTarget(MyFileDropTarget(frame.m_checkList12,"ToAudio"))
frame.m_checkList121.SetDropTarget(MyFileDropTarget(frame.m_checkList121,"Crop"))
frame.m_checkList1211.SetDropTarget(MyFileDropTarget(frame.m_checkList1211,"Options"))
frame.Show(True)
app.MainLoop()