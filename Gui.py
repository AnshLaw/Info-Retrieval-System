# Ansh Raj Suryavanshi

# Run this file in the terminal to start the program

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from collections import defaultdict
from soundex import soundex
from termifyDocument import termifyDocument
from query import termifyQuery
import logging
from compileSoundex import compileSoundex


class DocumentUploadTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.documents = defaultdict(dict)                                  # Dictionary to store documents
        self.uploaded_files = []                                            # List for uploaded files
        self.inverted_index = defaultdict(list)                             # Inverted Index intialization
        self.soundex_list = defaultdict(list)                               # Soundex_list initialization

        self.uploaded_documents_label = tk.Label(self, text="Uploaded Documents:", font=("Helvetica", 12, "bold"))
        self.uploaded_documents_label.pack()
        
        self.uploaded_documents_text = tk.Text(self, height=30, width=100)
        self.uploaded_documents_text.pack()

        self.select_folder_button = tk.Button(self, text="Select Folder", command=self.select_folder, font=("Helvetica", 12))
        self.select_folder_button.pack(pady=10)

        self.select_button = tk.Button(self, text="Select Documents", command=self.select_documents, font=("Helvetica", 12))
        self.select_button.pack(pady=10)

        self.update_uploaded_documents_text()
        

    def update_uploaded_documents_text(self):                     # Updates document tab text area
        self.uploaded_documents_text.delete('1.0', tk.END)
        for doc_id, doc_info in self.documents.items():
            self.uploaded_documents_text.insert(tk.END, f"Document ID: {doc_id}, Document Name: {doc_info['name']}\n")
            

    def load_existing_documents(self, directory_path):               # Loads existing files to the system
        if os.path.exists(directory_path):
            for file_name in os.listdir(directory_path):
                full_path = os.path.join(directory_path, file_name)
                if full_path.endswith('.txt'):
                    self.add_document(full_path)
            self.create_inverted_index()
            self.update_uploaded_documents_text()
            print("Loaded existing documents and updated inverted index.")
        else:
            print(f"Directory {directory_path} does not exist.")
    
    
    def select_folder(self):                        # Uploads documents to the program
        folder = filedialog.askdirectory()
        if folder:
            for file in os.listdir(folder):
                if file.endswith('.txt'):
                    self.add_document(os.path.join(folder, file))
            self.update_uploaded_documents_text()
            self.create_inverted_index()
            self.app.inverted_index_tab.update_inverted_index_text() 
            self.app.switch_to_query_tab()                  # Switches to the query tab automatically after documents are uploaded

    def select_documents(self):                            # Uploads documents to the program
        files = filedialog.askopenfilenames()
        for file in files:
            self.add_document(file)
        self.update_uploaded_documents_text()
        self.create_inverted_index()
        self.app.inverted_index_tab.update_inverted_index_text() 
        self.app.switch_to_query_tab()                  
        

    def add_document(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            name = os.path.basename(file)

        
        for doc_id, doc_info in self.documents.items():         # Updation with filename check
            if doc_info['name'] == name :
                print(f"Skipping {file}, already uploaded")
                return
            self.uploaded_files.append(file)

        # If name doesn't exist, proceed with adding the document
        doc_id = len(self.documents) + 1
        words = termifyDocument(file)
        for word in words["terms"]:
            code = soundex(word)
            self.soundex_list[code].append(word)
        self.documents[doc_id] = {'name': os.path.basename(file), 'word_freq': words["terms"], 'soundex': self.soundex_list, 'Total Words': words["wordsEncountered"], 'Distinct Words': words["uniqueWords"]}
        uploaded_files_dir = "uploaded_files"
        if not os.path.exists(uploaded_files_dir):
            os.makedirs(uploaded_files_dir)
        uploaded_file_path = os.path.join(uploaded_files_dir, os.path.basename(file))
        with open(uploaded_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
    
    def create_inverted_index(self):                    # inverted index created
        self.inverted_index = defaultdict(list)
        for doc_id, doc_info in self.documents.items():
            for word, freq in doc_info['word_freq'].items():
                self.inverted_index[word].append((doc_id, freq))
        self.app.inverted_index_tab.update_inverted_index_text() 
        

class InvertedIndexTab(tk.Frame):
    def __init__(self, parent, document_upload_tab):
        super().__init__(parent)
        self.document_upload_tab = document_upload_tab
        self.distinct_freq = 0

        self.inverted_index_label = tk.Label(self, text="Inverted Index:", font=("Helvetica", 12, "bold"))
        self.inverted_index_label.pack()
        
        self.refresh_button = tk.Button(self, text="Refresh Documents and Index", command=self.refresh_documents_and_index, font=("Helvetica", 12))
        self.refresh_button.pack(pady=10)

        self.inverted_index_text = tk.Text(self, height=40, width=100)
        self.inverted_index_text.pack()
        
    
    def refresh_documents_and_index(self):                                  # Reloads the inverted index if any changes to a file is made or a new file is added without rerunning the whole program
        self.document_upload_tab.documents.clear()
        self.document_upload_tab.load_existing_documents('uploaded_files')

    def update_inverted_index_text(self):                                               # Updates the inverted index text area
        self.inverted_index_text.delete('1.0', tk.END)
        for token, postings in sorted(self.document_upload_tab.inverted_index.items()):
            total_freq = sum(freq for _, freq in postings)
            self.inverted_index_text.insert(tk.END, f"{token}[{total_freq}]: {postings}\n")
                  
class QueryTab(tk.Frame):
    def __init__(self, parent, document_upload_tab):
        super().__init__(parent)

        self.document_upload_tab = document_upload_tab

        self.query_input = tk.Entry(self, font=("Helvetica", 12))
        self.query_input.pack(pady=10)

        radio_frame = tk.Frame(self)                   # Radio buttons for "AND" and "OR"
        radio_frame.pack(fill='x')
        self.search_mode = tk.StringVar(value="AND")
        self.radio_and = tk.Radiobutton(radio_frame, text="AND", variable=self.search_mode, value="AND")
        self.radio_and.pack(side=tk.LEFT, expand=True)
        self.radio_or = tk.Radiobutton(radio_frame, text="OR", variable=self.search_mode, value="OR")
        self.radio_or.pack(side=tk.LEFT, expand=True)

        self.execute_button = tk.Button(self, text="Execute Query", command=self.execute_query, font=("Helvetica", 12))
        self.execute_button.pack()

        self.result_label = tk.Label(self, text="Search Result: ", font=("Helvetica", 12, "bold"))
        self.result_label.pack(pady=10)
        
        self.query_text = tk.Text(self, height = 20, width = 100)
        self.query_text.pack()
        
    def open_document(self,path):
        if os.path.exists(path):
            os.startfile(path)

    def execute_query(self):
        self.query_text.delete('1.0', tk.END)
        self.root = tk.Toplevel()
        self.root.title('Document Opener')              # Document linker window
        self.root.geometry('400x800')
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)        # Added scroll to the document opener window
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
            
        query = termifyQuery(self.query_input.get())
        search_mode = self.search_mode.get()
    
        soundex_list = self.document_upload_tab.soundex_list
        
        inverted_index = self.document_upload_tab.inverted_index
        if not inverted_index:
            self.result_label.config(text="Inverted Index not created yet!")
            return

        result_docs = []
        soundex_result = {}
        term =[]
        final_ids = {}

        final_ids = {token: set(doc_id for doc_id, _ in inverted_index[token]) for token in query if token in inverted_index}           # taking unique document ids for all tokens
                
        
        for token in query:
            for key, val in soundex_list.items():
                for i in val:
                    if i == token:
                        soundex_result[token] = key 
            term = token
            if soundex_result:                                      # Spits out soundex code for each token of the query
                result_str1 = f"Soundex in query:\n"
                sorted_soundex = sorted(soundex_result.items(), key=lambda item: item[0], reverse=False)
                for term, soundx in sorted_soundex:
                    result_str1 += f"Soundex for '{term}': {soundx}\n"
            else:
                result_str1 = "No soundex found for the query.\n"
                
        if search_mode == "AND":
            if len(final_ids) != len(query):  # Check if all query terms were found in the inverted_index
                self.query_text.insert('1.0', "No documents match all terms of the query.")
                return
            doc_list = set.intersection(*final_ids.values())
        else:  # OR logic
            doc_list = set.union(*final_ids.values()) if final_ids else set()

        if not doc_list:
            self.query_text.insert('1.0', "No documents match the query.")
            return
        
        doc_freqs = {}
        for token in query:
            if token in inverted_index:
                for doc_id, freq in inverted_index[token]:
                    if doc_id in doc_list:
                        if doc_id in doc_freqs:
                            doc_freqs[doc_id] += freq
                        else:
                            doc_freqs[doc_id] = freq        # Simple ranking by adding the frequencies of all query tokens found in the document

        result_docs = [(doc_id, self.document_upload_tab.documents[doc_id]['name'], doc_freqs[doc_id]) for doc_id in doc_list if doc_id in doc_freqs]

        # Sort by  query frequency
        result_docs.sort(key=lambda x: x[2], reverse=True)          
                        
        directory_path = 'C:\\Users\\anshr\\Desktop\\Info Retrieval System\\uploaded_files'
    
        result_str2 = "Documents containing the query:\n"
        for doc_id, doc_name, query_freq in result_docs:
            result_str2 += f"Document ID: {doc_id}, Document Name: {doc_name}, Query Frequency: {query_freq}\n"
            full_path = os.path.join(directory_path, doc_name)
            button = tk.Button(scrollable_frame, text=f"Open Document ({doc_id}) {doc_name}", command=lambda p=full_path: self.open_document(p))
            button.pack(side='top', fill='x', padx=10, pady=2)
                             
        self.query_text.insert('1.0', result_str1 + result_str2)      
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")          
        self.root.mainloop()
            


class StatisticsTab(tk.Frame):                                                                                              # Dumping and displaying statistics start here
    def __init__(self, parent, document_upload_tab, inverted_index_tab, loggers):
        super().__init__(parent)
        self.document_upload_tab = document_upload_tab
        self.inverted_index_tab = inverted_index_tab
        self.loggers = loggers
        self.label = tk.Label(self, text="Statistics", font=("Helvetica", 12, "bold"))
        self.label.pack(pady=10)
        
        self.stats_text = tk.Text(self, height=20, width=100)
        self.stats_text.pack(pady=10)
        
        self.update_stats_button = tk.Button(self, text="Document Statistics", command=self.document_statistics)
        self.update_stats_button.pack(pady=10)
        
        self.update_stats1_button = tk.Button(self, text="Collection Data", command=self.collection_statistics)
        self.update_stats1_button.pack(pady=10)
        
        self.rank_button = tk.Button(self, text="Calculate Frequent Words", command=self.update_and_display_ranked_words)
        self.rank_button.pack( pady=10)
        
        self.display_index_button = tk.Button(self, text="Inverted Index", command=self.display_inverted_index)
        self.display_index_button.pack(pady=10)
        
        self.soundex_button = tk.Button(self, text="Calculate Soundex", command=self.update_and_display_soundex)
        self.soundex_button.pack(pady=10)
        
        self.document_statistics()  # Initial update

    def document_statistics(self):
        self.stats_text.delete('1.0', tk.END)
        directory_path = 'C:\\Users\\anshr\\Desktop\\Info Retrieval System\\uploaded_files'
        stats_message = ""
        
        total_words = 0
        
        for doc_id, doc_info in self.document_upload_tab.documents.items():
            path = doc_info.get('name')
            full_path =  os.path.join(directory_path, doc_info['name'])
            num_distinct_words = doc_info.get('Distinct Words')
            num_total_words = doc_info.get('Total Words')
            total_words += num_total_words
            stats_message += f"Document {doc_id} ({path}):\nDistinct Words: {num_distinct_words}\nTotal Words: {num_total_words}\n\n"
            self.stats_text.insert('1.0', stats_message)
            self.loggers['general_stats'].info(f"Document {doc_id} ({path}):\nDistinct Words: {num_distinct_words}\nTotal Words: {num_total_words}\n\n")
         
    def collection_statistics(self):
        self.stats_text.delete('1.0', tk.END)
        stats_message = ""
        total_words = 0
        all_words = set()
        
        for doc_id, doc_info in self.document_upload_tab.documents.items():
            num_total_words = doc_info.get('Total Words')
            total_words += num_total_words
            all_words.update(set(list(doc_info['word_freq'].keys())))
   
        total_documents = len(self.document_upload_tab.documents)
        if total_documents:
            stats_message += f"Overall Statistics for All Documents:\n"
            stats_message += f"Total Documents in the Collection: {total_documents}\n"
            stats_message += f"Total Distinct Words in Collection: {len(all_words)}\n"
            stats_message += f"Total Words in Collection: {total_words}\n"
            self.stats_text.insert('1.0', stats_message)
            self.loggers['general_stats'].info(f"Total documents: {total_documents}")
            self.loggers['general_stats'].info(f"Total words: {total_words}")
            self.loggers['general_stats'].info(f"Distinct words without stop words: {len(all_words)}")
        
    def aggregate_word_frequencies(self):
        word_frequencies = {}
        for word, postings in self.document_upload_tab.inverted_index.items():
            total_frequency = sum(freq for _, freq in postings)
            word_frequencies[word] = total_frequency
        return word_frequencies

    def find_specific_ranks(self, word_frequencies):
        sorted_words = sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)
        ranks = [0, 99, 499, 999]
        rank_results = {}
        for rank in ranks:
            if rank < len(sorted_words):
                rank_results[rank + 1] = sorted_words[rank]
            else:
                rank_results[rank + 1] = ("Not enough words", 0)
        return rank_results

    def update_and_display_ranked_words(self):
        word_frequencies = self.aggregate_word_frequencies()
        rank_results = self.find_specific_ranks(word_frequencies)
        self.display_rank_results(rank_results)

    def display_rank_results(self, rank_results):
        self.stats_text.delete('1.0', tk.END) 
        for rank, (word, freq) in rank_results.items():
            if rank == 1:
                self.stats_text.insert(tk.END, f"The most frequent word is '{word}' with a frequency of {freq}.\n")
            else:
                self.stats_text.insert(tk.END, f"The {rank}th most frequent word is '{word}' with a frequency of {freq}.\n")
            self.loggers['ranked_frequency'].info(f"Rank {rank} Word: {word} Frequency: {freq}")
            
    
    def update_and_display_soundex(self):
        self.stats_text.delete('1.0', tk.END)
        for doc_id, doc_info in self.document_upload_tab.documents.items():
            Soundex_log = compileSoundex(list(doc_info['word_freq'].keys()))
            for code, word in Soundex_log['soundex'].items():
                self.stats_text.insert(tk.END, f"Soundex {code}: {', '.join(word)}\n")
                self.loggers['soundex'].info(f"Soundex {code}: {', '.join(word)}")
                
            
    def display_inverted_index(self):
        self.stats_text.delete('1.0', tk.END)
        for word, postings in sorted(self.inverted_index_tab.document_upload_tab.inverted_index.items()):
            total_freq = sum(freq for _, freq in postings)
            postings_str = ', '.join(f"[ {doc_id},{freq}]" for doc_id, freq in postings)
            self.stats_text.insert(tk.END, f"{word}[{total_freq}]: {postings_str}\n")
            log_message = f"{word}[{total_freq}]: {postings_str}\n"
            self.loggers['inverted_index'].info(log_message)
            
