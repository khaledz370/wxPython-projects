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
true = True
defaultfileTypesList = [".mkv" ,".ts" ,".mp4" ,".avi" ,".webm" ,".flv" ,".ogg" ,".mov" ,".mpeg-2"]
mkvMerge = "C:\Program Files\MKVToolNix\mkvmerge.exe"
mkvpropedit = "C:\Program Files\MKVToolNix\mkvpropedit.exe"

        # Connect Events
        self.m_button3.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToMkv") )
        self.m_button11.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToMkv") )
        self.m_button15.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToMkv") )
        self.m_button111.Bind( wx.EVT_BUTTON, lambda event: self.deleteToMkv("ToMkv") )
        self.m_button7.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("ToMkv") )
        self.m_button9.Bind( wx.EVT_BUTTON, self.convertToMkv )
        self.m_button31.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToAudio") )
        self.m_button112.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToAudio") )
        self.m_button151.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToAudio") )
        self.m_button1111.Bind( wx.EVT_BUTTON, lambda event: self.deleteToMkv("ToAudio") )
        self.m_button71.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("ToAudio") )
        self.m_button91.Bind( wx.EVT_BUTTON, self.convertToAudio )

    def deleteToMkv( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        allFilesInCheckBoxList = checkBoxListWindow.GetItems()
        selectedFilesFromList = checkBoxListWindow.GetCheckedStrings()
        newList = list(filter(lambda file:str(file) not in selectedFilesFromList,allFilesInCheckBoxList))
        checkBoxListWindow.SetItems(newList)

    def openFilesSelector( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        openFileDialog = wx.FileDialog(self, "Select files", "", "", "All files (*.*)|*.*",
           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST|wx.FD_MULTIPLE)
        openFileDialog.ShowModal()
        checkBoxListWindow.Set(openFileDialog.GetFilenames())
        openFileDialog.Destroy()

    def selectFolder( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        fileTypes = eval(f"fileTypes{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        fileTypesList = wx.FindWindowById(fileTypes)
        openDirDialog = wx.DirDialog(self, "Choose folder",style=wx.DD_DIR_MUST_EXIST)
        openDirDialog.ShowModal()
        selectedDir = openDirDialog.GetPath()
        filesInDir = os.listdir(selectedDir)
        absFilesInDir = [f"{selectedDir}\\" + x for x in filesInDir]
        selectedFileTypes = fileTypesList.GetCheckedStrings()
        # print(selectedFileTypes)
        if not len(selectedFileTypes):
            selectedFileTypes = tuple(defaultfileTypesList)
        filterFilesInDir = list(filter(lambda file: str(file).endswith(selectedFileTypes),absFilesInDir))
        checkBoxListWindow.Set(filterFilesInDir)
        # print(filterFilesInDir)

        # self.m_checkList1.Set(openFileDialog.GetFilenames())
        openDirDialog.Destroy()


    def selectAll( self, event ):
        selectAll = eval(f"selectAll{event}")
        selectedFiles = eval(f"selectedFiles{event}")
        thisButton = wx.FindWindowById(selectAll)
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        indexes = checkBoxListWindow.GetCount()
        selectedItems = checkBoxListWindow.GetCheckedItems()
        if indexes and indexes != len(selectedItems):
            checkBoxListWindow.SetCheckedItems(range(indexes))
            thisButton.SetLabel("Select none")
        else:
            checkBoxListWindow.SetCheckedItems([])
            thisButton.SetLabel("Select all")

    def checkAllTypes( self, event ):
        fileTypes = eval(f"fileTypes{event}")
        all = eval(f"all{event}")
        thisButton = wx.FindWindowById(all)
        checkBoxListFileTypes = wx.FindWindowById(fileTypes)
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
                print(presentage)
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