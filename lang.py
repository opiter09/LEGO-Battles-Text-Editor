import FreeSimpleGUI as psg
import os
import subprocess
import sys

def splitFile(folder, path):
    binn2 = open(path, "rb")
    bytE = binn2.read()
    binn2.close()

    try:
        os.mkdir("_" + path.split("\\")[-1].split(".")[0] + "_" + "langFiles")
    except OSError as error:
        pass

    count = 0
    holding = 0
    currentMax = int.from_bytes(bytE[16:20], "little")
    for i in range(12, currentMax - 3, 4):
        count = count + 1

        oldOffset = int.from_bytes(bytE[i:(i + 4)], "little")
        newOffset = int.from_bytes(bytE[(i + 4):(i + 8)], "little")
        if (i == (currentMax - 4)):
            newOffset = os.stat(path).st_size
        
        fileName = "_" + path.split("\\")[-1].split(".")[0] + "_" + "langFiles/" + str(count).zfill(4) + ".txt"

        if (newOffset > currentMax):
            newFile = open(fileName, "wb")
            if (holding == 0):
                nullCount = bytE[oldOffset:newOffset].decode("UTF-8", errors = "ignore").count("\0")
                if (oldOffset < (newOffset - nullCount)):
                    newFile.write(bytE[oldOffset:(newOffset - nullCount)])
                else:
                    newFile.write(bytE[oldOffset:newOffset])
                newFile.close()
                currentMax = newOffset
            else:
                nullCount = bytE[holding:newOffset].decode("UTF-8", errors = "ignore").count("\0")
                if (holding < (newOffset - nullCount)):
                    newFile.write(bytE[holding:(newOffset - nullCount)])
                else:
                    newFile.write(bytE[holding:newOffset])
                newFile.close()
                currentMax = newOffset
                holding = 0
        else:
            if (holding == 0):
                holding = oldOffset
                
        if (os.path.exists(fileName) == True):
            if (os.stat(fileName).st_size == 0):
                os.remove(fileName)
            else:
                newFile = open(fileName, "rb")
                reading = newFile.read()
                newFile.close()
                for i in range(len(reading) - 1):
                    if (reading[i] == 0) and (reading[i + 1] > 0):
                        os.remove(fileName)
                        break
    print(path.split("\\")[-1].split(".")[0].replace("_", " ") + " finished")
    
def mergeFile(folder, path):
    binn2 = open(path, "rb")
    bytE = binn2.read()
    binn2.close()

    langFolder = "_" + path.split("\\")[-1].split(".")[0] + "_" + "langFiles/"
    nulls = [0] * 10000
    currentMax = int.from_bytes(bytE[16:20], "little")
    offsetCount = (currentMax - 12) // 4

    newFile = open("output_" + path.split("\\")[-1], "wb")
    newFile.close()
    newFile = open("output_" + path.split("\\")[-1], "ab")
    newFile.write(bytE[0:16])

    oldOffsetList = []
    newOffsetList = []
    for i in range(offsetCount):
        oldOffsetList.append(int.from_bytes(bytE[(16 + (i * 4)):(20 + (i * 4))], "little"))

    offset = int.from_bytes(bytE[12:16], "little")
    for i in range(offsetCount - 1):
        if (os.path.exists(langFolder + str(i + 1).zfill(4) + ".txt") == True):
            size = os.stat(langFolder + str(i + 1).zfill(4) + ".txt").st_size
            nulls[i] = 4 - (size % 4)
            f = open(langFolder + str(i + 1).zfill(4) + ".txt", "rb")
            r = f.read().decode("UTF-8", errors = "ignore")
            f.close()
            if (r.replace("\0", "") == ""):
                nulls[i] = 0
            offset = offset + size + nulls[i]
            newFile.write(offset.to_bytes(4, "little"))
            newOffsetList.append(offset)
        else:
            thisInt = int.from_bytes(bytE[(16 + (i * 4)):(20 + (i * 4))], "little")
            if (i > 0):
                thisIndex = oldOffsetList[0:i].index(thisInt)
                newFile.write(newOffsetList[thisIndex].to_bytes(4, "little"))
                newOffsetList.append(newOffsetList[thisIndex])
            else:
                newFile.write(bytE[(16 + (i * 4)):(20 + (i * 4))])
                newOffsetList.append(thisInt)

    for i in range(offsetCount):
        if (os.path.exists(langFolder + str(i + 1).zfill(4) + ".txt") == True):
            file = open(langFolder + str(i + 1).zfill(4) + ".txt", "rb")
            newFile.write(file.read())
            newFile.write(bytes(nulls[i]))
            file.close()
    newFile.close()
    os.remove(folder + path.split("\\")[-1])
    os.rename("output_" + path.split("\\")[-1], folder + path.split("\\")[-1])
    print(path.split("\\")[-1].split(".")[0].replace("_", " ") + " finished")

if (os.path.exists("NDS_UNPACK") == False):
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    for root, dirs, files in os.walk("NDS_UNPACK/data/LOC"):
        for file in files:
            if (file.endswith(".lng") == True):
                splitFile("./NDS_UNPACK/data/LOC/", os.path.join(root, file))
else:
    for root, dirs, files in os.walk("NDS_UNPACK/data/LOC"):
        for file in files:
            if (file.endswith(".lng") == True):
                mergeFile("./NDS_UNPACK/data/LOC/", os.path.join(root, file))
    subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
    oldROM = sys.argv[1].split("\\")[-1][0:-4]
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", oldROM + ".nds", "out.nds", "out.xdelta" ])
    psg.popup("You can now play out.nds!", font = "-size 12")