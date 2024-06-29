# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 15:13:49 2024

@author: Cristina
"""


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import Tk, Toplevel, Label, Entry, CENTER
from tkinter import Scrollbar, Button, END, Listbox, StringVar
from tkinter import messagebox
import time as tm
import sys
class Client:

    def __init__(self):

        self.check = False
        
        
        self.Window = Tk()
        self.Window.withdraw()
        
        # Schermata di login
        self.login = Toplevel()
        
        # Imposto il titolo della schermata
        self.login.title("Login")
        #Gestisce la chiusura con la X della finestra di login 
        self.Window.protocol("WM_DELETE_WINDOW", self.on_closinglog)
        self.login.resizable(width=False,
                             height=False)
        self.login.geometry('400x250')

        self.login.configure(width=350,
                             height=200,
                             bg="#8CAEE6")
        self.labelhost = Label(self.login,
                         text="Inserisci Host",
                         justify=CENTER,
                         font="Arial 12",
                         bg='#8CAEE6',
                         fg='black')

        self.labelhost.place(relheight = 0.07, 
                       relx = 0.24, 
                       rely = 0.05)

        # Casella di testo dove l'utente inserirà Server host
        self.entryhost = Entry(self.login, font="Arial 11")

        self.entryhost.place(relx = 0.24,
                             rely = 0.15)

        # Imposto il focus sulla casella di testo
        self.entryhost.focus()
        
        self.labelporta = Label(self.login,
                         text="Inserisci porta",
                         justify=CENTER,
                         font="Arial 12",
                         bg='#8CAEE6',
                         fg='black')

        self.labelporta.place( 
                       relx = 0.24, 
                       rely = 0.25)

        # Casella di testo dove l'utente inserirà la porta
        self.entryporta = Entry(self.login, font="Arial 11")

        self.entryporta.place(relx = 0.24,
                             rely = 0.35)
        self.labelnome = Label(self.login,
                         text="Inserisci Nome",
                         justify=CENTER,
                         font="Arial 12",
                         bg='#8CAEE6',
                         fg='black')

        self.labelnome.place(relheight = 0.24, 
                       relx = 0.24, 
                       rely = 0.45)

        # Casella di testo dove l'utente inserirà il nome
        self.entryName = Entry(self.login, font="Arial 11")

        self.entryName.place(relx = 0.24,
                             rely = 0.60)

        # Creazione del bottone che invoca
        # la funzione connetti_accedi
        self.go = Button(self.login,
                         text="Accedi",
                         font="Helvetica 14 bold",
                         command=lambda: self.connetti_accedi(self.entryhost.get(),self.entryporta.get(),self.entryName.get()),
                         bg='#8CAEE6',
                         fg='#ffffff')

        self.go.place(relx = 0.38, 
                      rely = 0.75)
        
        
        
        
        self.entryName.bind("<Return>", self.on_invio)
        self.Window.mainloop()

    #Lego la funzione connetti_accedi al tasto invio 
    def on_invio(self,event):
            
        self.connetti_accedi(self.entryhost.get(),self.entryporta.get(),self.entryName.get())


    #Passaggio alla schermata successiva in caso di Server e nome inseriti non vuoti 
    def connetti_accedi(self,host,port, name):
        
        if host== "":
            messagebox.showerror("Errore","Obbligatorio inserire il Server host oppure localhost")
        if port=="":
            port=53000
        else:
            port=int(port)
        
        self.request_connection(host, port)
        # Se il nome non è vuoto invio il messaggio col nome al Server,chiudo
        #  la finestra di login e creo una nuova finestra
        if name != "":  
            self.client_socket.send(bytes(name, FORMAT))
            self.login.destroy()
            self.layout(name)
            
            # Faccio partire i thread per ascoltare i messaggi in entrata
            rcv = Thread(target=self.receive)
            rcv.start()
        else: 
            messagebox.showerror("Errore","Obbligatorio inserire il nome")
    # Funzione che connette il Client al Server        
    def request_connection(self,host, port):
    # Inizializza il socket del Client
        self.client_socket = socket(AF_INET, SOCK_STREAM)    
        
        try: 
        # Si connette al server
            self.client_socket.connect((host, port))
        except Exception as error:
            
            messagebox.showerror ("Impossibile stabilire la connessione\n" , Exception,":",error)
            sys.exit(0)

    

    
    # Creazione layout della schermata della chat
    def layout(self, name):

        self.name = name

        self.Window.deiconify()
        self.Window.title("Chat in compagnia")
        
        #Funzione da eseguire quando viene cliccata la x
        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.Window.resizable(width=False,
                              height=False)

        self.Window.configure(width=500,
                              height=600,
                              bg="white")

        self.labelHead = Label(self.Window,
                               bg="#8CAEE6",
                               fg="black",
                               text=self.name,
                               font="Arial 14",
                               pady=5)

        self.labelHead.place(relwidth=1)
        
        self.my_msg = StringVar()
        self.my_msg.set("")
        self.textList = Listbox(self.Window,
                             height=15, 
                             width=50,
                             bg="white",
                             fg="black",
                             font="Arial 11")

        self.textList.place(relheight=0.745,
                            relwidth=1,
                            rely=0.05)

        self.labelBottom = Label(self.Window,                                 
                                 bg="#8CAEE6",                                                                 
                                 height=40)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)
        self.labelText =Label(self.labelBottom,
                              text="Scrivi qui il tuo messaggio e premi Invia",
                              font="Arial 12",
                              bg="#8CAEE6",
                              fg="black",
                              height=10)
        
        self.labelText.place(relwidth=0.74,
                            relheight=0.04,
                            rely=0.010,
                            relx=0.011)
        
        
                               
        self.entryMsg = Entry(self.labelBottom,
                              textvariable=self.my_msg,
                              bg="white",
                              fg="black",
                              font="Arila 11")

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.05,
                            rely=0.045,
                            relx=0.011)

        self.entryMsg.focus()
        
        

        self.buttonMsg = Button(self.labelBottom,
                                text="Invia",
                                font="Helvetica 12 bold",
                                width=2,
                                bg='#8CAEE6',
                                command=lambda:self.send(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.05,
                             relwidth=0.20)

        self.buttonEsci = Button(self.labelBottom,
                                text="Esci",
                                font="Helvetica 12 bold",
                                width=2,
                                bg='#8CAEE6',
                                command=lambda:self.send("{quit}"))

        self.buttonEsci.place(relx=0.77,
                             rely=0.070,
                             relheight=0.05,
                             relwidth=0.20)


        self.textList.config(cursor="arrow")

        # Creo lo scrollbar verticale e orizzantale
        scrollbary = Scrollbar(self.textList)

        scrollbary.place(relheight=1,
                        relx=0.974)

        scrollbary.config(command=self.textList.yview)
        
        scrollbarx = Scrollbar(self.textList,orient="horizontal")
        scrollbarx.place(relwidth=1,
                        rely=0.974)
        
        
        scrollbarx.config(command=self.textList.xview)
        #Lego il tasto invio all'invio dei messaggi
        self.entryMsg.bind("<Return>", self.on_inviomsg)
    
    def on_inviomsg(self,event):
         self.send(self.entryMsg.get())

    # Invio messaggi al server 
    #Se il messaggio è {quit}chiudo il socket e la finestra chat
    # Se non e quit e non è vuoto invio il messaggio al server 
    #e imposto come vuota la casella di inserimento
    def send(self, msg):
        if msg=="{quit}":
            self.client_socket.send(bytes(msg, FORMAT))
            self.client_socket.close()
            self.Window.quit()
            self.Window.destroy()
        else:
            
            msg = self.my_msg.get()
            if msg == "": # Blocco invio di messaggi vuoti
                messagebox.showerror("Errore","Non è possibile inviare un messaggio vuoto")
                return
        
        
            self.client_socket.send(bytes(msg, FORMAT))
            self.my_msg.set("")
        
            
           
        
        
        

    #Ricezione dei messaggi 
    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode(FORMAT)
                
                # Inserisci i messaggi alla textbox
                self.textList.insert(END, msg + "\n\n")
           
            except OSError:
                
                break
    
    
    
    # Chiusura applicazione e del socket
    def close(self):
        self.client_socket.close()
        self.Window.quit()
        self.Window.destroy()
   
    # Chiusura con la x della finestra Chat    
    def on_closing(self, event=None):
        self.client_socket.send(bytes('{quit}', FORMAT))
        tm.sleep(1)
        
        self.close()
       
    # Chiusura con la x della finestra login    
    def on_closinglog(self, event=None):
         self.Window.quit()
         self.Window.destroy()    
    
        

BUFSIZ = 1024

FORMAT = "utf8"


# Lancio l'applicativo
c = Client()





