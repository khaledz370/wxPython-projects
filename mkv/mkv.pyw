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
import traceback
import sys
import translatesubs
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except:  
    config = {
            "mkvtoolnix":"C:\\Program Files\\MKVToolNix",
        }
    with open('config.json', 'w') as f:
        json.dump(config, f)

true = True
defaultfileTypesList = [".mkv" ,".ts" ,".mp4" ,".avi" ,".webm" ,".flv" ,".ogg" ,".mov" ,".mpeg-2"]
toMkvtfileTypesList = [".ts" ,".mp4" ,".avi" ,".webm" ,".flv" ,".ogg" ,".mov" ,".mpeg-2"]
subtitleFileTypeList = [".srt", ".sub", ".sbv", ".ass", ".ssa", ".usf", ".idx", ".aqt", ".jss", ".psb", ".rt", ".smi", ".stl", ".vtt", ".xml", ".txt"]
# defaultfileTypesFillter = "(*.mkv)|*.mkv|(*.mp4)|*.mp4|(*.ts)|*.ts|(*.flv)|*.flv|(*.avo)|*.avo|(*.webm)|*.webm|(*.ogg)|*.ogg|(*.mov)|*.mov|(*.mpeg-2)|*.mpeg-2"
defaultFileTypeFillter = "Videos|*.mkv;*.ts;*.mp4;*.avi;*.webm;*.flv;*.ogg;*.mov;*.mpeg-2|All files (*.*)|*.*"
subtitleFileTypeFillter = "Subtitles|*.srt;*.sub;*.sbv;*.ass;*.ssa;*.usf;*.idx;*.aqt;*.jss;*.psb;*.rt;*.smi;*.stl;*.vtt;*.xml;*.txt;|All files (*.*)|*.*"
mkvMerge = f"{config['mkvtoolnix']}\\mkvmerge.exe"
mkvpropedit = f"{config['mkvtoolnix']}\\mkvpropedit.exe"

