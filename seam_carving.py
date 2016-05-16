import sys

COST = 2
PARENT = 3

def minCost2(p1, p2):
    if(p1[COST] < p2[COST]):
        return p1[0][1] #Return the column of pixel 1
    else:
        return p2[0][1] #Return the column of pixel 2

def minCost3(p1, p2, p3):
    if(p1[COST] < p2[COST]):
        return minCost2(p1, p3)
    else:
        return minCost2(p2, p3)

#Writes a seam to a file
def writeSeam(filename, seam):
    s = filename.split(".")
    newFileName = s[0] + "_output." + s[1] 
    f = open(newFileName, "w")
    f.write("Min Seam: " + str(seam[0][COST]) + "\n")
    for pixel in seam:
        f.write("[" + str(pixel[0][0]) + ", " + str(pixel[0][1]) \
                + ", " + str(pixel[1]) + "]\n")
    f.close()

#Returns the cost analysis for seams of the image
def calcCostMtx(filename):
    f = open(filename)
    pixelMtx = []
    rowIdx = 0
    for line in f:
        row = line.strip().split(",")
        pixelRow = []
        colBound = len(row)
        for col in range(0, colBound):
            if rowIdx > 0:
                prevRow = rowIdx - 1
                if(col == 0 and col == (colBound - 1)):
                    pc = (rowIdx-1, col)
                elif(col == 0):
                    pc = minCost2(pixelMtx[prevRow][col], \
                                  pixelMtx[prevRow][col+1])
                elif(col == (colBound - 1)):
                    pc = minCost2(pixelMtx[prevRow][col], \
                                  pixelMtx[prevRow][col-1])
                else:
                    pc = minCost3(pixelMtx[prevRow][col], \
                                  pixelMtx[prevRow][col-1], \
                                  pixelMtx[prevRow][col+1])

                pixelRow.append(((rowIdx,col), row[col], \
                                 float(row[col]) + pixelMtx[prevRow][pc][COST], \
                                 (rowIdx - 1, pc)))
            else:
                pixelRow.append(((rowIdx,col), row[col], \
                                 float(row[col]), None))
        pixelMtx.append(pixelRow)
        rowIdx += 1
    return pixelMtx

#Returns the minimum cost pixel of a list of pixels
def getMinPixel(pixelList):
    minPixel = None 
    for pixel in pixelList:
        if minPixel is not None:
            if(pixel[COST] < minPixel[COST]):
                minPixel = pixel
        else: minPixel = pixel
    return minPixel 

#Gets a seam by performing a traceback on a pixel
def traceBack(pixel, pixelMtx):
    seam = []
    while(pixel[PARENT] is not None):
        seam.append(pixel)
        row = pixel[PARENT][0]
        col = pixel[PARENT][1]
        pixel = pixelMtx[row][col]
    seam.append(pixel)
    return seam

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print "Input error: expected input file name as argument"
        sys.exit(-1)
    filename = sys.argv[1]
    try:
        costMtx = calcCostMtx(filename)
    except IOError:
        print "Error: Unknown file: " + filename
        sys.exit(-1) 
    minPixel = getMinPixel(costMtx[len(costMtx) - 1])
    seam = traceBack(minPixel, costMtx)
    try:
        writeSeam(filename, seam)
    except IOError:
        print "Error in opening file for writing"
        sys.exit(-1)
