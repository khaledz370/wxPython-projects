# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-282-g1fa54006)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

tabContainer = 1000
selectedFilesToMkv = 1001
browseFilesToMkv = 1002
browseFolderToMkv = 1003
selectAllToMkv = 1004
dBtnToMkv = 1005
mkvmergeTomkv = 1006
mkvmergeOldFolderToMkv = 1007
convertToMkv = 1008
currentFileToMkv = 1009
pBarToMkv = 1010
selectedFilesToAudio = 1011
browseFilesToAudio = 1012
browseFolderToAudio = 1013
selectAllToAudio = 1014
dBtnToAudio = 1015
clearListToAudio = 1016
convertToAudio = 1017
currentFileToAudio = 1018
pBarToAudio = 1019
selectedFilesCrop = 1020
browseFilesCrop = 1021
browseFolderCrop = 1022
selectAllCrop = 1023
dBtnCrop = 1024
clearListCrop = 1025
cTop = 1026
cRight = 1027
cBottom = 1028
cLeft = 1029
cropVideo = 1030
currentFileCrop = 1031
pBarCrop = 1032
selectedFilesOptions = 1033
browseFilesOptions = 1034
browseFolderOptions = 1035
mkvmergeOptions = 1036
selectAllOptions = 1037
dBtnOptions = 1038
clearListOptions = 1039
mkvmergeOldFolderOptions = 1040
optionsFile = 1041
runOption = 1042
currentFileOptions = 1043
pBarOptions = 1044
errorMissing = 1045
selectedFilesTranslate = 1046
browseFilesTranslate = 1047
selectAllTranslate = 1048
dBtnTranslate = 1049
clearListTranslate = 1050
translateTo = 1051
runTranslate = 1052
currentFileTranslate = 1053
pBarTranslate = 1054
mkvDir = 1055

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 660,590 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 660,440 ), wx.Size( 660,700 ) )

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
		self.m_checkList1 = wx.CheckListBox( self.m_panel71, selectedFilesToMkv, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList1Choices, 0 )
		self.m_checkList1.DragAcceptFiles( true )
		self.m_checkList1.SetMinSize( wx.Size( -1,230 ) )

		bSizer81.Add( self.m_checkList1, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_panel9 = wx.Panel( self.m_panel71, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

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

		self.m_staticText13 = wx.StaticText( self.m_panel20, mkvmergeOldFolderToMkv, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
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

		self.m_button9 = wx.Button( self.tomkv, convertToMkv, u"Convert to mkv", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		bSizer12.Add( self.m_button9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

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
		self.m_notebook30.AddPage( self.tomkv, u"to mkv", False )
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
		self.m_checkList12 = wx.CheckListBox( self.m_panel711, selectedFilesToAudio, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList12Choices, 0 )
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

		self.m_button151 = wx.Button( self.m_panel91, selectAllToAudio, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer711.Add( self.m_button151, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button1111 = wx.Button( self.m_panel91, dBtnToAudio, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer711.Add( self.m_button1111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


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
		self.m_button91 = wx.Button( self.toAudio, convertToAudio, u"Convert to audio", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		bSizer121.Add( self.m_button91, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

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
		self.m_checkList121 = wx.CheckListBox( self.m_panel7111, selectedFilesCrop, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList121Choices, 0 )
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

		self.m_button1511 = wx.Button( self.m_panel911, selectAllCrop, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7111.Add( self.m_button1511, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button11111 = wx.Button( self.m_panel911, dBtnCrop, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7111.Add( self.m_button11111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


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
		self.m_button911 = wx.Button( self.crop, cropVideo, u"Crop", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		bSizer1211.Add( self.m_button911, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

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
		self.m_checkList1211 = wx.CheckListBox( self.m_panel71111, selectedFilesOptions, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList1211Choices, 0|wx.HSCROLL )
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

		self.m_button212 = wx.Button( self.m_panel9111, mkvmergeOptions, u"mkvmerge old", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71111.Add( self.m_button212, 0, wx.ALL, 5 )

		self.m_button15111 = wx.Button( self.m_panel9111, selectAllOptions, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71111.Add( self.m_button15111, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button111111 = wx.Button( self.m_panel9111, dBtnOptions, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71111.Add( self.m_button111111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


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

		self.clearList3 = wx.CheckBox( self.m_panel20111, clearListOptions, u"Clear list after complete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer421.Add( self.clearList3, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button2111 = wx.Button( self.m_panel20111, mkvmergeOptions, u"mkvmerge old", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer421.Add( self.m_button2111, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText131 = wx.StaticText( self.m_panel20111, mkvmergeOldFolderOptions, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )

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

		self.m_button9111 = wx.Button( self.mkvOptions, runOption, u"Run", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		bSizer12111.Add( self.m_button9111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

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
		self.translate = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4112 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3212 = wx.StaticText( self.translate, wx.ID_ANY, u"Subtitle translator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3212.Wrap( -1 )

		bSizer4112.Add( self.m_staticText3212, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( self.translate, errorMissing, u"! translatesubs Library is missing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		self.m_staticText19.SetForegroundColour( wx.Colour( 179, 0, 0 ) )
		self.m_staticText19.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

		bSizer4112.Add( self.m_staticText19, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

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
		self.m_button3112 = wx.Button( self.m_panel9112, browseFilesTranslate, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71112.Add( self.m_button3112, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_button11212 = wx.Button( self.m_panel9112, browseFolderCrop, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71112.Add( self.m_button11212, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button15112 = wx.Button( self.m_panel9112, selectAllTranslate, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71112.Add( self.m_button15112, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button111112 = wx.Button( self.m_panel9112, dBtnTranslate, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71112.Add( self.m_button111112, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


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

		self.clearList21 = wx.CheckBox( self.m_panel20112, clearListTranslate, u"Clear list after complete", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.clearList21.SetValue(True)
		bSizer431.Add( self.clearList21, 1, wx.ALL|wx.EXPAND, 5 )

		m_choice2Choices = [ u"aa", u"ab", u"af", u"ak", u"sq", u"am", u"ar", u"an", u"hy", u"as", u"av", u"ae", u"ay", u"az", u"ba", u"bm", u"eu", u"be", u"bn", u"bh", u"bi", u"bs", u"br", u"bg", u"my", u"ca", u"km", u"ch", u"ce", u"ny", u"zh", u"cu", u"cv", u"kw", u"co", u"cr", u"hr", u"cs", u"da", u"dv", u"nl", u"dz", u"en", u"eo", u"et", u"ee", u"fo", u"fj", u"fi", u"fr", u"fy", u"ff", u"ka", u"de", u"gd", u"ga", u"gl", u"gv", u"el", u"gn", u"gu", u"ht", u"ha", u"he", u"hz", u"hi", u"ho", u"hr", u"hu", u"ig", u"is", u"io", u"ii", u"iu", u"ie", u"ia", u"id", u"ik", u"it", u"jv", u"ja", u"kl", u"kn", u"ks", u"kr", u"kk", u"km", u"ki", u"rw", u"ky", u"kv", u"kg", u"ko", u"ku", u"kj", u"la", u"lb", u"lg", u"li", u"ln", u"lo", u"lt", u"lu", u"lv", u"gv", u"mk", u"mg", u"ms", u"ml", u"mt", u"mi", u"mr", u"mh", u"mn", u"na", u"nv", u"nb", u"nd", u"ne", u"ng", u"nn", u"no", u"ii", u"nr", u"oc", u"oj", u"cu", u"om", u"or", u"os", u"pa", u"pi", u"fa", u"pl", u"ps", u"pt", u"qu", u"rm", u"ro", u"rn", u"ru", u"sg", u"sa", u"si", u"sk", u"sl", u"se", u"sm", u"sn", u"sd", u"so", u"st", u"es", u"sc", u"sr", u"ss", u"su", u"sw", u"sv", u"ty", u"ta", u"tt", u"te", u"tg", u"tl", u"th", u"bo", u"ti", u"to", u"tn", u"ts", u"tk", u"tr", u"tw", u"ug", u"uk", u"ur", u"uz", u"ve", u"vi", u"vo", u"cy", u"wa", u"wo", u"xh", u"yi", u"yo", u"za", u"zu" ]
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
		self.m_button9112 = wx.Button( self.translate, runTranslate, u"Translate", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		bSizer12112.Add( self.m_button9112, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

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
		self.m_notebook30.AddPage( self.translate, u"translate", True )
		self.Settings = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41111 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText32111 = wx.StaticText( self.Settings, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32111.Wrap( -1 )

		bSizer41111.Add( self.m_staticText32111, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( self.Settings, wx.ID_ANY, u"Mkvtoolnix folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer41111.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_dirPicker1 = wx.DirPickerCtrl( self.Settings, mkvDir, u"C:\\Program Files\\MKVToolNix", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer41111.Add( self.m_dirPicker1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText20 = wx.StaticText( self.Settings, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		bSizer41111.Add( self.m_staticText20, 0, wx.ALL, 5 )


		self.Settings.SetSizer( bSizer41111 )
		self.Settings.Layout()
		bSizer41111.Fit( self.Settings )
		self.m_notebook30.AddPage( self.Settings, u"Settings", False )

		bSizer2.Add( self.m_notebook30, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()


		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button3.Bind( wx.EVT_BUTTON, self.openFilesSelector("ToMkv") )
		self.m_button11.Bind( wx.EVT_BUTTON, self.selectFolder("ToMkv") )
		self.m_button15.Bind( wx.EVT_BUTTON, self.selectAll("ToMkv") )
		self.m_button111.Bind( wx.EVT_BUTTON, self.deleteFromList("ToMkv") )
		self.m_button211.Bind( wx.EVT_BUTTON, self.setMkvMergeFolder )
		self.m_button9.Bind( wx.EVT_BUTTON, self.convertToMkv )
		self.m_button31.Bind( wx.EVT_BUTTON, self.openFilesSelector("ToAudio") )
		self.m_button112.Bind( wx.EVT_BUTTON, self.selectFolder("ToAudio") )
		self.m_button151.Bind( wx.EVT_BUTTON, self.selectAll("ToAudio") )
		self.m_button1111.Bind( wx.EVT_BUTTON, self.deleteFromList("ToAudio") )
		self.m_button91.Bind( wx.EVT_BUTTON, self.convertToAudio )
		self.m_button311.Bind( wx.EVT_BUTTON, self.openFilesSelector("Crop") )
		self.m_button1121.Bind( wx.EVT_BUTTON, self.selectFolder("Crop") )
		self.m_button1511.Bind( wx.EVT_BUTTON, self.selectAll("Crop") )
		self.m_button11111.Bind( wx.EVT_BUTTON, self.deleteFromList("Crop") )
		self.m_button911.Bind( wx.EVT_BUTTON, self.cropVideo )
		self.m_button3111.Bind( wx.EVT_BUTTON, self.openFilesSelector("Options") )
		self.m_button11211.Bind( wx.EVT_BUTTON, self.selectFolder("Options") )
		self.m_button212.Bind( wx.EVT_BUTTON, self.setMkvMergeFolder )
		self.m_button15111.Bind( wx.EVT_BUTTON, self.selectAll("Options") )
		self.m_button111111.Bind( wx.EVT_BUTTON, self.deleteFromList("Options") )
		self.m_button2111.Bind( wx.EVT_BUTTON, self.setMkvMergeFolder )
		self.m_filePicker1.Bind( wx.EVT_FILEPICKER_CHANGED, self.setRunEnable )
		self.m_button9111.Bind( wx.EVT_BUTTON, self.runWithJson )
		self.m_button3112.Bind( wx.EVT_BUTTON, self.openFilesSelector("Crop") )
		self.m_button11212.Bind( wx.EVT_BUTTON, self.selectFolder("Crop") )
		self.m_button15112.Bind( wx.EVT_BUTTON, self.selectAll("Crop") )
		self.m_button111112.Bind( wx.EVT_BUTTON, self.deleteFromList("Crop") )
		self.m_button9112.Bind( wx.EVT_BUTTON, self.runTranslate )
		self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.setMkvDir )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def openFilesSelector("ToMkv")( self, event ):
		event.Skip()

	def selectFolder("ToMkv")( self, event ):
		event.Skip()

	def selectAll("ToMkv")( self, event ):
		event.Skip()

	def deleteFromList("ToMkv")( self, event ):
		event.Skip()

	def setMkvMergeFolder( self, event ):
		event.Skip()

	def convertToMkv( self, event ):
		event.Skip()

	def openFilesSelector("ToAudio")( self, event ):
		event.Skip()

	def selectFolder("ToAudio")( self, event ):
		event.Skip()

	def selectAll("ToAudio")( self, event ):
		event.Skip()

	def deleteFromList("ToAudio")( self, event ):
		event.Skip()

	def convertToAudio( self, event ):
		event.Skip()

	def openFilesSelector("Crop")( self, event ):
		event.Skip()

	def selectFolder("Crop")( self, event ):
		event.Skip()

	def selectAll("Crop")( self, event ):
		event.Skip()

	def deleteFromList("Crop")( self, event ):
		event.Skip()

	def cropVideo( self, event ):
		event.Skip()

	def openFilesSelector("Options")( self, event ):
		event.Skip()

	def selectFolder("Options")( self, event ):
		event.Skip()


	def selectAll("Options")( self, event ):
		event.Skip()

	def deleteFromList("Options")( self, event ):
		event.Skip()


	def setRunEnable( self, event ):
		event.Skip()

	def runWithJson( self, event ):
		event.Skip()





	def runTranslate( self, event ):
		event.Skip()

	def setMkvDir( self, event ):
		event.Skip()


