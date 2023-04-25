# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-282-g1fa54006)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

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

	def __del__( self ):
		pass


