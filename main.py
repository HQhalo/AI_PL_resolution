from knowledge import *
def input(path):
    f = open(path,"r")
    lines = f.readlines()    
    alpha = lines[0][:-1]
    N = int(lines[1])
    propositionals = lines[2:]
    for i in range(len(propositionals)-1):
        propositionals[i] = propositionals[i][:-1]
    KB = knowledge(propositionals)
   

    flag , rel = KB.PL_resolution(alpha)
    for i in rel:
        for j in i:
            for k in j:
                print(k,end=" ")
            print("\n")
        print("______")
    print(flag)

    
if __name__ == "__main__":
    input("input.txt")