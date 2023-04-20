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
from tendo import singleton

selectedFilesToMkv = 1000
browseFilesToMkv = 1001
browseFolderToMkv = 1002
selectAllToMkv = 1003
fileTypesToMkv = 1004
allToMkv = 1005
convertToMkv = 1006
currentFileTomkv = 1007
pBarToMkv = 1008
dBtnToMkv = 1009
true = True
defaultfileTypesList = [".mkv" ,".ts" ,".mp4" ,".avi" ,".webm" ,".flv" ,".ogg" ,".mov" ,".mpeg-2"]
mkvMerge = "C:\Program Files\MKVToolNix\mkvmerge.exe"
mkvpropedit = "C:\Program Files\MKVToolNix\mkvpropedit.exe"

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
        self.m_checkList1.DragAcceptFiles( True )

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
        self.m_checkList11.DragAcceptFiles( True )

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
        self.m_button3.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToMkv") )
        self.m_button11.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToMkv") )
        self.m_button15.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToMkv") )
        self.m_button111.Bind( wx.EVT_BUTTON, lambda event: self.deleteToMkv("ToMkv") )
        self.m_button7.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("ToMkv") )
        self.m_button9.Bind( wx.EVT_BUTTON, self.convertToMkv )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def deleteToMkv( self, event ):
        checkBoxListWindow = wx.FindWindowById(selectedFilesToMkv)
        allFilesInCheckBoxList = checkBoxListWindow.GetItems()
        selectedFilesFromList = checkBoxListWindow.GetCheckedStrings()
        newList = list(filter(lambda file:str(file) not in selectedFilesFromList,allFilesInCheckBoxList))
        checkBoxListWindow.SetItems(newList)


    def openFilesSelector( self, event ):
        openFileDialog = wx.FileDialog(self, "Select files", "", "", "All files (*.*)|*.*",
           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE)
        openFileDialog.ShowModal()
        checkBoxListWindow = wx.FindWindowById(selectedFilesToMkv)
        checkBoxListWindow.Set(openFileDialog.GetFilenames())
        openFileDialog.Destroy()

    def selectFolder( self, event ):
        openDirDialog = wx.DirDialog(self, "Choose folder",style=wx.DD_DIR_MUST_EXIST)
        openDirDialog.ShowModal()
        selectedDir = openDirDialog.GetPath()
        filesInDir = os.listdir(selectedDir)
        absFilesInDir = [f"{selectedDir}\\" + x for x in filesInDir]
        fileTypesList = wx.FindWindowById(fileTypesToMkv)
        selectedFileTypes = fileTypesList.GetCheckedStrings()
        # print(selectedFileTypes)
        if not len(selectedFileTypes):
            selectedFileTypes = tuple(defaultfileTypesList)
        filterFilesInDir = list(filter(lambda file: str(file).endswith(selectedFileTypes),absFilesInDir))
        checkBoxListWindow = wx.FindWindowById(selectedFilesToMkv)
        checkBoxListWindow.Set(filterFilesInDir)
        # print(filterFilesInDir)

        # self.m_checkList1.Set(openFileDialog.GetFilenames())
        openDirDialog.Destroy()


    def selectAll( self, event ):
        thisButton = wx.FindWindowById(selectAllToMkv)
        checkBoxListWindow = wx.FindWindowById(selectedFilesToMkv)
        indexes = checkBoxListWindow.GetCount()
        selectedItems = checkBoxListWindow.GetCheckedItems()
        if indexes and indexes != len(selectedItems):
            checkBoxListWindow.SetCheckedItems(range(indexes))
            thisButton.SetLabel("Select none")
        else:
            checkBoxListWindow.SetCheckedItems([])
            thisButton.SetLabel("Select all")

    def checkAllTypes( self, event ):
        thisButton = wx.FindWindowById(allToMkv)
        checkBoxListFileTypes = wx.FindWindowById(fileTypesToMkv)
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
        currentFile = wx.FindWindowById(currentFileTomkv)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarToMkv)
        # print(indexes)
        if indexes:
            allFiles = checkBoxListWindow.GetItems()
            duplicateFiles = list(allFiles)
            for index, file in enumerate(allFiles):
                selectedDir = os.path.dirname(file)
                fName = os.path.basename(file)
                fNameNoExt = os.path.splitext(fName)[0]
                if not os.path.exists((f"{selectedDir}\\mkvmerge_old")):
                    os.makedirs((f"{selectedDir}\\mkvmerge_old"))
                mkvmerge_old = (f"{selectedDir}\mkvmerge_old\{fName}")
                shutil.move(file, mkvmerge_old)
                currentFile.SetLabel(str(file))
                mkvCommand = f"\"{mkvMerge}\" --output \"{selectedDir}\\{fNameNoExt}.mkv\" \"{selectedDir}\\mkvmerge_old\\{fName}\""
                presentage = int(100*(index+1)/indexes)
                pBar.SetValue((presentage))
                runCommand(mkvCommand)
                duplicateFiles.remove(duplicateFiles[0])
                checkBoxListWindow.Set(duplicateFiles)
        pBar.SetValue(0)
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