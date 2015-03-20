import os
'''
Loads a list of packages to search recursively in a given root
Prints the files in which packege name appears
'''
packagesNamesFile = "res.csv"
rootFolfer = "."

def main():
    packagesNames = loadPackesNames()
    reportPackagesOccurances(packagesNames)

def loadPackesNames():
    res = []
    lines = [line.strip() for line in open(packagesNamesFile)]
    for line in lines:
        jarInfo=line.split(",")
        res+= [jarInfo[-1]]
    return res

def reportPackagesOccurances(packagesNames):
    def logRes(res):
        with open('occuranceRes.csv', 'a') as f:
            for r in res:
                f.write(r + "\n")
        f.close()
        
    res = []
    for dname, dirs, files in os.walk(rootFolfer):
        for fname in files:
            fpath = os.path.join(dname, fname)
            with open(fpath) as f:
                s = f.read()
            for pName in packagesNames:
                if pName in s:
                    res += [dname + "\\" +fname + " : " + pName]
    logRes(res)

if __name__ == '__main__':
    main()
