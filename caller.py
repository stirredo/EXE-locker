import psutil, os
import subprocess
from EXELockerFile.Encryptor import EncryptedFile
import sys

def checkScriptNameInFolder():
    parentProcessName = psutil.Process(os.getpid()).parent().name()
    if parentProcessName != "python.exe":
        scriptName = parentProcessName
    else:
        scriptName = os.path.basename(__file__)
    # get script name without extension
    scriptName = os.path.splitext(scriptName)[0]
    # change extension of script name to lock to .exelocker
    scriptName = scriptName + ".exelocker"
    fileList = getRelevantFilesInFolder()
    try:
        index = fileList.index(scriptName)
    except ValueError:
        index = None
    if index != None:
        return True
    else:
        return False


def getRelevantFilesInFolder():
    files = os.listdir('.')
    filteredList = []
    for f in files:
        if os.path.isfile(f):
            extension = os.path.splitext(f)[1]
            if extension == ".exelocker":
                filteredList.append(f)
    return filteredList

if __name__ == "__main__":
    if checkScriptNameInFolder():
        parentProcessName = psutil.Process(os.getpid()).parent().exe()
        if parentProcessName != "python.exe":
            scriptName = os.path.basename(parentProcessName)
        else:
            scriptName = os.path.basename(__file__)
        # get the script name without file extension
        scriptName = os.path.splitext(scriptName)[0] + ".exelocker"
        baseLocation = EncryptedFile.UNLOCK_DIALOG_LOCATION
        subprocess.Popen([baseLocation, scriptName])
    else:
        # baseLocation = EncryptedFile.BASE_FILE_LOCATION
        baseLocation = EncryptedFile.UNLOCK_DIALOG_LOCATION
        subprocess.Popen([baseLocation, os.getcwd()])
    sys.exit(0)



