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
    matched = {}
    engagedKnights = []
    unenagedKnights = [*unmatchedKnights.keys()]

    engagedLadies = []

    for x in range(1,20):
        for knight in unenagedKnights:
            # Stores the name of the first lady in the knight's list
            lady = unmatchedKnights[knight][0]

            # YES, there are no knights of higher preference in the lady's list
            if unmatchedLadies[lady][0] == knight:
                removeFromLists(matched, unmatchedKnights, unmatchedLadies, knight, lady)
                unenagedKnights.remove(knight)

            # MAYBE, not yet proposed to
            elif (lady not in engagedLadies):
                engagedKnights.append(knight)
                engagedLadies.append(lady)
                unenagedKnights.remove(knight)
                # Remove knights of lower preference
                # removeLowerKnights(unmatchedLadies, lady, knight)

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


            # # NO, the lady already has a knight of higher preference
            # Remove knights of lower preference


    # The people that were engaged will now finally tie the knot and will have the same index

    print(matched)

# Removes knights and ladies from unmatched and the preference lists of all the others
def removeFromLists(matched, unmatchedKnights, unmatchedLadies, luckyKnight, luckyLady):
    unmatchedKnights.pop(luckyKnight)
    unmatchedLadies.pop(luckyLady)
    for i in unmatchedKnights:
        unmatchedKnights[i].remove(luckyLady)
    for j in unmatchedLadies:
        unmatchedLadies[j].remove(luckyKnight)

    matched[luckyKnight] = luckyLady

# Removes knights with a lower preference than the one given
def removeLowerKnights(unmatchedLadies, lady, knight):
    index = unmatchedLadies[lady].index(knight)

    for i in range(len(unmatchedLadies), index, -1):
        print("Removed element", unmatchedLadies[lady].pop())

main()
