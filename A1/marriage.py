import sys

def main():
    unmatchedKnights, unmatchedLadies = handleInput()
    match(unmatchedKnights, unmatchedLadies)
    
# Saves knights and ladies into dictionaries for String:list key-value pairs
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

def match(unmatchedKnights, unmatchedLadies):
    for knight in unmatchedKnights.copy():
        # Stores the name of the first lady in the knight's list
        lady = unmatchedKnights[knight][0]
        if unmatchedLadies[lady][0] == knight:
            removeFromLists(unmatchedKnights, unmatchedLadies, knight, lady)
            print(unmatchedKnights)
            print(unmatchedLadies)

# Removes knights and ladies from unmatched and the lists of all the others
def removeFromLists(unmatchedKnights, unmatchedLadies, luckyKnight, luckyLady):
    unmatchedKnights.pop(luckyKnight)
    unmatchedLadies.pop(luckyLady)
    for i in unmatchedKnights:
        oldList = unmatchedKnights[i]
        newList = oldList.remove(luckyLady)

main()