class SoundexTab(tk.Frame):                                                                        # Soundex Searching to search for terms with same soundex code
    def __init__(self, parent, document_upload_tab, loggers):
        super().__init__(parent)
        self.document_upload_tab = document_upload_tab
        self.loggers = loggers
        self.label = tk.Label(self, text="Enter search term or soundex:", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.search_entry = tk.Entry(self, font=("Helvetica", 12))
        self.search_entry.pack(pady=10)
        
        radio_frame = tk.Frame(self)                # Radio buttons to search by term or soundex code
        radio_frame.pack(fill='x')
        self.search_mode = tk.StringVar(value="term")
        self.radio_term = tk.Radiobutton(radio_frame, text="Search by Term", variable=self.search_mode, value="term")
        self.radio_term.pack(side=tk.LEFT, expand=True)
        self.radio_soundex = tk.Radiobutton(radio_frame, text="Search by Soundex Code", variable=self.search_mode, value="soundex")
        self.radio_soundex.pack(side=tk.LEFT, expand=True)
        self.search_button = tk.Button(self, text="Search", command=self.perform_soundex_search)
        self.search_button.pack(pady=10)

        self.results_text = tk.Text(self, height=20, width=100)
        self.results_text.pack(pady=10) 

    def perform_soundex_search(self):
        search_term = self.search_entry.get()
        search_mode = self.search_mode.get()
        if search_mode == "term":
            soundex_code = soundex(search_term)
            # self.results_text.insert(tk.END, f"Soundex for '{search_term}' is {soundex_code}\n")
            matches = []
            matches.append(f"Soundex for '{search_term}' is {soundex_code}\n")
            matches.append(f"Terms with same soundex code as '{search_term}':\n")
            
            # Search for matching Soundex codes in the indexed documents
            for doc_id, doc_info in self.document_upload_tab.documents.items():
                Soundex_log = compileSoundex(list(doc_info['word_freq'].keys()))
                for code, word in Soundex_log['soundex'].items():
                    if code == soundex_code:
                        matches.append(f"Doc ID {doc_id},{doc_info['name']}: {word}")

            # Display results
            self.results_text.delete('1.0', tk.END)
            if matches:
                for match in matches:
                    self.results_text.insert(tk.END, f"{match}\n")
            else:
                self.results_text.insert(tk.END, "No matches found.")
            
        elif search_mode == "soundex":
            soundex_code = search_term
            matches = []
            matches.append(f"Terms with same soundex code '{soundex_code}':\n")

           
            for doc_id, doc_info in self.document_upload_tab.documents.items():
                Soundex_log = compileSoundex(list(doc_info['word_freq'].keys()))
                for code, word in Soundex_log['soundex'].items():
                    if code == soundex_code:
                        matches.append(f"Doc ID {doc_id},{doc_info['name']}: {word}")

           
            self.results_text.delete('1.0', tk.END)
            if matches:
                for match in matches:
                    self.results_text.insert(tk.END, f"{match}\n")
            else:
                self.results_text.insert(tk.END, "No matches found.")


def clear_log_files_and_reset_loggers():                                                            # Implementing file logging to dump statistics
    log_directory = "logs"
    log_files = ["inverted_index.log", "ranked_frequency.log", "general_stats.log", "soundex.log"]
    loggers = ["inverted_index", "ranked_frequency", "general_stats", "soundex"]

    # Close all loggers
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            handler.close()  # Close each handler to flush and stop using the file
            logger.removeHandler(handler)  # Remove handler from logger

    # Clear files
    for log_file in log_files:
        open(os.path.join(log_directory, log_file), 'w').close()

    # Re-add handlers
    setup_logging()

def setup_logging():
        
        log_directory = "logs"
        os.makedirs(log_directory, exist_ok=True)  # Ensure log directory exists
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
        
        # Handlers for different logs
        handlers = {
            "inverted_index": logging.FileHandler(f"{log_directory}/inverted_index.log", mode='w'),
            "ranked_frequency": logging.FileHandler(f"{log_directory}/ranked_frequency.log", mode='w'),
            "general_stats": logging.FileHandler(f"{log_directory}/general_stats.log", mode='w'),
            "soundex": logging.FileHandler(f"{log_directory}/soundex.log", mode='w')
        }

        # Formatters define the log message format.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Assign formatter to each handler
        for handler in handlers.values():
            handler.setFormatter(formatter)

        # Create loggers and assign the respective handlers
        loggers = {
            "inverted_index": logging.getLogger("inverted_index"),
            "ranked_frequency": logging.getLogger("ranked_frequency"),
            "general_stats": logging.getLogger("general_stats"),
            "soundex": logging.getLogger("soundex")
        }

        for key, logger in loggers.items():
            logger.addHandler(handlers[key])

        return loggers

class Application(tk.Tk):                                   # Main GUI window to display all tabs and interface
    def __init__(self):
        super().__init__()
        self.title("Information Retrieval System")
        
        self.geometry("1280x720")

        self.configure(bg="#f0f0f0")

        self.tabControl = ttk.Notebook(self)

        self.document_upload_tab = DocumentUploadTab(self.tabControl, self)
        self.soundex_tab = SoundexTab(self.tabControl, self.document_upload_tab, loggers)
        self.inverted_index_tab = InvertedIndexTab(self.tabControl, self.document_upload_tab)
        self.query_tab = QueryTab(self.tabControl, self.document_upload_tab)
        self.statistics_tab = StatisticsTab(self.tabControl, self.document_upload_tab, self.inverted_index_tab, loggers)

        self.tabControl.add(self.document_upload_tab, text = "Document Upload")
        self.tabControl.add(self.inverted_index_tab, text = "Inverted Index")
        self.tabControl.add(self.query_tab, text = "Query")
        self.tabControl.add(self.soundex_tab, text="Soundex Search")
        self.tabControl.add(self.statistics_tab, text="Statistics")
        
        documents_directory = 'C:\\Users\\anshr\\Desktop\\Info Retrieval System\\uploaded_files'
        self.document_upload_tab.load_existing_documents(documents_directory)           # Loads data if it exists already in the directory
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        self.clear_logs_button = ttk.Button(self, text="Clear Log Files", command=clear_log_files_and_reset_loggers)
        self.clear_logs_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.tabControl.pack(expand=1, fill="both")

    def switch_to_query_tab(self):
        self.document_upload_tab.inverted_index = self.document_upload_tab.inverted_index  # Keeping the inverted index intact
        self.tabControl.select(self.query_tab)
        
    

if __name__ == "__main__":
    loggers = setup_logging()
    app = Application()                 # Running the application
    app.mainloop()

