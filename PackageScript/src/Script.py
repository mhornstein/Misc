import urllib2
import os
import zipfile
import shutil

'''
This script:
(1) Loads jar files downlod adress.
(2) Downloads the jar
(3) Generates the package prefix in java imports
(4) write result to file
'''

jarDownloadLoc = "tmp"
doneJarsLoc = "done"
jarListFileName = "Jars2.csv"

def main():
    jarsLoc = loadJarsUrl()
    os.chdir(jarDownloadLoc)
    packagesNames = {}
    for jar in jarsLoc:
        jarName = jar
        jarUrl = jarsLoc[jarName]
        
        downloadFile(jarName, jarUrl)
        unzipFile(jarName)
        packagesNames[jarName]= getPackagesNames()
        clean(jarName)
    writeRes(packagesNames) 
        
def loadJarsUrl():
    jarsUrl = {}
    lines = [line.strip() for line in open(jarListFileName)]
    for line in lines:
        jarInfo=line.split(",")
        jarsUrl[jarInfo[0]] = jarInfo[-1]
    return jarsUrl

def downloadFile(fileName, url):
    with open(fileName,'wb') as f:
        f.write(urllib2.urlopen(url).read())
        f.close()

def unzipFile(jarName):
    with zipfile.ZipFile(jarName, "r") as z:
        z.extractall(".")
        z.close()
        
def getPackagesNames():
    def getPackgeName(name):
        name = name.replace(".\\", "") #removes the initial .\\
        name = name.replace(".", "") #in case this is the root
        name = name.replace ("\\", ".") #translate into package structure
        return name
        
    def isValidPackagenName(name):
        if "META-INF" in name:
            return False
        name = getPackgeName(name)
        if name != None and len(name.split(".")) == 3:
            return True
        else:
            return False
        
    d='.'
    dirs = [getPackgeName(x[0]) for x in os.walk(d) if isValidPackagenName(x[0])]
    return dirs
    

def clean(jarName):
    for x in next(os.walk('.'))[1]:
        shutil.rmtree(x)
    shutil.move(jarName, "..\\" +doneJarsLoc + "\\" + jarName)
    
def writeRes(packagesNames):
    with open('res.csv', 'a') as f:
        for jarName in packagesNames:
            for packageName in packagesNames[jarName]:
                f.write(jarName + "," + packageName)
    f.close()

if __name__ == '__main__':
    main()