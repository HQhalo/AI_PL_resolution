from knowledge import *

def input(path):
    f = open(path,"r")
    lines = f.readlines()    
    alpha = lines[0][:-1]
    N = int(lines[1])
    PLs = lines[2:2+N]
    for i in range(len(PLs)-1):
        PLs[i] = PLs[i][:-1]
    return alpha,knowledge(PLs)
   
def output(path,flag, PLs):
    f = open(path,"w")
    if PLs != None:
        for i in PLs:
            f.write(str(len(i))+"\n")
            for j in i:
                f.write(j+"\n")
    f.write(flag)

    
if __name__ == "__main__":
    alpha,KB = input("input.txt")
    flag , PLs = KB.PL_resolution(alpha)
    output("output.txt",flag , PLs)
    