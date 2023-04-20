# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-282-g1fa54006)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

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
selectedFilesCorp = 1020
browseFilesCorp = 1021
browseFolderCorp = 1022
selectAllCorp = 1023
dBtnCorp = 1024
fileTypesCorp = 1025
allCorp = 1026
cTop = 1027
cRight = 1028
cBottom = 1029
cLeft = 1030
corpVideo = 1031
currentFileCorp = 1032
pBarCorp = 1033

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
		self.corp = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer411 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText321 = wx.StaticText( self.corp, wx.ID_ANY, u"corp video", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText321.Wrap( -1 )

		bSizer411.Add( self.m_staticText321, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		bSizer611 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel2011 = wx.Panel( self.corp, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer721 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel721 = wx.Panel( self.m_panel2011, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer511 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel821 = wx.Panel( self.m_panel721, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer821 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel7111 = wx.Panel( self.m_panel821, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8111 = wx.BoxSizer( wx.HORIZONTAL )

		m_checkList121Choices = []
		self.m_checkList121 = wx.CheckListBox( self.m_panel7111, selectedFilesCorp, wx.DefaultPosition, wx.Size( 480,-1 ), m_checkList121Choices, 0 )
		self.m_checkList121.DragAcceptFiles( true )

		bSizer8111.Add( self.m_checkList121, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_panel911 = wx.Panel( self.m_panel7111, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7111 = wx.BoxSizer( wx.VERTICAL )

		self.m_button311 = wx.Button( self.m_panel911, browseFilesCorp, u"browse files", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7111.Add( self.m_button311, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_button1121 = wx.Button( self.m_panel911, browseFolderCorp, u"select folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7111.Add( self.m_button1121, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button1511 = wx.Button( self.m_panel911, selectAllCorp, u"Select all", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7111.Add( self.m_button1511, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button11111 = wx.Button( self.m_panel911, dBtnCorp, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7111.Add( self.m_button11111, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


		self.m_panel911.SetSizer( bSizer7111 )
		self.m_panel911.Layout()
		bSizer7111.Fit( self.m_panel911 )
		bSizer8111.Add( self.m_panel911, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_panel8111 = wx.Panel( self.m_panel7111, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer911 = wx.BoxSizer( wx.VERTICAL )

		m_checkList1111Choices = [u"mkv", u"ts", u"mp4", u"avi", u"webm", u"flv", u"ogg", u"mov", u"mpeg-2"]
		self.m_checkList1111 = wx.CheckListBox( self.m_panel8111, fileTypesCorp, wx.DefaultPosition, wx.DefaultSize, m_checkList1111Choices, 0 )
		self.m_checkList1111.DragAcceptFiles( true )

		bSizer911.Add( self.m_checkList1111, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button711 = wx.Button( self.m_panel8111, allCorp, u"check all", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
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

		self.m_staticText15 = wx.StaticText( self.corp, wx.ID_ANY, u"Top", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		bSizer46.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self.corp, cTop, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText16 = wx.StaticText( self.corp, wx.ID_ANY, u"Right", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer46.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl3 = wx.TextCtrl( self.corp, cRight, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.m_textCtrl3, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText17 = wx.StaticText( self.corp, wx.ID_ANY, u"Bottom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		bSizer46.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl4 = wx.TextCtrl( self.corp, cBottom, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.m_textCtrl4, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText18 = wx.StaticText( self.corp, wx.ID_ANY, u"Left", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		bSizer46.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl5 = wx.TextCtrl( self.corp, cLeft, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.m_textCtrl5, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1111.Add( bSizer46, 1, wx.EXPAND, 5 )

		bSizer1211 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button911 = wx.Button( self.corp, corpVideo, u"Corp", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		bSizer1211.Add( self.m_button911, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText3111 = wx.StaticText( self.corp, currentFileCorp, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3111.Wrap( -1 )

		bSizer1211.Add( self.m_staticText3111, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1111.Add( bSizer1211, 1, wx.EXPAND, 5 )

		self.m_gauge111 = wx.Gauge( self.corp, pBarCorp, 100, wx.DefaultPosition, wx.Size( -1,30 ), wx.GA_HORIZONTAL )
		self.m_gauge111.SetValue( 0 )
		bSizer1111.Add( self.m_gauge111, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer611.Add( bSizer1111, 1, wx.EXPAND, 5 )


		bSizer411.Add( bSizer611, 1, wx.EXPAND, 5 )


		self.corp.SetSizer( bSizer411 )
		self.corp.Layout()
		bSizer411.Fit( self.corp )
		self.m_notebook30.AddPage( self.corp, u"corp", True )

		bSizer2.Add( self.m_notebook30, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()


		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button3.Bind( wx.EVT_BUTTON, self.openFilesSelector("ToMkv") )
		self.m_button11.Bind( wx.EVT_BUTTON, self.selectFolder("ToMkv") )
		self.m_button15.Bind( wx.EVT_BUTTON, self.selectAll("ToMkv") )
		self.m_button111.Bind( wx.EVT_BUTTON, self.deleteFromList("ToMkv") )
		self.m_button7.Bind( wx.EVT_BUTTON, self.checkAllTypes("ToMkv") )
		self.m_button9.Bind( wx.EVT_BUTTON, self.convertToMkv )
		self.m_button31.Bind( wx.EVT_BUTTON, self.openFilesSelector("ToAudio") )
		self.m_button112.Bind( wx.EVT_BUTTON, self.selectFolder("ToAudio") )
		self.m_button151.Bind( wx.EVT_BUTTON, self.selectAll("ToAudio") )
		self.m_button1111.Bind( wx.EVT_BUTTON, self.deleteFromList("ToAudio") )
		self.m_button71.Bind( wx.EVT_BUTTON, self.checkAllTypes("ToAudio") )
		self.m_button91.Bind( wx.EVT_BUTTON, self.convertToAudio )
		self.m_button311.Bind( wx.EVT_BUTTON, self.openFilesSelector("Corp") )
		self.m_button1121.Bind( wx.EVT_BUTTON, self.selectFolder("Corp") )
		self.m_button1511.Bind( wx.EVT_BUTTON, self.selectAll("Corp") )
		self.m_button11111.Bind( wx.EVT_BUTTON, self.deleteFromList("Corp") )
		self.m_button711.Bind( wx.EVT_BUTTON, self.checkAllTypes("Corp") )
		self.m_button911.Bind( wx.EVT_BUTTON, self.corpVideo )

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

	def checkAllTypes("ToMkv")( self, event ):
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

	def checkAllTypes("ToAudio")( self, event ):
		event.Skip()

	def convertToAudio( self, event ):
		event.Skip()

	def openFilesSelector("Corp")( self, event ):
		event.Skip()

	def selectFolder("Corp")( self, event ):
		event.Skip()

	def selectAll("Corp")( self, event ):
		event.Skip()

	def deleteFromList("Corp")( self, event ):
		event.Skip()

	def checkAllTypes("Corp")( self, event ):
		event.Skip()

	def corpVideo( self, event ):
		event.Skip()


