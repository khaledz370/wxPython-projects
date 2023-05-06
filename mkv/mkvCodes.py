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
import json

true = True
defaultfileTypesList = [".mkv" ,".ts" ,".mp4" ,".avi" ,".webm" ,".flv" ,".ogg" ,".mov" ,".mpeg-2"]
fileTypesFillter = "Video files (*.mkv)|*.mkv|(*.mp4)|*.mp4|(*.ts)|*.ts|(*.flv)|*.flv|(*.avo)|*.avo|(*.webm)|*.webm|(*.ogg)|*.ogg|(*.mov)|*.mov|(*.mpeg-2)|*.mpeg-2"
mkvMerge = "C:\Program Files\MKVToolNix\mkvmerge.exe"
mkvpropedit = "C:\Program Files\MKVToolNix\mkvpropedit.exe"
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
cropVideo = 1031
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
runOption = 1042
currentFileOptions = 1043
pBarOptions = 1044
tabContainer = 1045

###########################################################################
## Class MyFrame1
###########################################################################

        # Connect Events
        self.m_button3.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToMkv") )
        self.m_button11.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToMkv") )
        self.m_button15.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToMkv") )
        self.m_button111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("ToMkv") )
        self.m_button7.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("ToMkv") )
        self.m_button9.Bind( wx.EVT_BUTTON, self.convertToMkv )
        self.m_button31.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("ToAudio") )
        self.m_button112.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("ToAudio") )
        self.m_button151.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("ToAudio") )
        self.m_button1111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("ToAudio") )
        self.m_button71.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("ToAudio") )
        self.m_button91.Bind( wx.EVT_BUTTON, self.convertToAudio )
        self.m_button311.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("Crop") )
        self.m_button1121.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("Crop") )
        self.m_button1511.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("Crop") )
        self.m_button11111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("Crop") )
        self.m_button711.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("Crop") )
        self.m_button911.Bind( wx.EVT_BUTTON, self.cropVideo )
        self.m_button3111.Bind( wx.EVT_BUTTON, lambda event: self.openFilesSelector("Options") )
        self.m_button11211.Bind( wx.EVT_BUTTON, lambda event: self.selectFolder("Options") )
        self.m_button15111.Bind( wx.EVT_BUTTON, lambda event: self.selectAll("Options") )
        self.m_button111111.Bind( wx.EVT_BUTTON, lambda event: self.deleteFromList("Options") )
        self.m_button7111.Bind( wx.EVT_BUTTON, lambda event: self.checkAllTypes("Options") )
        self.m_button9111.Bind( wx.EVT_BUTTON, self.runWithJson )

    def __del__( self ):
        pass

    # Virtual event handlers, override them in your derived class
    def deleteFromList( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        allFilesInCheckBoxList = checkBoxListWindow.GetItems()
        selectedFilesFromList = checkBoxListWindow.GetCheckedStrings()
        newList = list(filter(lambda file:str(file) not in selectedFilesFromList,allFilesInCheckBoxList))
        checkBoxListWindow.SetItems(newList)

    def openFilesSelector( self, event ):
        selectedFiles = eval(f"selectedFiles{event}")
        checkBoxListWindow = wx.FindWindowById(selectedFiles)
        openFileDialog = wx.FileDialog(self, "Select files", "", "",fileTypesFillter,
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
        try:
            filesInDir = os.listdir(selectedDir)
            absFilesInDir = [f"{selectedDir}\\" + x for x in filesInDir]
            selectedFileTypes = fileTypesList.GetCheckedStrings()
            if not len(selectedFileTypes):
                selectedFileTypes = tuple(defaultfileTypesList)
            filterFilesInDir = list(filter(lambda file: str(file).endswith(selectedFileTypes),absFilesInDir))
            checkBoxListWindow.Set(filterFilesInDir)
            openDirDialog.Destroy()
        except:
            pass # no folder was selected


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
        currentFile = wx.FindWindowById(currentFileToMkv)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarToMkv)
        # print(indexes)
        if indexes:
            allFiles = checkBoxListWindow.GetItems()
            duplicateFiles = list(allFiles)
            for index, file in enumerate(allFiles):
                currentFile.SetLabel(str(file))
                selectedDir = os.path.dirname(file)
                fName = os.path.basename(file)
                fNameNoExt = os.path.splitext(fName)[0]
                if not os.path.exists((f"{selectedDir}\\mkvmerge_old")):
                    os.makedirs((f"{selectedDir}\\mkvmerge_old"))
                mkvmerge_old = (f"{selectedDir}\mkvmerge_old\{fName}")
                shutil.move(file, mkvmerge_old)
                mkvCommand = f"\"{mkvMerge}\" --output \"{selectedDir}\\{fNameNoExt}.mkv\" \"{selectedDir}\\mkvmerge_old\\{fName}\""
                presentage = int(100*(index+1)/indexes)
                print(presentage)
                pBar.SetValue((presentage))
                runCommand(mkvCommand)
                duplicateFiles.remove(duplicateFiles[0])
                checkBoxListWindow.Set(duplicateFiles)
        currentFile.SetLabel("")
        
    def convertToAudio( self, event ):
        checkBoxListWindow = wx.FindWindowById(selectedFilesToAudio)
        currentFile = wx.FindWindowById(currentFileToAudio)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarToAudio)
        # print(indexes)
        if indexes:
            allFiles = checkBoxListWindow.GetItems()
            duplicateFiles = list(allFiles)
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
                duplicateFiles.remove(duplicateFiles[0])
                checkBoxListWindow.Set(duplicateFiles)
        currentFile.SetLabel("")

    def cropVideo( self, event ):
        checkBoxListWindow = wx.FindWindowById(selectedFilesCrop)
        currentFile = wx.FindWindowById(currentFileCrop)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarCrop)
        cTopWindow = wx.FindWindowById(cTop)
        cLeftWindow = wx.FindWindowById(cLeft)
        cRightWindow = wx.FindWindowById(cRight)
        cBottomWindow = wx.FindWindowById(cBottom)
        cTopValue = int(cTopWindow.GetLineText(0))
        cLeftValue = int(cLeftWindow.GetLineText(0))
        cRightValue = int(cRightWindow.GetLineText(0))
        cBottomValue = int(cBottomWindow.GetLineText(0))
        # print(indexes)
        if indexes:
            allFiles = checkBoxListWindow.GetItems()
            duplicateFiles = list(allFiles)
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
                
                if cTopValue + cBottomValue + cLeftValue + cRightValue:
                    mkvCropCommand = f"\"{mkvpropedit}\" \"{selectedDir}\\{fNameNoExt}.mkv\" --edit track:v1 --set pixel-crop-top={int(cTopValue)} --set pixel-crop-left={int(cLeftValue)}  --set pixel-crop-right={int(cRightValue)} --set pixel-crop-bottom={int(cBottomValue)}"
                else:
                    mkvCropCommand = f"\"{mkvpropedit}\" \"{selectedDir}\\{fNameNoExt}.mkv\" --edit track:v1 --delete pixel-crop-top --delete pixel-crop-left  --delete pixel-crop-right --delete pixel-crop-bottom"
                
                presentage = int(100*(index+1)/indexes)
                pBar.SetValue((presentage))
                runCommand(mkvCropCommand)
                duplicateFiles.remove(duplicateFiles[0])
                checkBoxListWindow.Set(duplicateFiles)
        currentFile.SetLabel("")
        
    def runWithJson( self, event ):
        optionJson = wx.FindWindowById(optionsFile)
        checkBoxListWindow = wx.FindWindowById(selectedFilesOptions)
        currentFile = wx.FindWindowById(currentFileOptions)
        indexes = checkBoxListWindow.GetCount()
        pBar = wx.FindWindowById(pBarOptions)
        jsonFile = optionJson.GetPath()
        if os.path.exists(jsonFile):
            jsonVar = open(jsonFile)
            fileOptions = list(json.load(jsonVar))
            try:
                removeIndex = fileOptions.index('--output')
                del fileOptions[removeIndex] # remove --output line
                del fileOptions[removeIndex] # remove file line
            except ValueError:
                pass  # item not in list
            try:
                removeIndex = fileOptions.index('(')
                del fileOptions[removeIndex] # remove ( line
                del fileOptions[removeIndex] # remove what's between () line
                del fileOptions[removeIndex] # remove ) line
            except:
                pass # item not in list
            if fileOptions[0] != "--ui-language":
                currentFile.SetLabel("wrong json file")
                return
            selectedJsonDir = os.path.dirname(jsonFile)
            with open(f'{selectedJsonDir}\\options.json', 'w') as f:
                json.dump(fileOptions, f)
            jsonFile = f'{selectedJsonDir}\\options.json'
            if indexes:
                allFiles = checkBoxListWindow.GetItems()
                duplicateFiles = list(allFiles)
                for index, file in enumerate(allFiles):
                    currentFile.SetLabel(str(file))
                    selectedDir = os.path.dirname(file)
                    fName = os.path.basename(file)
                    fNameNoExt = os.path.splitext(fName)[0]
                    if not os.path.exists((f"{selectedDir}\\mkvmerge_old")):
                        os.makedirs((f"{selectedDir}\\mkvmerge_old"))
                    mkvmerge_old = (f"{selectedDir}\mkvmerge_old\{fName}")
                    shutil.move(file, mkvmerge_old)
                    mkvCommand = f"\"{mkvMerge}\" @{jsonFile} -o \"{selectedDir}\\{fNameNoExt}.mkv\" \"{selectedDir}\\mkvmerge_old\\{fName}\""
                    presentage = int(100*(index+1)/indexes)
                    print(presentage)
                    pBar.SetValue((presentage))
                    runCommand(mkvCommand)
                    duplicateFiles.remove(duplicateFiles[0])
                    checkBoxListWindow.Set(duplicateFiles)
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

def fileTypeFormat(listOfTypes):
    finalString = ""
    if len(listOfTypes):
        for type in listOfTypes:
            # newStr = f"(*{type})|*{type}"
            # finalString = f"{finalString}|{newStr}" 
            newStr = f"*.{type}"
            finalString = f"{finalString} {newStr}" 
    # print(finalString[1:])
    return finalString

wx.SizerFlags.DisableConsistencyChecks()
app = wx.App(False)
frame = MyFrame1(None)

frame.Show(True)
app.MainLoop()



class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
     def OnInit(self):
         self.Init()
         frame = MyDialog1(None)
         MyTaskBarIcon(frame,self)
         frame.Show()
         self.SetTopWindow(frame)
         return True
 
def main():
    wx.SizerFlags.DisableConsistencyChecks()
    app = MyApp(redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    main()
