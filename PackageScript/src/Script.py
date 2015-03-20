import urllib2
import os
import zipfile
import os.path

jarListLoc = "C:\\Users\\mhornstein\\workspace\\Script\\src"
jarDownloadLoc = "tmp"
jarListFileName = "Jars2.csv"

def main():
    generatePackagesName()

def generatePackagesName():
    jarsLoc = loadJarsUrl()
    os.chdir(jarDownloadLoc)
    for jar in jarsLoc:
        jarName = jar
        jarUrl = jarsLoc[jarName]
        
        downloadFile(jarName, jarUrl)
        unzipFile(jarName)
        packagesNames = getPackagesNames()
        clean()
        
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
        
def getPackagesNames():
    d='.'
    dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    print dirs

def clean():
    return None

if __name__ == '__main__':
    main()