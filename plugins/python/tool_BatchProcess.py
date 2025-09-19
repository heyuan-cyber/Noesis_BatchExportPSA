import os
from inc_noesis import *
import noesis

import noesis
import rapi
import os


def exportAsPSA(inFile, outFile):

    try:
        mod = noesis.instantiateModule()
        noesis.setModuleRAPI(mod)
        if not rapi.toolLoadGData(inFile):
            noesis.messagePrompt("Load failed: " + inFile)
            return

        if rapi.toolGetLoadedModelCount() > 0:
            rapi.toolExportGData(outFile, "-fmtoutidx 0 -animoutidx 314  -rotate -90 0 0")
            #noesis.messagePrompt("Export Success: " + outFile)
        else:
            noesis.messagePrompt("No anim/model loaded: " + inFile)

        rapi.toolFreeGData()
    except Exception as e:  # Python 2.7 语法
        noesis.messagePrompt("Export failed Exception: " + str(e))
    noesis.freeModule(mod)
# Register menu entries
def registerNoesisTypes():
    noesis.registerTool("Batch Export PSA (All)", batchExportPSAAll, "Export PSA files for all characters")
    noesis.registerTool("Batch Export PSA (Single)", batchExportPSASingleCharacter, "Export PSA files for a single character")
    noesis.registerTool("Batch Export PSA (Folder)", batchExportPSAFolder, "Export PSA files for a Forlder")
    return 1


# Shared export logic
def exportMotionFolders(rolePath):
    v00Path = os.path.join(rolePath, "v00", "motionlist")
    if not os.path.exists(v00Path):
        return

    # Expected motion subfolders
    for motionType in ["attack", "basic", "etc", "specialskill", "superarts"]:
        motionDir = os.path.join(v00Path, motionType)
        if not os.path.exists(motionDir):
            continue

        # Create output directory
        outDir = os.path.join(rolePath, "psa", motionType)
        os.makedirs(outDir, exist_ok=True)

        # Process motion files
        for fileName in os.listdir(motionDir):
            if not fileName.lower().endswith(".653"):
                continue

            inFile = os.path.join(motionDir, fileName)
            outFile = os.path.join(outDir, os.path.splitext(fileName)[0] + ".psa")

            try:
                exportAsPSA(inFile, outFile)
            except Exception as e:
                print("[ERROR] Exception during export:", inFile, e)

# Export all characters
def batchExportPSAAll(toolIndex):
    rootFolder = noesis.userPrompt(
        noesis.NOEUSERVAL_FOLDERPATH,
        "Select ESF root folder",
        "Pick the folder that contains esf000-esf021",
        "D:\\Game\\esf",
        None
    )

    if not rootFolder:
        noesis.messagePrompt("No folder selected. Operation cancelled.")
        return 0

    for roleDir in os.listdir(rootFolder):
        rolePath = os.path.join(rootFolder, roleDir)
        if not os.path.isdir(rolePath):
            continue

        print("[INFO] Processing character:", roleDir)
        exportMotionFolders(rolePath)

    noesis.messagePrompt("All characters exported successfully.")
    return 0

# Export one character only
def batchExportPSASingleCharacter(toolIndex):
    rolePath = noesis.userPrompt(
        noesis.NOEUSERVAL_FOLDERPATH,
        "Select single ESF folder",
        "Pick one esfxxx folder",
        "D:\\softwares\\ExportToolForREEngine\\StreetFighter6Extract\\REtool\\re_chunk_000\\natives\\stm\\product\\animation\\esf\\esf013",
        None
    )

    if not rolePath:
        noesis.messagePrompt("No folder selected. Operation cancelled.")
        return 0

    print("[INFO] Processing single character:", rolePath)
    exportMotionFolders(rolePath)

    noesis.messagePrompt("Single character exported successfully.")
    return 0

def batchExportPSAFolder(toolIndex):
    rolePath = noesis.userPrompt(
        noesis.NOEUSERVAL_FOLDERPATH,
        "Select single  folder",
        "Pick one esfxxx folder",
        "D:\\softwares\\ExportToolForREEngine\\StreetFighter6Extract\\REtool\\re_chunk_000_Aki\\natives\\stm\\product\\animation\\esf\\esf010\\v00\\motionlist\\specialskill",
        None
    )

    if not rolePath:
        noesis.messagePrompt("No folder selected. Operation cancelled.")
        return 0

    print("[INFO] Processing single character:", rolePath)
    exportSingleFolderPSA(rolePath)
    return 0
def exportSingleFolderPSA(folderPath):
    """
    Export all .653 files in the selected folder using toolExportGData.
    Output: folderPath/psa/<animation.psa>
    """
    if not os.path.exists(folderPath):
        print("[WARN] folder not found:", folderPath)
        return

    outRoot = os.path.join(folderPath, "psa")
    os.makedirs(outRoot, exist_ok=True)

    for f in os.listdir(folderPath):
        if not f.lower().endswith(".653"):
            continue

        inFile = os.path.join(folderPath, f)
        outFile = os.path.join(outRoot, os.path.splitext(f)[0] + ".psa")
        exportAsPSA(inFile, outFile)