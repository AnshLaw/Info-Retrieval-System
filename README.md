# Info-Retrieval-System
Information Retrieval System to parse through a collection of documents

Import libraries:
tkinter(used for GUI)
os(used for file operations)
collections(used to call default dictionary features)
logging(used to log data)

Functions implemented:
soundex(created to output soundex of a term)
termifyDocument(created to tokenize documents)
query(created to simply give in queries)
compileSoundex(created to output soundex dictionary for all terms)

The file Gui.py should be ran in the terminal for the program to open. After the window pulls up upload the 'data' folder to the upload all files. 

For our data set, we used
F Scott Fitzgerald - The Great Gatsby,
Mark Twain - The Adventures of Huckleberry Finn,
The intro to Jerry Sinefeld - The Bee Movie, 
Homer - The Odyssey

We are using 1044 text files for our database.

The function Termify Document removes the following characters:
!,.“"”():;?0123456789&|—_*#$%-[]{}=/\:
Additionally, the entire format is made lowercase.
Words are seperated using the built-in split() function.
Stop words:["a", "an", "the", "of", "and"] are removed from the document when tokenizing.

A tally of all encountered words and all the unique terms are kept, as well as
individual tallies of each individual term.

We have DocumentUploadTab, InvertedIndexTab, QueryTab, SoundexTab and StatisticsTab for different functions

In DocumentUploadTab we have functions like load_existing_documents, select_folder, select_documents to upload documents into our system.
We add documents using this class which in turn creates the inverted index parsing through all the uploaded documents.
These uploaded documents are are stored in a directory named "uploaded_files".

In InvertedIndexTab we have functions like refresh_documents_and_index and update_inverted_index_text used to update the inverted index when you make changes to an existing file or add a new file.

In QueryTab we have simple query executions using "AND" and "OR"
We have used a simple ranking mechanism where the frequencies of all tokens of the query are added for each document and then sorted on its basis.
We also show the soundex for each query token.

In SoundexTab we search for terms using soundex code or just search a term and find other terms with same soundex codes.


In StatisticsTab we have functions to report different stats about the system like 
Report the number of distinct words observed in each document, and the total number of
words encountered.
Report the number of distinct words observed in the whole collection of documents, and the
total number of words encountered.
Report the total number of times each word is seen (term frequency) and the document IDs
where the word occurs (Output the posting list for a term).
Report the top 1st, 100th, 500th, and 1000th most-frequent word and their frequencies of
occurrence.
All this information is dumped into log files and the files reset when you run the program again.

Please note even if a document is located with a key, the value may not exist exactly as shown on the key in the document.

As EXTRA CREDIT:
Added ranking mechanism for queries using sorting documents by max query frequency.
Added Soundex Searching to find all terms with the same soundex by searching through the soundex code or terms.
Added Soundex logging in Statistics to give a collection of all terms with their respective soundex codes.


References:
Text files:
https://www.gutenberg.org/

Other references:
https://www.geeksforgeeks.org/
https://www.w3schools.com/