languageCodes = [ "aa", "ab", "af", "ak", "sq", "am", "ar", "an", "hy", "as", "av", "ae", "ay", "az", "ba", "bm", "eu", "be", "bn", "bh", "bi", "bs", "br", "bg", "my", "ca", "km", "ch", "ce", "ny", "zh", "cu", "cv", "kw", "co", "cr", "hr", "cs", "da", "dv", "nl", "dz", "en", "eo", "et", "ee", "fo", "fj", "fi", "fr", "fy", "ff", "ka", "de", "gd", "ga", "gl", "gv", "el", "gn", "gu", "ht", "ha", "he", "hz", "hi", "ho", "hr", "hu", "ig", "is", "io", "ii", "iu", "ie", "ia", "id", "ik", "it", "jv", "ja", "kl", "kn", "ks", "kr", "kk", "km", "ki", "rw", "ky", "kv", "kg", "ko", "ku", "kj", "la", "lb", "lg", "li", "ln", "lo", "lt", "lu", "lv", "gv", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mh", "mn", "na", "nv", "nb", "nd", "ne", "ng", "nn", "no", "ii", "nr", "oc", "oj", "cu", "om", "or", "os", "pa", "pi", "fa", "pl", "ps", "pt", "qu", "rm", "ro", "rn", "ru", "sg", "sa", "si", "sk", "sl", "se", "sm", "sn", "sd", "so", "st", "es", "sc", "sr", "ss", "su", "sw", "sv", "ty", "ta", "tt", "te", "tg", "tl", "th", "bo", "ti", "to", "tn", "ts", "tk", "tr", "tw", "ug", "uk", "ur", "uz", "ve", "vi", "vo", "cy", "wa", "wo", "xh", "yi", "yo", "za", "zu" ]

# widget ids
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
mkvDir = 1053
selectedFilesTranslate = 1054
browseFilesTranslate = 1055
browseFolderTranslate = 1056
selectAllTranslate = 1057
dBtnTranslate = 1058
clearListTranslate = 1059
runTranslate = 1060
currentFileTranslate = 1061
pBarTranslate = 1062
translateTo = 1063
errorMissing = 1064
# end of widget ids

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

        self.m_staticText3 = wx.StaticText( self.tomkv, wx.ID_ANY, "Convert video to mkv", wx.DefaultPosition, wx.DefaultSize, 0 )
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

        self.m_button3 = wx.Button( self.m_panel9, browseFilesToMkv, "browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button11 = wx.Button( self.m_panel9, browseFolderToMkv, "select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button11, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button15 = wx.Button( self.m_panel9, selectAllToMkv, "Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button15, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button15.Disable()
        
        self.m_button111 = wx.Button( self.m_panel9, dBtnToMkv, "Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
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

        self.m_button211 = wx.Button( self.m_panel20, mkvmergeTomkv, "mkvmerge old", wx.DefaultPosition, wx.DefaultSize, 0 )
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

        self.m_button9 = wx.Button( self.tomkv, runToMkv, "Convert to mkv", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
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
        self.m_notebook30.AddPage( self.tomkv, "to mkv", True )
        self.toAudio = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer41 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText32 = wx.StaticText( self.toAudio, wx.ID_ANY, "Convert video to audio", wx.DefaultPosition, wx.DefaultSize, 0 )
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
        self.m_button31 = wx.Button( self.m_panel91, browseFilesToAudio, "browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button112 = wx.Button( self.m_panel91, browseFolderToAudio, "select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button112, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button151 = wx.Button( self.m_panel91, selectAllToAudio, "Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer711.Add( self.m_button151, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button151.Disable()
        
        self.m_button1111 = wx.Button( self.m_panel91, dBtnToAudio, "Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
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
        
        self.clearList1 = wx.CheckBox( self.m_panel201, clearListToAudio, "Clear list after complete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer72.Add( self.clearList1, 0, wx.ALL, 5 )

        self.m_panel201.SetSizer( bSizer72 )
        self.m_panel201.Layout()
        bSizer72.Fit( self.m_panel201 )
        bSizer61.Add( self.m_panel201, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer111 = wx.BoxSizer( wx.VERTICAL )

        bSizer121 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer121.SetMinSize( wx.Size( -1,30 ) )
        self.m_button91 = wx.Button( self.toAudio, runToAudio, "Convert to audio", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
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
        self.m_notebook30.AddPage( self.toAudio, "toAudio", False )
        self.crop = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer411 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText321 = wx.StaticText( self.crop, wx.ID_ANY, "crop video", wx.DefaultPosition, wx.DefaultSize, 0 )
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
        self.m_button311 = wx.Button( self.m_panel911, browseFilesCrop, "browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button1121 = wx.Button( self.m_panel911, browseFolderCrop, "select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button1121, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button1511 = wx.Button( self.m_panel911, selectAllCrop, "Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7111.Add( self.m_button1511, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button1511.Disable()

        self.m_button11111 = wx.Button( self.m_panel911, dBtnCrop, "Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
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

        self.clearList2 = wx.CheckBox( self.m_panel2011, clearListCrop, "Clear list after complete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer721.Add( self.clearList2, 0, wx.ALL, 5 )

        self.m_panel2011.SetSizer( bSizer721 )
        self.m_panel2011.Layout()
        bSizer721.Fit( self.m_panel2011 )
        bSizer611.Add( self.m_panel2011, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer1111 = wx.BoxSizer( wx.VERTICAL )

        bSizer46 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer46.SetMinSize( wx.Size( -1,30 ) )
        self.m_staticText15 = wx.StaticText( self.crop, wx.ID_ANY, "Top", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        bSizer46.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl4 = wx.SpinCtrl( self.crop, cTop, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl4, 1, wx.ALL, 5 )

        self.m_staticText16 = wx.StaticText( self.crop, wx.ID_ANY, "Right", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )

        bSizer46.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl3 = wx.SpinCtrl( self.crop, cRight, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl3, 1, wx.ALL, 5 )

        self.m_staticText17 = wx.StaticText( self.crop, wx.ID_ANY, "Bottom", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )

        bSizer46.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl2 = wx.SpinCtrl( self.crop, cBottom, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl2, 1, wx.ALL, 5 )

        self.m_staticText18 = wx.StaticText( self.crop, wx.ID_ANY, "Left", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )

        bSizer46.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl1 = wx.SpinCtrl( self.crop, cLeft, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 2000, 0 )
        bSizer46.Add( self.m_spinCtrl1, 1, wx.ALL, 5 )


        bSizer1111.Add( bSizer46, 0, wx.EXPAND, 5 )

        bSizer1211 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer1211.SetMinSize( wx.Size( -1,30 ) )
        self.m_button911 = wx.Button( self.crop, runCrop, "Crop", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
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
        self.m_notebook30.AddPage( self.crop, "crop", False )
        self.mkvOptions = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4111 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText3211 = wx.StaticText( self.mkvOptions, wx.ID_ANY, "mkv options", wx.DefaultPosition, wx.DefaultSize, 0 )
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

        self.m_button3111 = wx.Button( self.m_panel9111, browseFilesOptions, "browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71111.Add( self.m_button3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button11211 = wx.Button( self.m_panel9111, browseFolderOptions, "select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71111.Add( self.m_button11211, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_button15111 = wx.Button( self.m_panel9111, selectAllOptions, "Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71111.Add( self.m_button15111, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button15111.Disable()

        self.m_button111111 = wx.Button( self.m_panel9111, dBtnOptions, "Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
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

        self.m_button2111 = wx.Button( self.m_panel20111, mkvmergeOptions, "mkvmerge old", wx.DefaultPosition, wx.DefaultSize, 0 )
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

        self.m_filePicker1 = wx.FilePickerCtrl( self.mkvOptions, optionsFile, wx.EmptyString, "Select options file", "*.json*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer461.Add( self.m_filePicker1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


        bSizer11111.Add( bSizer461, 0, wx.EXPAND, 5 )

        bSizer12111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button9111 = wx.Button( self.mkvOptions, runOptions, "Run", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
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
        self.m_notebook30.AddPage( self.mkvOptions, "mkvOptions", False )
  
        self.translate = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4112 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText3212 = wx.StaticText( self.translate, wx.ID_ANY, "Subtitle translator", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3212.Wrap( -1 )

        bSizer4112.Add( self.m_staticText3212, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        self.m_staticText19 = wx.StaticText( self.translate, errorMissing, u"! translatesubs Library is missing", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText19.Wrap( -1 )

        self.m_staticText19.SetForegroundColour( wx.Colour( 179, 0, 0 ) )
        self.m_staticText19.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        
        try:
            import translatesubsx
            self.m_staticText19.Hide()
        except:
            print()

        bSizer6112 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel20112 = wx.Panel( self.translate, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer7212 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel7212 = wx.Panel( self.m_panel20112, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer5112 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel8212 = wx.Panel( self.m_panel7212, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        bSizer8212 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panel71112 = wx.Panel( self.m_panel8212, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer81112 = wx.BoxSizer( wx.VERTICAL )

        m_checkList1212Choices = []
        self.m_checkList1212 = wx.CheckListBox( self.m_panel71112, selectedFilesTranslate, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList1212Choices, 0 )
        self.m_checkList1212.DragAcceptFiles( true )
        self.m_checkList1212.SetMinSize( wx.Size( -1,200 ) )

        bSizer81112.Add( self.m_checkList1212, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_panel9112 = wx.Panel( self.m_panel71112, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer71112 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer71112.SetMinSize( wx.Size( -1,40 ) )
        self.m_button3112 = wx.Button( self.m_panel9112, browseFilesTranslate, "browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71112.Add( self.m_button3112, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button11212 = wx.Button( self.m_panel9112, browseFolderTranslate, "select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71112.Add( self.m_button11212, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button15112 = wx.Button( self.m_panel9112, selectAllTranslate, "Select all / none", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71112.Add( self.m_button15112, 1, wx.ALL|wx.EXPAND, 5 )
        self.m_button15112.Disable()

        self.m_button111112 = wx.Button( self.m_panel9112, dBtnTranslate, "Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71112.Add( self.m_button111112, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.m_button111112.Disable()


        self.m_panel9112.SetSizer( bSizer71112 )
        self.m_panel9112.Layout()
        bSizer71112.Fit( self.m_panel9112 )
        bSizer81112.Add( self.m_panel9112, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


        self.m_panel71112.SetSizer( bSizer81112 )
        self.m_panel71112.Layout()
        bSizer81112.Fit( self.m_panel71112 )
        bSizer8212.Add( self.m_panel71112, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel8212.SetSizer( bSizer8212 )
        self.m_panel8212.Layout()
        bSizer8212.Fit( self.m_panel8212 )
        bSizer5112.Add( self.m_panel8212, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 5 )


        self.m_panel7212.SetSizer( bSizer5112 )
        self.m_panel7212.Layout()
        bSizer5112.Fit( self.m_panel7212 )
        bSizer7212.Add( self.m_panel7212, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer431 = wx.BoxSizer( wx.HORIZONTAL )

        self.clearList21 = wx.CheckBox( self.m_panel20112, clearListTranslate, "Clear list after complete", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer431.Add( self.clearList21, 1, wx.ALL|wx.EXPAND, 5 )

        m_choice2Choices = languageCodes
        self.m_choice2 = wx.Choice( self.m_panel20112, translateTo, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
        self.m_choice2.SetSelection( 42 )
        bSizer431.Add( self.m_choice2, 0, wx.ALL, 5 )


        bSizer7212.Add( bSizer431, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.m_panel20112.SetSizer( bSizer7212 )
        self.m_panel20112.Layout()
        bSizer7212.Fit( self.m_panel20112 )
        bSizer6112.Add( self.m_panel20112, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer11112 = wx.BoxSizer( wx.VERTICAL )

        bSizer12112 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer12112.SetMinSize( wx.Size( -1,30 ) )
        self.m_button9112 = wx.Button( self.translate, runTranslate, "Translate", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
        bSizer12112.Add( self.m_button9112, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
        self.m_button9112.Disable()

        self.m_staticText31112 = wx.StaticText( self.translate, currentFileTranslate, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText31112.Wrap( -1 )

        bSizer12112.Add( self.m_staticText31112, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer11112.Add( bSizer12112, 0, wx.EXPAND, 5 )

        self.m_gauge1112 = wx.Gauge( self.translate, pBarTranslate, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
        self.m_gauge1112.SetValue( 0 )
        bSizer11112.Add( self.m_gauge1112, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer6112.Add( bSizer11112, 0, wx.EXPAND, 5 )


        bSizer4112.Add( bSizer6112, 1, wx.EXPAND, 5 )


        self.translate.SetSizer( bSizer4112 )
        self.translate.Layout()
        bSizer4112.Fit( self.translate )
        self.m_notebook30.AddPage( self.translate, "translate", True )

        self.Settings = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer41111 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText32111 = wx.StaticText( self.Settings, wx.ID_ANY, "Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText32111.Wrap( -1 )

        bSizer41111.Add( self.m_staticText32111, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_staticText21 = wx.StaticText( self.Settings, wx.ID_ANY, "Mkvtoolnix folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText21.Wrap( -1 )

        bSizer41111.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_dirPicker1 = wx.DirPickerCtrl( self.Settings, mkvDir, config['mkvtoolnix'], "Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        bSizer41111.Add( self.m_dirPicker1, 0, wx.ALL|wx.EXPAND, 5 )


        self.Settings.SetSizer( bSizer41111 )
        self.Settings.Layout()
        bSizer41111.Fit( self.Settings )
        self.m_notebook30.AddPage( self.Settings, "Settings", True )

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
        self.m_button3112.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("Translate") )
        self.m_button11212.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("Translate") )
        self.m_button15112.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("Translate") )
        self.m_button111112.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("Translate") )
        self.m_button9112.Bind( wx.EVT_BUTTON, lambda event: self.processThread("self.runTranslate"))
        self.m_filePicker1.Bind( wx.EVT_FILEPICKER_CHANGED, self.setRunEnable )
        self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.setMkvDir )

    def __del__( self ):
        pass
    
    def processThread( self, event ):
        process= eval(event)
        t = threading.Thread(target=process)
        t.daemon = True # set thread as daemon to terminate when main thread ends
        t.start()

    # Virtual event handlers, override them in your derived class
    def setMkvDir( self, event ):
        try:
            currentDir = wx.FindWindowById(mkvDir)
            newpath = currentDir.GetPath()
            config['mkvtoolnix'] = f"{newpath}"
            with open('config.json', 'w') as f:
                json.dump(config, f)
        except:
            print('')
  
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
            if event == "Options":
                    optionJson = wx.FindWindowById(optionsFile)
                    jsonFile = optionJson.GetPath()
                    if not os.path.exists(jsonFile):
                        wx.FindWindowById(eval(f"run{event}")).Disable()
        else:
            delBtnWindow.Disable() 
            buttonWindow.Disable() 
            selectAllWindow.Disable() 

    def openFilesSelector( self, event ):
        try:
            print(event)
            selectedFiles = eval(f"selectedFiles{event}")
            checkBoxListWindow = wx.FindWindowById(selectedFiles)
            oldFiles = checkBoxListWindow.GetItems() 
            fileTypeFilter = defaultFileTypeFillter
            if event=="Translate":
                fileTypeFilter = subtitleFileTypeFillter 
            openFileDialog = wx.FileDialog(self, "Select files", wildcard=fileTypeFilter,
               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE)
            openFileDialog.ShowModal()
            selectedFiles = openFileDialog.GetFilenames()
            allFiles = oldFiles + selectedFiles
            fileTypeList = defaultfileTypesList
            if event=="Translate":
                fileTypeList = subtitleFileTypeList
            allFiles = list(filter(lambda file: str(file).endswith(tuple(fileTypeList)),allFiles))
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
                if event == "Options":
                    optionJson = wx.FindWindowById(optionsFile)
                    jsonFile = optionJson.GetPath()
                    if not os.path.exists(jsonFile):
                        wx.FindWindowById(eval(f"run{event}")).Disable()
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
            fileTypeList = defaultfileTypesList
            if event=="Translate":
                fileTypeList = subtitleFileTypeList  
            filterFilesInDir = list(filter(lambda file: str(file).endswith(tuple(fileTypeList)),absFilesInDir))
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
                if event == "Options":
                    optionJson = wx.FindWindowById(optionsFile)
                    jsonFile = optionJson.GetPath()
                    if not os.path.exists(jsonFile):
                        wx.FindWindowById(eval(f"run{event}")).Disable()
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

    def setRunEnable(self, event):
        optionJson = wx.FindWindowById(optionsFile)
        jsonFile = optionJson.GetPath()
        runBtn = wx.FindWindowById(runOptions)
        if os.path.exists(jsonFile):
            runBtn.Enable()
        else:
            runBtn.Disable()

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
            bFilesWindow = wx.FindWindowById(browseFilesToMkv)
            bFoldersWindow = wx.FindWindowById(browseFolderToMkv)
            bSelectAllWindow = wx.FindWindowById(selectAllToMkv)
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
                # duplicateFiles = list(allFiles)
                convertTomkvWindow.Disable()
                bFilesWindow.Disable()
                bFoldersWindow.Disable()
                bSelectAllWindow.Disable()
                for index, file in enumerate(allFiles):
                    currentFile.SetLabel(str(file))
                    selectedDir = os.path.dirname(file)
                    fName = os.path.basename(file)
                    fNameNoExt = os.path.splitext(fName)[0]
                    if not os.path.exists((f"{mkvmergeDir}\\mkvmerge_old")):
                        os.makedirs((f"{mkvmergeDir}\\mkvmerge_old"))
                    mkvmerge_old = (f"{mkvmergeDir}\mkvmerge_old\\{fName}")
                    shutil.move(file, mkvmerge_old)
                    outputFile = f"{selectedDir}\\{fNameNoExt}.mkv"
                    inputFile = f"{mkvmergeDir}\\mkvmerge_old\\{fName}"
                    mkvCommand = f'"{mkvMerge}" --output "{outputFile}" "{inputFile}"'
                    presentage = int(100*(index+1)/indexes)
                    # print(presentage)
                    pBar.SetValue((presentage))
                    runCommand(mkvCommand)
            currentFile.SetLabel("")
            pBar.SetValue(0)
            checkBoxListWindow.SetItems([])
            bFilesWindow.Enable()
            bFoldersWindow.Enable()
        except Exception as e:
            print(e)
        
    def runToAudio( self ):
        try:
            bFilesWindow = wx.FindWindowById(browseFilesToAudio)
            bFoldersWindow = wx.FindWindowById(browseFolderToAudio)
            bSelectAllWindow = wx.FindWindowById(selectAllToAudio)
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
                # duplicateFiles = list(allFiles)
                convertToAudioWindow.Disable()
                bFilesWindow.Disable()
                bFoldersWindow.Disable()
                bSelectAllWindow.Disable()
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
                bSelectAllWindow.Enable()
            bFilesWindow.Enable()
            bFoldersWindow.Enable()
        except Exception as e:
            print(e)

    def runCrop( self ):
        try:
            bFilesWindow = wx.FindWindowById(browseFilesCrop)
            bFoldersWindow = wx.FindWindowById(browseFolderCrop)
            bSelectAllWindow = wx.FindWindowById(selectAllCrop)
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
                # duplicateFiles = list(allFiles)
                bFilesWindow.Disable()
                bFoldersWindow.Disable()
                bSelectAllWindow.Disable()
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
                bSelectAllWindow.Enable()
            bFilesWindow.Enable()
            bFoldersWindow.Enable()
        except Exception as e:
            print(e)
        
    def runOptions( self ):
        try:
            bFilesWindow = wx.FindWindowById(browseFilesOptions)
            bFoldersWindow = wx.FindWindowById(browseFolderOptions)
            bSelectAllWindow = wx.FindWindowById(selectAllOptions)
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
                    if "--output" in fileOptions: 
                        removeIndex = fileOptions.index('--output')
                        del fileOptions[removeIndex] # remove --output line
                        del fileOptions[removeIndex] # remove file line
                except ValueError:
                    print(e)  # item not in list
                try:
                    if '(' in fileOptions:
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
                    # duplicateFiles = list(allFiles)
                    convertOptionsWindow.Disable()
                    bFilesWindow.Disable()
                    bFoldersWindow.Disable()
                    bSelectAllWindow.Disable()
                    for index, file in enumerate(allFiles):
                        currentFile.SetLabel(str(file))
                        selectedDir = os.path.dirname(file)
                        fName = os.path.basename(file)
                        fNameNoExt = os.path.splitext(fName)[0]
                        print(fName,"dir=>",selectedDir)
                        if not os.path.exists((f"{mkvmergeDir}\\mkvmerge_old")):
                            os.makedirs((f"{mkvmergeDir}\\mkvmerge_old"))
                        mkvmerge_old = (f"{mkvmergeDir}\mkvmerge_old\\{fName}")
                        shutil.move(file, mkvmerge_old)
                        outputFile = f'{selectedDir}\\{fNameNoExt}.mkv'
                        inputfile = f'{mkvmergeDir}\\mkvmerge_old\\{fName}'
                        mkvCommand = f'"{mkvMerge}" @"{jsonFile}" -o "{outputFile}" "{inputfile}"'
                        print(mkvCommand)
                        presentage = int(100*(index+1)/indexes)
                        # print(presentage)
                        pBar.SetValue((presentage))
                        runCommand(mkvCommand)
                    currentFile.SetLabel("")
                    pBar.SetValue(0)
                    checkBoxListWindow.SetItems([])
                    bFilesWindow.Enable()
                    bFoldersWindow.Enable()
            else:
                currentFile.SetLabel("Please select options file first!")
        except Exception as e:
            print(traceback.format_exc())
        
    def runTranslate( self ):
        try:
            bFilesWindow = wx.FindWindowById(browseFilesTranslate)
            bFoldersWindow = wx.FindWindowById(browseFolderTranslate)
            bSelectAllWindow = wx.FindWindowById(selectAllTranslate)
            checkBoxListWindow = wx.FindWindowById(selectedFilesTranslate)
            currentFile = wx.FindWindowById(currentFileTranslate)
            selectedLangWindow = wx.FindWindowById(translateTo)
            selectedLangIndex = selectedLangWindow.GetSelection()
            selectedLang = languageCodes[selectedLangIndex]
            translateWindow = wx.FindWindowById(runTranslate)
            indexes = checkBoxListWindow.GetCount()
            pBar = wx.FindWindowById(pBarTranslate)
            clearListCheckbox = wx.FindWindowById(clearListTranslate)
            isClearChecked = clearListCheckbox.GetValue()
            # print(indexes)
            if indexes:
                allFiles = checkBoxListWindow.GetItems()
                translateWindow.Disable()
                bFilesWindow.Disable()
                bFoldersWindow.Disable()
                bSelectAllWindow.Disable()
                for index, file in enumerate(allFiles):
                    currentFile.SetLabel(str(file))
                    selectedDir = os.path.dirname(file)
                    fName = os.path.basename(file)
                    fNameNoExt = os.path.splitext(fName)[0]
                    fixIndex = 0
                    sourceFile = f"{selectedDir}\\{fName}"
                    outputFile = f"{selectedDir}\\{fNameNoExt}.{selectedLang}.srt"
                    while os.path.exists(outputFile):
                       fixIndex += 1 
                       outputFile = f"{selectedDir}\\{fNameNoExt}.{selectedLang} ({fixIndex}).srt"
                    translateCommand = f"translatesubs \"{sourceFile}\" \"{outputFile}\" --to_lang {selectedLang}"
                    presentage = int(100*(index+1)/indexes)
                    pBar.SetValue((presentage))
                    runCommand(translateCommand)
            currentFile.SetLabel("")
            pBar.SetValue(0)
            if isClearChecked:
                checkBoxListWindow.SetItems([])
            else:
                translateWindow.Enable()
                bSelectAllWindow.Enable()
            bFilesWindow.Enable()
            bFoldersWindow.Enable()
        except Exception as e:
            print(e)

        
class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window,tab):
        super().__init__()
        self.m_checkList1 = window
        self.tab = tab

    def OnDropFiles(self, x, y, filenames):
        allFiles = filenames
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
            fileTypesList = toMkvtfileTypesList
        elif self.tab == "Translate":
            fileTypesList = subtitleFileTypeList
        else:
            fileTypesList = defaultfileTypesList
        allFiles = list(filter(lambda file: str(file).endswith(tuple(fileTypesList)),allFiles))
        checkBoxList.Set(allFiles)
        selectAllId = eval(f"selectAll{self.tab}")
        selectAllWindow = wx.FindWindowById(selectAllId)
        if len(allFiles):
            buttonWindow = wx.FindWindowById(buttonId)
            buttonWindow.Enable()
            selectAllWindow.Enable()
            if self.tab == "Options":
                optionJson = wx.FindWindowById(optionsFile)
                jsonFile = optionJson.GetPath()
                if not os.path.exists(jsonFile):
                    wx.FindWindowById(eval(f"run{self.tab}")).Disable()
        return True

def runCommand(cmd, timeout=None, window=None):
    # cmd = cmd.replace("\\","/")
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,encoding='utf-8'
    )
    output = ""
    for line in p.stdout:
        output += line
        print(line)
        window.Refresh() if window else None  # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)

wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False)
frame = MyFrame1(None)
wx.FindWindowById(tabContainer).SetSelection(0)
frame.m_checkList1.SetDropTarget(MyFileDropTarget(frame.m_checkList1,"ToMkv"))
frame.m_checkList12.SetDropTarget(MyFileDropTarget(frame.m_checkList12,"ToAudio"))
frame.m_checkList121.SetDropTarget(MyFileDropTarget(frame.m_checkList121,"Crop"))
frame.m_checkList1211.SetDropTarget(MyFileDropTarget(frame.m_checkList1211,"Options"))
frame.m_checkList1212.SetDropTarget(MyFileDropTarget(frame.m_checkList1212,"Translate"))
frame.Show(True)
app.MainLoop()