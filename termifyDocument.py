# Ansh Raj Suryavanshi

bannedChars = '!,.“"”():;?0123456789&|—_*#$%-[]{}=/\:'

# Stop words must be an exact match to be removed from the term list
stopWords = ["a", "an", "the", "of", "and", "to"]

# Takes an input file from the data folder by name, and returns a sorted dictionary of terms with parsing
def termifyDocument(inputFile, encoding= 'utf-8'):
    # Open the file, convert it all to lowercase
    f = open(inputFile, "r", encoding= encoding)
    text = f.read()
    text = text.lower()

    # Loop through every character and get rid of it if it's banned
    for char in text:
        if char in bannedChars:
            text = text.replace(char, "")

    # Break the input string into a list of words
    listOfWords = text.split()

    # Create the output dict to work from
    output = {
        "name": inputFile,
        "wordsEncountered": len(listOfWords),
        "uniqueWords": 0,
        "terms": {}
    }

    # Loop through every word and make sure the count is accurate
    for word in listOfWords:
        if not word in output["terms"]:
            # Word isn't in terms list, add it
            output["terms"][word] = 1
        else:
            # Increment term by 1
            output["terms"][word] += 1

    # Sort the term list into alphabetical order
    output["terms"] = dict(sorted(output["terms"].items()))
    output["uniqueWords"] = len(output["terms"])

    # Remove stopwords without affecting the unique term count
    for term in stopWords:
        output["terms"].pop(term, "not present")

    return output