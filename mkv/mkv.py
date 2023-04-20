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
currentFileTomkv = 1008
pBarToMkv = 1009

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 760,462 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook30 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tomkv = wx.Panel( self.m_notebook30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self.tomkv, wx.ID_ANY, u"Convert video to mkv", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer4.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self.tomkv, wx.ID_ANY, u"Drop files here", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer4.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

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

		self.m_button9 = wx.Button( self.tomkv, convertToMkv, u"Convert to mkv", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button9, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText31 = wx.StaticText( self.tomkv, currentFileTomkv, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer12.Add( self.m_staticText31, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer11.Add( bSizer12, 1, wx.EXPAND, 5 )

		self.m_gauge1 = wx.Gauge( self.tomkv, pBarToMkv, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 )
		bSizer11.Add( self.m_gauge1, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer6.Add( bSizer11, 1, wx.EXPAND, 5 )


		bSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )


		self.tomkv.SetSizer( bSizer4 )
		self.tomkv.Layout()
		bSizer4.Fit( self.tomkv )
		self.m_notebook30.AddPage( self.tomkv, u"to mkv", True )

		bSizer2.Add( self.m_notebook30, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()


		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button3.Bind( wx.EVT_BUTTON, self.openFilesSelector )
		self.m_button11.Bind( wx.EVT_BUTTON, self.selectFolder )
		self.m_button15.Bind( wx.EVT_BUTTON, self.selectAll )
		self.m_button111.Bind( wx.EVT_BUTTON, self.deleteToMkv )
		self.m_button7.Bind( wx.EVT_BUTTON, self.checkAllTypes )
		self.m_button9.Bind( wx.EVT_BUTTON, self.convertToMkv )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def openFilesSelector( self, event ):
		event.Skip()

	def selectFolder( self, event ):
		event.Skip()

	def selectAll( self, event ):
		event.Skip()

	def deleteToMkv( self, event ):
		event.Skip()

	def checkAllTypes( self, event ):
		event.Skip()

	def convertToMkv( self, event ):
		event.Skip()


