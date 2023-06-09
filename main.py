from main import *

if __name__ == "__main__":
    
    if os.path.exists('/home/jupyter/Blockchain/tmp/blockchain test/blockchain.pickle'):
        delete_file()
    else:
        pass
    
    os.system('clear')

    # download del registro da Gcloud Bucket
    download_file()
    
    # Carica la blockchain da file, se esiste
    loaded_blockchain = load_blockchain()

    if loaded_blockchain:
        blockchain = loaded_blockchain
    else:
        print(color('Nessun registro presente, creo blocco origine. ', 'blue'))
        # Crea una nuova blockchain se non ne esiste una salvata
        genesis_transaction = Transaction("Banco_BPM", "Mario_Rossi", 5000)
        blockchain = Blockchain(genesis_transaction)
        save_blockchain(blockchain)
        upload_file()
    
    print(color('Blockchain Demo\n','blue'))
    ask = input("Cosa vuoi fare? \n(1) Visualizza la blockchain\n(2) Inserisci una nuova transazione\n")

    if ask == '1':
        #visualizza transazioni
        blockchain.display_transactions_2()
        delete_file()
        raise SystemExit(0)
    elif ask == '2':
        pass
    else:
        print('input non valido')
        delete_file()
        raise SystemExit(0)

    # Aggiungi nuove transazioni e salva la blockchain
    while True:
        os.system('clear')
        t = input(color("Inserisci mittente, destinatario e importo separati da spazi (es. BPM Mario_Rossi 1000): ",'blue'))
        #ottieni i dati della transazione
        sender, recipient, amount = t.split()
        print('Inserendo transazione: ', sender, recipient, amount)
        t = Transaction(sender, recipient, amount)
        blockchain.add_transaction(t)
        save_blockchain(blockchain)
        os.system('cls')
        print('List of all the blockchain blocks: ')
        blockchain.display_transactions_2()
        ask = input("vuoi inserire un'altra transazione? (y/n)")
        if ask == 'n' or ask == 'N':
            upload_file()
            delete_file()
            break
        elif ask == 'y' or ask == 'Y':
            pass
        else:
            print('input non valido')
            upload_file()
            delete_file()
            raise SystemExit(0)

    # Visualizza le transazioni
    #blockchain.display_transactions()

'''
L'hash di un blocco è una rappresentazione crittografica del contenuto del blocco stesso. Viene utilizzato per garantire l'integrità e l'immutabilità dei dati all'interno della blockchain. Nella nostra implementazione, l'hash di un blocco è generato utilizzando la funzione hash_block nella classe Block, che calcola l'hash SHA-256 dei dati del blocco.

Un hash di blocco è composto dai seguenti elementi:

Indice del blocco (index): un numero intero che rappresenta la posizione del blocco nella blockchain.
Hash del blocco precedente (prev_hash): l'hash del blocco precedente nella blockchain, che crea un legame tra i blocchi e garantisce l'integrità della catena.
Timestamp (timestamp): il timestamp di quando è stato creato il blocco.
Dati del blocco (data): il contenuto del blocco, che può includere transazioni, informazioni del contratto o qualsiasi altro dato.
Nonce (nonce): un numero intero arbitrario che viene utilizzato nell'algoritmo di Proof of Work (PoW) per trovare un hash che soddisfi un determinato requisito di difficoltà.
L'hash di un blocco è una stringa alfanumerica di lunghezza fissa (64 caratteri per l'hash SHA-256) che sembra casuale. Tuttavia, ogni modifica, anche minima, ai dati del blocco genera un hash completamente diverso.
'''