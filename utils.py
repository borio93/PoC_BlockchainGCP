import hashlib
import time
import pickle
import os
from google.cloud import storage
from colorama import Fore, Style, init, Back
import signal
import sys
from datetime import datetime


def save_blockchain(blockchain, file_name="/home/jupyter/Blockchain/tmp/blockchain test/blockchain.pickle"):
    with open(file_name, "wb") as file:
        pickle.dump(blockchain, file)


def load_blockchain(file_name="blockchain.pickle", ):
    try:
        with open('/home/jupyter/Blockchain/tmp/blockchain test/' + file_name, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        return None
    
def download_file():
    bucket_name = "test_blockchain"
    folder_name = "blockchain test/"
    local_folder_path = '/home/jupyter/Blockchain/tmp'

    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    # Inizializza il client di GCS
    storage_client = storage.Client()

    # Ottiene una lista di nomi di file nella cartella del bucket
    blobs = storage_client.list_blobs(bucket_name, prefix=folder_name)

    # Itera su tutti i file nella cartella e scarica ciascun file nella directory locale
    for blob in blobs:
        if '.' in os.path.basename(blob.name):  
            local_file_path = os.path.join(local_folder_path, os.path.dirname(blob.name))
            #print('local file path: ' + str(local_file_path))
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            # Scarica il file nella directory locale
            blob.download_to_filename(os.path.join(local_folder_path, blob.name))
            #print(str(blob.name) + ' downloaded')    
            #ricrea tutta l'alberatura di storage
    
def upload_file():
    
    # Impostare il client
    client = storage.Client()
    # Impostare il nome del bucket nel quale vogliamo salvare i files
    bucket_name = "test_blockchain"
    folder_name = "blockchain test"

    # Impostare il bucket
    bucket = client.bucket(bucket_name)

    # Impostare il path della directory temporanea
    temp_directory_path = "/home/jupyter/Blockchain/tmp/blockchain test/"

    # Effettuare il caricamento di ogni file sulla directory selezionata in precedenza
    try:
        for root, dirs, files in os.walk(temp_directory_path):

            for file in files:

                file_path = os.path.join(root, file)

                blob_path = os.path.join(folder_name, os.path.relpath(file_path, temp_directory_path))

                blob = bucket.blob(blob_path)

                blob.upload_from_filename(file_path)

        #print(f"All files in the temporary directory uploaded to the {folder_name} folder in {bucket_name}.")
    except Exception as e: 
        print(e)
                      
def delete_file(file_path = '/home/jupyter/Blockchain/tmp/blockchain test/blockchain.pickle'):
    os.remove(file_path)
    
def color(text, color):
    colors = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN
    }

    if color not in colors:
        raise ValueError(f'Il colore "{color}" non è supportato')

    return colors[color] + text + Style.RESET_ALL

class Transaction:
    def __init__(self, sender, recipient, amount, date = datetime.now().strftime('%d-%m-%Y')):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.date = date

    def __str__(self):
        return f"{self.sender} eroga prestito di {self.amount} EUR a {self.recipient}"

class Block:
    def __init__(self, index, prev_hash, timestamp, data, nonce=0):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.prev_hash).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.nonce).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self, genesis_data, difficulty=4):
        self.chain = [self.create_genesis_block(genesis_data)]
        self.difficulty = difficulty

    def create_genesis_block(self, genesis_data):
        return Block(0, "0", time.time(), genesis_data)

    def add_block(self, new_block):
        new_block.prev_hash = self.chain[-1].hash_block()
        new_block = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        while block.hash_block()[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
        return block

    def display_transactions(self):
        os.system('clear')
        print(color('Registro Blockchain Aggiornato: ','blue'))
        for block in self.chain:
            print(f"Block {block.index}: {block.data}, | hash: {block.hash_block()}")
    
    def display_transactions_2(self):
        os.system('clear')
        print(color('Registro Blockchain Aggiornato: ','blue'))
        for block in self.chain:
            transaction = block.data
            print('-'*70)
            print(color(f"Block {block.index}",'green'))
            #print(f"Data: {block.data}")
            print(f"Date: {transaction.date}")
            #print(f"Date: {block.timestamp}") tolto perchè dà proprio il ts e non la data
            print(f"Desc: {block.data}")
            print(f"Sender: {transaction.sender}")
            print(f"Receiver: {transaction.recipient}")
            print(f"Amount: {transaction.amount} EUR")
            print(f"Hash: {block.hash_block()}")
            
        else:
            print('-'*70)

    def add_transaction(self, transaction):
        new_block = Block(len(self.chain), "", time.time(), transaction)
        self.add_block(new_block)