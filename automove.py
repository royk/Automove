# Moves files according to rules embedded in their file name
# The rules are:
# 1) Target directory and target file name are separated with a __
#    So to copy the file to c:\ and call it foo.txt, the original file's name must be:
#    c__foo.txt
#
# 2) Sub directories are separated with _
#     So to copy the file to c:\temp and call it lala.foo, the original file's name must be:
#     c_temp__lala.foo
#
# Source directory is determined according to the following rules:
# 1) If the first argument exists, use it as a path
# 2) Otherwise, try to fetch the environment variable DESKTOP. if it exist, use it as a path
# 3) Otherwise, use current path.
#
# The copy operation is not recursive. Will only test files in the first level of the given directory

import os
import shutil
from sys import argv

def extractPath():
    if len(argv)>1 and os.access(argv[1], os.R_OK):
        returnPath = argv[1]
    else:
        returnPath = os.getenv("DESKTOP")
        if returnPath is None or not os.access(myPath, os.R_OK):
            returnPath = "."
    return returnPath

def readConfiguration():
    configFile = open("automove.cfg", "r")
    config = {}
    for line in configFile:
        line = line.strip()
        parts = line.split("=")
        if len(parts)!=2:
            continue
        if str.find(parts[0], "#")==0:
            continue
        config[parts[0]] = parts[1]
    return config

def getPathAndFile(file):
    # Directory and file name are split by double underline __
    parts       = file.split("__")
    returnDir   = None
    returnFile  = None
    if len(parts)==2:
        returnFile  = parts[1]
        # Sub directories are split by one underline _
        if parts[0] in pathShortcuts:
            returnDir = pathShortcuts[parts[0]]
        else:
            dirParts    = parts[0].split("_")
            # The first part is the drive letter. Give it : (like c:)
            dirParts[0] = dirParts[0]+":"
            returnDir   = "_".join(dirParts).replace("_","\\")
    return returnDir, returnFile

def nameContainsPath(file):
    result                  = False
    targetPath = getPathAndFile(file)[0]
    if not targetPath is None and os.access(targetPath, os.W_OK): 
        result = True;
    return result

def moveAndRename(file, targetPath, targetName):
    shutil.move(file, targetPath+"\\"+targetName)
    
# Main logic    

myPath          = extractPath()
files           = os.listdir(myPath)
pathShortcuts   = readConfiguration() 

print "Copying from %s:" % myPath

for file in files:
    if nameContainsPath(file):
        sourceFile              = myPath+"\\"+file
        targetPath, targetName  = getPathAndFile(file)
        print "\t%s\\%s" % (targetPath, targetName)
        moveAndRename(sourceFile, targetPath, targetName)
        
print "Done."