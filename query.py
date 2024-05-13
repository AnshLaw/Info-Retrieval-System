# Ansh Raj Suryavanshi

# This import makes sure the bannedChars list is consistent
from termifyDocument import bannedChars

# Takes a query input and parses it to the same format as the document termifier
def termifyQuery(inputQuery):
    # Make query lowercase
    inputQuery = inputQuery.lower()

    # Remove banned chars from the query
    for char in inputQuery:
        if char in bannedChars:
            inputQuery = inputQuery.replace(char, "")

    # Break the input string into a list of words
    QueryList = inputQuery.split()

    # Sort the query and return the list of terms to search for
    return(sorted(QueryList))
