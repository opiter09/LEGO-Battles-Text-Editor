import sys
binn2 = open(sys.argv[1], "rb")
bytE = binn2.read()
binn2.close()

import os
try:
    os.mkdir(sys.argv[1].split("\\")[-1].split(".")[0] + "_" + "langFiles")
except OSError as error:
    pass

zeroList = []
count = 0
holding = 0
currentMax = int.from_bytes(bytE[16:20], "little")
for i in range(12, 0x2FE9, 4):
    count = count + 1

    oldOffset = int.from_bytes(bytE[i:(i + 4)], "little")
    newOffset = int.from_bytes(bytE[(i + 4):(i + 8)], "little")
    if (i == 0x2FE8):
        newOffset = os.stat(sys.argv[1]).st_size
    
    fileName = sys.argv[1].split("\\")[-1].split(".")[0] + "_" + "langFiles/" + str(count).zfill(4) + ".txt"

    if (newOffset > currentMax):
        newFile = open(fileName, "wb")
        if (holding == 0):
            nullCount = bytE[oldOffset:newOffset].decode("UTF-8", errors = "ignore").count("\0")
            if (oldOffset < (newOffset - nullCount)):
                zeroList.append(nullCount)
                newFile.write(bytE[oldOffset:(newOffset - nullCount)])
            else:
                zeroList.append(0)
                newFile.write(bytE[oldOffset:newOffset])
            newFile.close()
            currentMax = newOffset
        else:
            nullCount = bytE[holding:newOffset].decode("UTF-8", errors = "ignore").count("\0")
            if (holding < (newOffset - nullCount)):
                zeroList.append(nullCount)
                newFile.write(bytE[holding:(newOffset - nullCount)])
            else:
                zeroList.append(0)
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

nulls = open(sys.argv[1].split("\\")[-1].split(".")[0] + "_" + "langFiles" + "/ByteCounts.txt", "wt")
nulls.close()
nulls = open(sys.argv[1].split("\\")[-1].split(".")[0] + "_" + "langFiles" + "/ByteCounts.txt", "at")
for number in zeroList:
    nulls.write(str(number) + "\n")
nulls.close()

print("The first unit name is at 387.txt")