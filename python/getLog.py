import subprocess
import os
import shutil


def getLog(rootProject,LogDir):
    gitProject = rootProject
    saveLogDir = LogDir

    if os.path.isdir(saveLogDir):
        shutil.rmtree(saveLogDir)
    os.makedirs(saveLogDir)

    beLatestVersion = "git checkout master"
    subprocess.run(beLatestVersion.split(), cwd=gitProject, check=True)

    getLog = "git log --pretty=format:%H --name-only --diff-filter=ACMR -- *.java"
    hash = subprocess.run(
        getLog.split(), cwd=gitProject, capture_output=True, check=True, text=True
    )
    blocks = hash.stdout.split("\n\n")
    k = 0
    count=0
    for commit in blocks:
        commitLines = commit.split("\n")
        filterList = [i for i in commitLines if "test" not in i and "info" not in i and "example" not in i and "exception" in i and "Test" not in i and "Example" not in i and "Exception" not in i]
        if len(filterList) >= 2:
            count=count+len(filterList)-1
            k = k + 1
            for i in range(1, len(filterList)):
                filterList[i] = os.path.join(gitProject , filterList[i])
            fileWrite = "\n".join(filterList)
            with open(os.path.join(saveLogDir,"logHash.txt"),"a",encoding="utf-8") as f:
                f.write(str(k)+","+filterList[0]+"\n")
            with open(os.path.join(saveLogDir , str(k) + ".txt"), "w", encoding="utf-8") as f:
                f.write(fileWrite)
                
# gitプロジェクトのパスから、test info を除いた Javaファイル を変更したlog( commitID と　変更Javaファイル )をlogDataに保存する　※１つのコミットに対して１つのファイル
#git show