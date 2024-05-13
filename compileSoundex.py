# Ansh Raj Suryavanshi

from soundex import *

# Take an array of words in and return a key-value list by soundex
def compileSoundex(wordArray):
    # This function already assumes all inputs have been cleaned
    output = {
        "soundex": {}
    }

    # Loop through every word and catorgorize them by soundex
    for word in wordArray:
        
        soundOfWord = soundex(word)

        if not soundOfWord in output["soundex"]:
            # Soundex isn't in terms list, add it
            output["soundex"][soundOfWord] = [word]
        else:
            # Add word to the existing soundex position
            output["soundex"][soundOfWord].append(word)
    
    # Sort by soundex entry
    output["soundex"] = dict(sorted(output["soundex"].items()))

    return output
