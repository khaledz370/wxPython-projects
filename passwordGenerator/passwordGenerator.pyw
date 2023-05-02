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
import random
import string
import pyperclip
import threading

passLength = 1000
symbols = 1001
numbers = 1002
lowerCase = 1003
upperCase = 1004
ambiguousChar = 1005
noDuplicates = 1006
passwordTxt = 1007

start_val = 8
end_val = 128
passLenthList = list(range(start_val, end_val + 1))

passLenthListStr = [str(num) for num in passLenthList]

ambiguousCharachers = "({\}\[]()/\\\'\"`~,;:.<>)"

ambiguousCharachersLst = list(ambiguousCharachers)



###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 650,340 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 650,340 ), wx.Size( 650,340 ) )
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)

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

        Password_lengthChoices = passLenthListStr
        self.Password_length = wx.ComboBox( self, passLength, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, Password_lengthChoices, style=wx.CB_READONLY)
        self.Password_length.SetSelection( 0 )
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

        bSizer12.Add( bSizer17, 1, wx.EXPAND, 5 )

        self.upperCase = wx.CheckBox( self, upperCase, u"Include Uppercase Characters:  ( e.g. ABCDEFGH )", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer12.Add( self.upperCase, 1, wx.ALL|wx.EXPAND, 5 )

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
        self.Generate .Bind( wx.EVT_BUTTON, lambda event: self.processThread("self.generatePass") )
        self.Copy.Bind( wx.EVT_BUTTON, self.copyPass )

    def __del__( self ):
        pass



    def processThread( self, event):
        process= eval(event)
        t = threading.Thread(target=process)
        t.daemon = True # set thread as daemon to terminate when main thread ends
        t.start()
    
    # Virtual event handlers, override them in your derived class
    def generatePass( self):
        passwordWindow = wx.FindWindowById(passwordTxt)
        
        rangeWindow = wx.FindWindowById(passLength)
        passRange = int(rangeWindow.GetStringSelection())
        
        lowerCaseWindow = wx.FindWindowById(lowerCase)
        lowerCaseVal = lowerCaseWindow.IsChecked()
        
        upperCaseWindow = wx.FindWindowById(upperCase)
        upperCaseVal = upperCaseWindow.IsChecked()
        
        numbersWindow = wx.FindWindowById(numbers)
        numbersVal = numbersWindow.IsChecked()
        
        symbolsWindow = wx.FindWindowById(symbols)
        symbolsVal = symbolsWindow.IsChecked()
        
        noDuplicatesWindow = wx.FindWindowById(symbols)
        noDuplicatesVal = noDuplicatesWindow.IsChecked()
        
        ambiguousCharWindow = wx.FindWindowById(symbols)
        ambiguousCharVal = ambiguousCharWindow.IsChecked()
        
        password = ""
        passwordList = []
        password_chars = ""
        if lowerCaseVal:
            password_chars += string.ascii_lowercase
        # select 1 uppercase
        if upperCaseVal:
            password_chars += string.ascii_uppercase
        # select 1 digit
        if numbersVal:
            password_chars += string.digits
        # select 1 special symbol
        if symbolsVal:
            password_chars += string.punctuation
            
        while len(password) < passRange:
            if password_chars != "":
                password += ''.join(random.choice(password_chars) for i in range(passRange)).replace("\n", "")
                if noDuplicatesVal:
                    password = ''.join(set(password))
                if ambiguousCharVal:
                    password = replaceStringInList(password,ambiguousCharachersLst)
            else:
                password_chars = string.digits + string.ascii_letters + string.punctuation + string.whitespace
                password += ''.join(random.choice(password_chars) for i in range(passRange)).replace("\n", "")
                
        passwordList.append(str(password))
        print(password)
        passwordListStrs = '\n'.join(passwordList)
        passwordWindow.SetValue(passwordListStrs)
        return password

    def copyPass( self, event ):
        passwordWindow = wx.FindWindowById(passwordTxt)
        myPassword = passwordWindow.GetValue()
        pyperclip.copy(myPassword)

def remove_duplicates(s):
    return ''.join(set(s))

def replaceStringInList(s,myList):
    for char in myList:
        s = s.replace(char, '')
    return s



wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False) 
frame = MyFrame1(None) 
frame.Show(True) 
app.MainLoop() 