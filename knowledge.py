
class knowledge:
    
    def __init__(self,PLs):
        listPls = []
        # split each line, add the line into list 
        for PL in PLs:
            listPls.append(self.splitLine(PL))
       
        # count words
        self.charCount = self.countWords(listPls)
        self.charCount.sort()

        # create dictionary of word to store index in matrix
        self.words = {}
        self.NoWords = 0
        for i in self.charCount:
            self.words[i] = self.NoWords
            self.NoWords +=1

        # create matrix to represent KB
        # matrix[i][j] = 
        #   0   :if this word doesn't appear in i'th sentence
        #   1   :if this word is positive
        #   -1  :if this word is negative
        self.matrix = []
        for i in listPls:
            self.matrix.append(self.sentenceToMatrix(i))

    def splitLine(self,line):
        tokens = line.split()
        temp = []
        for i in tokens:
            if i != "OR":
                temp.append(i)
        return temp
  
    def countWords(self, listPls):
        charCount = []
        for line in listPls:
            for word in line:
                temp = word
                if word[0] == "-":
                    temp = temp[1:]
                if not temp in charCount:
                    charCount.append(temp)
        return charCount
   
    def sentenceToMatrix(self,PL):
        rowMatrix = [0 for x in range(self.NoWords)]
        for word in PL:
            temp = word
            value = 1
            if temp[0] == "-":
                temp = temp[1:]
                value = -1
            rowMatrix[self.words[temp]] = value
        return rowMatrix

    def resolutionHelper(self,PL1,PL2,index):
        re = [0 for x in range(self.NoWords)]
        if abs(PL1[index] - PL2[index]) != 2 :
            return False,None
        else:
            for i in range(self.NoWords):
                if i != index:
                    add = PL1[i] + PL2[i]
                    if add == 0:
                        if PL1[i] != 0:
                            return False, None
                    elif add == 2 :
                        re[i] = 1
                    elif add == -2:
                        re[i] = -1
                    else:
                        re[i] = add
        return True, re    

    def resolution(self,PL1,PL2):
        rel = []
        flag = False
        for i in range(self.NoWords):
            f ,re = self.resolutionHelper(PL1,PL2,i)
            if f == True :
                flag = True
                rel.append(re)
        return rel 

    def combine(self,PL1,PL2):
        added = []
        if len(PL2) == 0:
            return PL1,PL1
        else:
            rel = PL2.copy()
        for i in PL1:
            if not i in PL2 :
                rel.append(i)
                added.append(i)
        return rel,added

    def negative(self,alpha):
        for i in range(len(alpha)):
            alpha[i] = -alpha[i]
        return alpha
        
    def PL_resolution(self,alpha):
        alphaToken = self.splitLine(alpha)
        try:
            rowAlpha = self.sentenceToMatrix(alphaToken)
            rowAlpha = self.negative(rowAlpha)
        except:
            return "NO1",None

        empty = [0 for x in range(self.NoWords)]

        alphaMatrix = self.matrix.copy()
        alphaMatrix.append(rowAlpha)

        m = len(alphaMatrix)
        newPLs = []
        relPls = []
        while True:     
            rel = []
            for i in range(m):
                for j in range(m):
                    temp = self.resolution(alphaMatrix[i],alphaMatrix[j])
                    for k in temp:
                        if not k in rel:
                            rel.append(k)
            if len(rel) != 0:
                newPLs,plM = self.combine(rel,newPLs)
            else:
                return "NO",relPls
            if len(plM) == 0:
                return "NO2",relPls
            alphaMatrix,added= self.combine(newPLs,alphaMatrix)
            if len(added) == 0:
                return "NO3",relPls
            relPls.append(added)
            if empty in newPLs:
                return "YES",relPls
            m = len(alphaMatrix)
        return 0
