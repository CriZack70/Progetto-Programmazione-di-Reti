# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 21:51:13 2024

@author: Cristina
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# La funzione che accetta le connessioni  dei client in entrata.
## Usa un try-except per catturare e gestire eventuali eccezioni in fase di connessione
def accetta_connessioni_in_entrata():
    while True:
        try:
            
            client, client_address = SERVER.accept()
            print("%s:%s si è collegato." % client_address)
        
            # ci serviamo di un dizionario per registrare i client
            indirizzi[client] = client_address
            #diamo inizio all'attività del Thread - uno per ciascun client
            Thread(target=gestice_client, args=(client,)).start()
        except Exception as e:
            print(f"Errore di connessione: {e}")
        

#La funzione  gestisce la connessione di un singolo client e
# ne gestisce i messaggi in un ciclo infinito.
def gestice_client(client):  # Prende il socket del client come argomento della funzione.
    try:
        #riceve il nome dal client
        nome = client.recv(BUFSIZ).decode("utf8")
        #da il benvenuto al client e gli indica come fare per uscire dalla chat
        benvenuto = "Benvenuto/a  %s ! Per uscire premi Esci " % nome
        #invia il messaggio di benvenuto al client
        client.send(bytes(benvenuto , "utf8"))
    
        msg = "%s si è unito all chat!" % nome
        #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
        broadcast(bytes(msg, "utf8"))
        #aggiorna il dizionario clients creato all'inizio
        clients[client] = nome
    
    #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, nome+": ")
            else:
                
               nom=clients[client]
               adr=indirizzi[client]
               client.close()
               print("%s:%s si è scollegato." % adr)

               del clients[client]
               # Se ci sono altri client ancora attivi invia loro il messaggio
               if len(clients)==0:
                   print("Nessuno presente in chat")
                   break
               if len(clients)>= 1:

                   broadcast(bytes("%s ha abbandonato la Chat." % nom, "utf8"))      

                   break
    except Exception as e:
        print(f"Errore nella gestione del client: {e}")
        client.close()
        if client in clients:
            del clients[client]
            broadcast(bytes("%s ha abbandonato la chat!" % clients[client], "utf8"))
            print(indirizzi[client], " si è scollegato.")
        
            

# La funzione invia un messaggio in broadcast a tutti i client.
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso, "utf8")+msg)

        
clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)
# Creazione del socket del server
SERVER = socket(AF_INET, SOCK_STREAM)
#Associa il socket all' indirizzo IP e alla porta specificati dal Client
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(4)
    print("In attesa di connessioni...")
    #Thread che accetta le connessioni in entrata
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    #inizializzo il thread
    ACCEPT_THREAD.start()
    #Faccio in modo che lo script principale attenda il
    #completamento e non salti alla riga successiva
    ACCEPT_THREAD.join()
    #chiudo il server
    SERVER.close()
