import re
import os

def searchFile(ROOT_PATH,saveFile):
    if not os.path.isdir(os.path.dirname(saveFile)):
        os.makedirs(os.path.dirname(saveFile))
    allFile={}
    for pathname,dirnames,filenames in os.walk(ROOT_PATH):
        for filename in filenames:
            if filename.endswith(".java"):
                fullPath=os.path.join(pathname,filename)
                if "test" not in fullPath and "info" not in fullPath and "example" not in fullPath and "exception" in fullPath and "Test" not in fullPath and "Example" not in fullPath and "Exception" not in fullPath:
                    parentFolder=re.sub(r"\\src\\.*","",fullPath)
                    if parentFolder in allFile:
                        allFile[parentFolder].append(fullPath)
                    else:
                        allFile.setdefault(parentFolder,[fullPath])
                        
    with open(saveFile,"w",encoding="utf-8") as f:              
        for key,item in allFile.items():
            for pathfile in item:
                print(pathfile,file=f)
            print(file=f)
                     

#gitProject="C:\\Users\\sugii syuji\\jsoup"
#searchFile(gitProject)

#gitプロジェクトのパスを渡して、gitプロジェクト内に含まれる test info を除いたjavaファイルの一覧を取得する