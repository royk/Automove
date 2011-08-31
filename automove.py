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
        myPath = argv[1]
    else:
        myPath = os.getenv("DESKTOP")
        if myPath is None or not os.access(myPath, os.R_OK):
            myPath = "."
    return myPath

def getPathAndFile(file):
    # Directory and file name are split by double underline __
    parts       = file.split("__")
    returnDir   = None
    returnFile  = None
    if len(parts)==2:
        # Sub directories are split by one underline _
        dirParts    = parts[0].split("_")
        # The first part is the drive letter. Give it : (like c:)
        dirParts[0] = dirParts[0]+":"
        returnDir   = "_".join(dirParts).replace("_","\\")
        returnFile  = parts[1]
    return returnDir, returnFile

def nameContainsPath(file):
    result                  = False
    targetPath, targetFile  = getPathAndFile(file)
    if not targetPath is None and os.access(targetPath, os.W_OK): 
        result = True;
    return result

def moveAndRename(file, targetPath, targetName):
    shutil.move(file, targetPath+"\\"+targetName)
    
# Main logic    

myPath  = extractPath()
files   = os.listdir(myPath)

print "Copying from %s:" % myPath

for file in files:
    if nameContainsPath(file):
        sourceFile              = myPath+"\\"+file
        targetPath, targetName  = getPathAndFile(file)
        print "\t%s\\%s" % (targetPath, targetName)
        moveAndRename(sourceFile, targetPath, targetName)
        
print "Done."