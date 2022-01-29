import sys

def main():
    unmatchedKnights, unmatchedLadies = handleInput()
    

def handleInput():
    fileName = sys.argv[1]
    unmatchedKnights = {}
    unmatchedLadies  = {}

    try:
        with open(fileName, "r") as f:
            pairs = int(f.readline()) 
            for i in range(pairs * 2):
                line = f.readline()
                names = line.split()
                if i < pairs: 
                    unmatchedKnights[names[0]] = names[1:]
                else: 
                    unmatchedLadies[names[0]] = names[1:]
            return unmatchedKnights, unmatchedLadies
    except:
        print("Exited")
        exit(1)

main()