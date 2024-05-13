# Ansh Raj Suryavanshi

# Take one uppercase letter and return the soundex coded number for it
def numberize(letter):
    match letter:
        case "R":
            return 6
        case "M"|"N":
            return 5
        case "L":
            return 4
        case "D"|"T":
            return 3
        case "C"|"G"|"J"|"K"|"Q"|"S"|"X"|"Z":
            return 2
        case "B"|"F"|"P"|"V":
            return 1
        case _:
            return 0


# Takes in a word and returns the soundex code for it
def soundex(word):
    word = word.upper()
    
    # Get the first letter off the word
    output = word[0]
    word = word[1:]

    # For every letter left in the word, get the number. Also removes duplicate numbers
    numcode = ""
    prevCode = "0"
    for letter in word:
        numberized = str(numberize(letter))
        if numberized != prevCode:
            numcode += numberized
        prevCode = numberized
    
    # Remove 0's
    numcode = numcode.replace("0", "")

    # Put the first letter back on
    output += numcode

    # Add 0's if too short
    output = output.ljust(4, "0")

    # Make string 4 chars long
    output = output[:4]

    return output