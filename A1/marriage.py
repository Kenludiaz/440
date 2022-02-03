import sys
import time 

def main():
    start = time.perf_counter()
    unmatchedKnights, unmatchedLadies = handleInput()
    match(unmatchedKnights, unmatchedLadies)
    print(f"Completed Execution in {time.perf_counter() - start} seconds")
    
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
                if len(names) > pairs + 1:
                    raise Exception()

                if i < pairs: 
                    unmatchedKnights[names[0]] = names[1:]
                else: 
                    unmatchedLadies[names[0]] = names[1:]
            return unmatchedKnights, unmatchedLadies
    except:
        exit(1)

def match(unmatchedKnights, unmatchedLadies):
    engagedKnights = []
    unenagedKnights = [*unmatchedKnights.keys()]

    engagedLadies = []

    while unenagedKnights:
        for knight in unenagedKnights:
            # Stores the name of the first lady in the knight's list
            lady = unmatchedKnights[knight][0]

            # MAYBE, lady not yet proposed to
            if (lady not in engagedLadies):
                engagedKnights.append(knight)
                engagedLadies.append(lady)
                unenagedKnights.remove(knight)

                # Remove knights of lower preference
                removeLowerKnights(unmatchedLadies, lady, knight)

            # MAYBE, was proposed to by a knight of higher preference
            elif (knight in unmatchedLadies[lady]):
                # Undo the previous engagement
                index = engagedLadies.index(lady)
                engagedLadies.pop(index)
                leftoverKnight = engagedKnights.pop(index)
                unenagedKnights.append(leftoverKnight)

                # Re-propose
                # Lady is removed and then re-added to have the pairings share an index 
                engagedKnights.append(knight)
                engagedLadies.append(lady)
                unenagedKnights.remove(knight)

                removeLowerKnights(unmatchedLadies, lady, knight)
            
            # NO, the knight should never ask the same lady again
            else:
                unmatchedKnights[knight].pop(0)

    # The people that were engaged will now finally tie the knot
    # The couples will have the same index
    # This prevents the wrong couples from being printed.
    for x in range(len(engagedLadies)):
        print(engagedKnights[x], engagedLadies[x])

# Removes knights with a lower preference than the one given
def removeLowerKnights(unmatchedLadies, lady, knight):
    index = unmatchedLadies[lady].index(knight)

    for i in range(len(unmatchedLadies[lady]) - index - 1):
        unmatchedLadies[lady].pop()
    

main()
