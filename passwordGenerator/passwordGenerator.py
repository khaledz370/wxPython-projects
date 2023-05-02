# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-282-g1fa54006)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

passLength = 1000
symbols = 1001
numbers = 1002
lowerCase = 1003
quantity = 1004
uperCase = 1005
ambiguousChar = 1006
noDuplicates = 1007
passwordTxt = 1008

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 650,340 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 650,340 ), wx.Size( 650,340 ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.title = wx.StaticText( self, wx.ID_ANY, u"Password Generator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.title.Wrap( -1 )

		bSizer1.Add( self.title, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8.SetMinSize( wx.Size( 600,200 ) )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.Password_length = wx.StaticText( self, wx.ID_ANY, u"Password Length:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Password_length.Wrap( -1 )

		bSizer11.Add( self.Password_length, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		Password_lengthChoices = []
		self.Password_length = wx.ComboBox( self, passLength, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, Password_lengthChoices, 0 )
		bSizer11.Add( self.Password_length, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer10.Add( bSizer11, 1, wx.EXPAND, 5 )

		self.symbols = wx.CheckBox( self, symbols, u"Include Symbols: ( e.g. @#$% )", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.symbols, 1, wx.ALL|wx.EXPAND, 5 )

		self.numbers = wx.CheckBox( self, numbers, u"Include Numbers: ( e.g. 123456 )", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.numbers, 1, wx.ALL|wx.EXPAND, 5 )

		self.lowerCase = wx.CheckBox( self, lowerCase, u"Include Lowercase Characters: ( e.g. abcdefgh )", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.lowerCase, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer8.Add( bSizer10, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		self.quantity1 = wx.StaticText( self, wx.ID_ANY, u"quantity", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.quantity1.Wrap( -1 )

		bSizer17.Add( self.quantity1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		quantityChoices = []
		self.quantity = wx.ComboBox( self, quantity, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, quantityChoices, 0 )
		bSizer17.Add( self.quantity, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer12.Add( bSizer17, 1, wx.EXPAND, 5 )

		self.uperCase = wx.CheckBox( self, uperCase, u"Include Uppercase Characters:  ( e.g. ABCDEFGH )", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.uperCase, 1, wx.ALL|wx.EXPAND, 5 )

		self.ambiguousChar = wx.CheckBox( self, ambiguousChar, u"Exclude Ambiguous Characters:  ( { } [ ] ( ) /  ' \" ` ~ , ; : . < > )", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.ambiguousChar, 1, wx.ALL|wx.EXPAND, 5 )

		self.noDuplicates = wx.CheckBox( self, noDuplicates, u"No Duplicate Characters", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.noDuplicates, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer8.Add( bSizer12, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer8, 1, wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		bSizer14.SetMinSize( wx.Size( 500,-1 ) )
		self.password = wx.richtext.RichTextCtrl( self, passwordTxt, u" ", wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer14.Add( self.password, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer9.Add( bSizer14, 1, wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.Generate  = wx.Button( self, wx.ID_ANY, u"Generate password", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.Generate , 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.Copy = wx.Button( self, wx.ID_ANY, u"Copy", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.Copy, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


		bSizer9.Add( bSizer13, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer9, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Generate .Bind( wx.EVT_BUTTON, self.generatePass )
		self.Copy.Bind( wx.EVT_BUTTON, self.copyPass )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def generatePass( self, event ):
		event.Skip()

	def copyPass( self, event ):
		event.Skip()


wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False) 
frame = MyFrame1(None) 
frame.Show(True) 
app.MainLoop() 