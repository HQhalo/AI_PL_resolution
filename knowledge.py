
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
            if temp in self.words:
                rowMatrix[self.words[temp]] = value
        return rowMatrix
    def toSentence(self,M):
        if len(M) != self.NoWords:
            print("err")
            return None
        else:
            sen =""
            for i in range(self.NoWords):
                if M[i] == 1:
                    if sen != "":
                        sen+=" OR "
                    sen += self.charCount[i]
                if M[i] == -1:
                    if sen != "":
                        sen+=" OR "
                    sen += "-"
                    sen += self.charCount[i]
            if sen == "":
                sen +="{}"
            return sen 
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
        rel = []
        for i in range(len(alpha)):
            if alpha[i] != 0:
                temp = [0 for x in range(self.NoWords)]
                temp[i] = - alpha[i]
                rel.append(temp)
        return rel
    def PL_resolution(self,alpha):
        flag , rel = self.PL_resolutionHelper(alpha)
        PLs = []
        if rel != None:
            for i in rel:
                pl = []
                for j in i:
                    pl .append(self.toSentence(j))
                PLs.append(pl)
        return flag,PLs
    def PL_resolutionHelper(self,alpha):
        alphaToken = self.splitLine(alpha)
        rowAlpha = self.sentenceToMatrix(alphaToken)
        rowAlphaNegative = self.negative(rowAlpha)

        empty = [0 for x in range(self.NoWords)]

        alphaMatrix = self.matrix.copy()
        alphaMatrix += rowAlphaNegative

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
                alphaMatrix,added= self.combine(newPLs,alphaMatrix)
                relPls.append(added)
            else:
                relPls.append([])
                return "NO1",relPls
            if empty in newPLs:
                return "YES",relPls
            if len(added) == 0:
                return "NO2",relPls
            m = len(alphaMatrix)
        return 0
