import os 
import subprocess

def ExcuteSpoon(full,diff,tmpResult):
    outPutDir=tmpResult    #結果を保存するフォルダ
    SpoonRootDir=os.path.join(os.path.dirname(os.getcwd()),"spoon")

    spoonCMD=["java","-jar","target/demo-1.0-snapshot.jar",full,diff,outPutDir]
    subprocess.run(spoonCMD,cwd=SpoonRootDir)
    
