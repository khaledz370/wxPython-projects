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
fajrTime = 1001
dhuhrLabel = 1002
dhuhrTime = 1003
asrLabel = 1004
asrTime = 1005
maghribLabel = 1006
maghribTime = 1007
ishaLabel = 1008
ishaTime = 1009
todayDate = 1010
nextPrayerName = 1011
nextPrayerTime = 1012
latValue = 1013
longValue = 1014
timeZoneValue = 1015
methodValue = 1016
asrValue = 1017
dhuhrValue = 1018
fajrValue = 1019
maghribValue = 1020
ishaValue = 1021
minimized = 1022
trValue = 1023

###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 358,356 ), style = 0 )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Prayer times", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer1.Add( self.m_staticText1, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		fajr_row = wx.BoxSizer( wx.HORIZONTAL )

		self.fajr_text = wx.StaticText( self, fajrLabel, u"Fajr", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fajr_text.Wrap( -1 )

		self.fajr_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.fajr_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		fajr_row.Add( self.fajr_text, 1, wx.ALL|wx.EXPAND, 10 )

		self.fajr_time = wx.StaticText( self, fajrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.fajr_time.Wrap( -1 )

		self.fajr_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.fajr_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		fajr_row.Add( self.fajr_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10 )


		bSizer8.Add( fajr_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

		dhuhr_row = wx.BoxSizer( wx.HORIZONTAL )

		self.dhuhr_text = wx.StaticText( self, dhuhrLabel, u"Dhuhr", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.dhuhr_text.Wrap( -1 )

		self.dhuhr_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.dhuhr_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		dhuhr_row.Add( self.dhuhr_text, 1, wx.ALL|wx.EXPAND, 10 )

		self.dhuhr_time = wx.StaticText( self, dhuhrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.dhuhr_time.Wrap( -1 )

		self.dhuhr_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.dhuhr_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		dhuhr_row.Add( self.dhuhr_time, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.ALL, 10 )


		bSizer8.Add( dhuhr_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

		asrt_row = wx.BoxSizer( wx.HORIZONTAL )

		self.asr_text = wx.StaticText( self, asrLabel, u"Asr", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.asr_text.Wrap( -1 )

		self.asr_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.asr_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		asrt_row.Add( self.asr_text, 1, wx.ALL|wx.EXPAND, 10 )

		self.asr_time = wx.StaticText( self, asrTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.asr_time.Wrap( -1 )

		self.asr_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.asr_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		asrt_row.Add( self.asr_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 10 )


		bSizer8.Add( asrt_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

		maghrib_row = wx.BoxSizer( wx.HORIZONTAL )

		self.maghrib_text = wx.StaticText( self, maghribLabel, u"Maghrib", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.maghrib_text.Wrap( -1 )

		self.maghrib_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.maghrib_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		maghrib_row.Add( self.maghrib_text, 1, wx.ALL|wx.EXPAND, 10 )

		self.maghrib_time = wx.StaticText( self, maghribTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.maghrib_time.Wrap( -1 )

		self.maghrib_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.maghrib_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		maghrib_row.Add( self.maghrib_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 10 )


		bSizer8.Add( maghrib_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )

		isha_row = wx.BoxSizer( wx.HORIZONTAL )

		self.isha_text = wx.StaticText( self, ishaLabel, u"Isha", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.isha_text.Wrap( -1 )

		self.isha_text.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.isha_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		isha_row.Add( self.isha_text, 1, wx.ALL|wx.EXPAND, 10 )

		self.isha_time = wx.StaticText( self, ishaTime, u"00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.isha_time.Wrap( -1 )

		self.isha_time.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.isha_time.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

		isha_row.Add( self.isha_time, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 10 )


		bSizer8.Add( isha_row, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 20 )


		bSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )

		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel3.SetMaxSize( wx.Size( -1,100 ) )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText8 = wx.StaticText( self.m_panel3, todayDate, u"00-00-0000, 00:00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText8.Wrap( -1 )

		self.m_staticText8.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer6.Add( self.m_staticText8, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

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

		bSizer71.Add( self.m_staticText101, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_staticText111 = wx.StaticText( self.m_panel3, nextPrayerTime, u"00:00:00", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText111.Wrap( -1 )

		self.m_staticText111.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer71.Add( self.m_staticText111, 1, wx.ALL|wx.EXPAND, 5 )


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


###########################################################################
## Class Settings
###########################################################################

class Settings ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,238 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText17.Wrap( -1 )

		self.m_staticText17.SetFont( wx.Font( 16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer15.Add( self.m_staticText17, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer14.Add( bSizer15, 1, wx.EXPAND, 5 )

		bSizer151 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Lat:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		bSizer151.Add( self.m_staticText18, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.latValue = wx.SpinCtrlDouble( self, latValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 2.000000, 1 )
		self.latValue.SetDigits( 3 )
		bSizer151.Add( self.latValue, 1, wx.ALL|wx.EXPAND, 5 )

		self.Long = wx.StaticText( self, wx.ID_ANY, u"Long:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Long.Wrap( -1 )

		bSizer151.Add( self.Long, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.LongValue = wx.SpinCtrlDouble( self, longValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0.000000, 1 )
		self.LongValue.SetDigits( 3 )
		bSizer151.Add( self.LongValue, 1, wx.ALL|wx.EXPAND, 5 )

		self.timeZone = wx.StaticText( self, wx.ID_ANY, u"TimeZone:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.timeZone.Wrap( -1 )

		bSizer151.Add( self.timeZone, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_spinCtrl1 = wx.SpinCtrl( self, timeZoneValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, -12, 12, 0 )
		bSizer151.Add( self.m_spinCtrl1, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer14.Add( bSizer151, 1, wx.EXPAND, 5 )

		bSizer152 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Method:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		bSizer152.Add( self.m_staticText20, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		methodsChoices = [ u"MWL", u"ISNA", u"Egypt", u"Makkah", u"Karachi", u"Tehran", u"Jafari" ]
		self.methods = wx.Choice( self, methodValue, wx.DefaultPosition, wx.DefaultSize, methodsChoices, 0 )
		self.methods.SetSelection( 0 )
		bSizer152.Add( self.methods, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Asr method:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer152.Add( self.m_staticText21, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choice2Choices = [ u"Standard", u"Hanafi" ]
		self.m_choice2 = wx.Choice( self, asrValue, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
		self.m_choice2.SetSelection( 0 )
		bSizer152.Add( self.m_choice2, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"Dhuhr:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )

		bSizer152.Add( self.m_staticText28, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_spinCtrl2 = wx.SpinCtrl( self, dhuhrValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 60, 0 )
		bSizer152.Add( self.m_spinCtrl2, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer14.Add( bSizer152, 1, wx.EXPAND, 5 )

		bSizer153 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"Fajr:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		bSizer153.Add( self.m_staticText22, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_spinCtrlDouble3 = wx.SpinCtrlDouble( self, fajrValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 30.500000, 0.5 )
		self.m_spinCtrlDouble3.SetDigits( 2 )
		bSizer153.Add( self.m_spinCtrlDouble3, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"Deg", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )

		bSizer153.Add( self.m_staticText24, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Maghrib:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )

		bSizer153.Add( self.m_staticText25, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_spinCtrlDouble5 = wx.SpinCtrlDouble( self, maghribValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0, 1 )
		self.m_spinCtrlDouble5.SetDigits( 0 )
		bSizer153.Add( self.m_spinCtrlDouble5, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Deg", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		bSizer153.Add( self.m_staticText27, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Isha:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )

		bSizer153.Add( self.m_staticText23, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_spinCtrlDouble4 = wx.SpinCtrlDouble( self, ishaValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0, 1 )
		self.m_spinCtrlDouble4.SetDigits( 0 )
		bSizer153.Add( self.m_spinCtrlDouble4, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"Deg", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )

		bSizer153.Add( self.m_staticText26, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer14.Add( bSizer153, 1, wx.EXPAND, 5 )

		bSizer155 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_checkBox1 = wx.CheckBox( self, minimized, u"hide on start", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox1.SetValue(True)
		bSizer155.Add( self.m_checkBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, u"Transparency", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		bSizer155.Add( self.m_staticText29, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_spinCtrl3 = wx.SpinCtrl( self, trValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 500, 300 )
		bSizer155.Add( self.m_spinCtrl3, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer14.Add( bSizer155, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		bSizer154 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer154.Add( self.m_button1, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer154.Add( self.m_button2, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer14.Add( bSizer154, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer14 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button1.Bind( wx.EVT_BUTTON, self.setDefault )
		self.m_button2.Bind( wx.EVT_BUTTON, self.saveSettings )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def setDefault( self, event ):
		event.Skip()

	def saveSettings( self, event ):
		event.Skip()


