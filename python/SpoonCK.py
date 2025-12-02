import shutil
import subprocess
import os
import pandas as pd
import sys

import ExcuteCK, ExcuteSpoon, getAllFile, getLog

ClassFlag=True
MethodFlag=True
def editClass(Spoonfile, CKfile, outPutFolder, fileName):   #fileName=何個目のlogか
    global ClassFlag
    df = pd.read_csv(CKfile)
    CK = df[["file", "class","type", "wmc", "tcc", "loc","totalMethodsQty"]]
    CK["class"] = CK["class"].str.replace("$Anonymous", "$")
    spoon = pd.read_csv(Spoonfile)
    join = spoon.merge(CK, how="inner", on=["file", "class"])
    join["num"]=fileName

    join.to_csv(
        os.path.join(outPutFolder ,  str(fileName) + "class.csv")
    ) 
    
    if ClassFlag:
        join.to_csv(
            os.path.join(outPutFolder,"allClass.csv"),mode="w",index=False
        )
        ClassFlag=False
    else:
        join.to_csv(
            os.path.join(outPutFolder,"allClass.csv"),mode="a",header=False,index=False
        )


def editMethod(SpoonFile, CKFile, outPutFolder, fileName):
    global MethodFlag
    df = pd.read_csv(CKFile)
    CK = df[["file", "class", "method", "wmc", "loc"]]
    spoon = pd.read_csv(SpoonFile)
    join = spoon.merge(CK, how="inner", on=["file", "class", "method"])
    join["num"]=fileName
    join.to_csv(
        os.path.join(outPutFolder , str(fileName) + "method.csv")
    ) 
    
    if MethodFlag:
        join.to_csv(
            os.path.join(outPutFolder,"allMethod.csv"),mode="w",index=False
        )
        MethodFlag=False
    else:
        join.to_csv(
            os.path.join(outPutFolder,"allMethod.csv"),mode="a",header=False,index=False
        )
        
def makeNewDir(file):
    if os.path.isdir(file):
        shutil.rmtree(file)
    os.makedirs(file)
    
#projectFolder=sys.argv[1]
#outPutFolder=sys.argv[2]
Folders=[["C:\\Users\\syuuj\\gitProject\\redisson","C:\\Users\\syuuj\\gitProjectResult\\redisson"],["C:\\Users\\syuuj\\gitProject\\guava","C:\\Users\\syuuj\\gitProjectResult\\guava"]]

for AnalyzeSet in Folders:
    ClassFlag=True
    MethodFlag=True
    projectFolder=AnalyzeSet[0]
    outPutFolder=AnalyzeSet[1]
    if not os.path.isdir(outPutFolder):
        os.makedirs(outPutFolder)

    absolutePath = os.getcwd()
    tmpResult=os.path.join(absolutePath,"tmpResult")
    tmpCKClassResult=os.path.join(tmpResult,"class.csv")
    tmpCKMethodResult=os.path.join(tmpResult,"method.csv")
    tmpSpoonClassResult=os.path.join(tmpResult,"spoonClass.csv")
    tmpSpoonMethodResult=os.path.join(tmpResult,"spoonMethod.csv")       #各ツールの結果を一時保存する場所，結合する必要あり
    os.makedirs(tmpResult,exist_ok=True)            #一時保存するフォルダを作成

    LogDir=os.path.join(outPutFolder,"logData")                  #ログのjava差分ファイル
    makeNewDir(LogDir)
    
    LogFullDir=os.path.join(outPutFolder,"logFull")              #あるコミット時点の全てのjavaファイル
    makeNewDir(LogFullDir)

    getLog.getLog(projectFolder,LogDir)
    with open(os.path.join(LogDir,"logHash.txt"),"r",encoding="utf-8") as f:
        hashList=[s.rstrip() for s in f.readlines()]
    i=0
    for hashSet in hashList:
        hashSplit=hashSet.split(",")
        DiffText=os.path.join(LogDir,hashSplit[0]+".txt")
        FullText=os.path.join(LogFullDir,hashSplit[0]+".txt")
        gitCheckout=["git","checkout",hashSplit[1]]
        subprocess.run(gitCheckout,cwd=projectFolder,check=True)
        getAllFile.searchFile(projectFolder,FullText)
        ExcuteCK.ExcuteCK(DiffText,tmpResult+"/")
        ExcuteSpoon.ExcuteSpoon(FullText,DiffText,tmpResult+"/")
        editClass(tmpSpoonClassResult,tmpCKClassResult,outPutFolder,i)
        editMethod(tmpSpoonMethodResult,tmpCKMethodResult,outPutFolder,i)
        i=i+1

        #プロジェクトのissuueとlogがしっかり書かれているかしっかりと見る