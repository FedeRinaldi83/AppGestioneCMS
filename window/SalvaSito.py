"""
Finestra salva paramtri connessione ftp a sito
Caricamento CMS su server
Autore : Federico Rinaldi
Web: http://www.federicorinaldi.com
Version : 1.0
"""

from Tkinter import *
import functions.GestioneProperties as properties
import ttk
import tkMessageBox
import os

class SalvaParametri(Frame):

    errors = 0
    textSito = None
    textHost = None
    textUser = None
    textPassword = None
    textPort = None

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("Connessione FTP")
        self.pack(fill=BOTH, expand=True)
        self.createWidget()


    def createWidget(self):
        datiConnessione = properties.GestioneProperties().leggiFile()

        labelSito = Label(self, text="Nome Sito")
        labelSito.grid(row=0, column=0, sticky=W,pady=5)

        self.textSito = Entry(self,width=28)
        self.textSito.insert(0,datiConnessione['nome'])
        self.textSito.grid(row=0,column=1,pady=5)

        labelHost = Label(self,text="Host")
        labelHost.grid(row=1,column=0,sticky=W,pady=5)

        self.textHost = Entry(self,width=28)
        self.textHost.insert(0,datiConnessione['host'])
        self.textHost.grid(row=1,column=1,pady=5)

        labelUser = Label(self,text="Username")
        labelUser.grid(row=2,column=0,sticky=W,pady=5)

        self.textUser = Entry(self,width=28)
        self.textUser.insert(0,datiConnessione['username'])
        self.textUser.grid(row=2,column=1,pady=5)

        labelPass = Label(self,text="Password")
        labelPass.grid(row=3,column=0,sticky=W,pady=5)

        self.textPassword = Entry(self,width=28,show="*")
        self.textPassword.insert(0,datiConnessione['password'])
        self.textPassword.grid(row=3,column=1,pady=5)

        labelPort = Label(self,text="Porta")
        labelPort.grid(row=4,column=0,sticky=W,pady=5)

        self.textPort = Entry(self,width=28)
        self.textPort.insert(0,datiConnessione['port'])
        self.textPort.grid(row=4,column=1,pady=5)

        pulsanteInserisci = Button(self,text="Salva",width=7,command=self.validainserisci)
        pulsanteInserisci.grid(row=5,column=0,sticky=W,pady=5,padx=5)



    def validainserisci(self):
        #tkMessageBox.showerror("Attenzione","Errore durante il salvataggio")
        errori = 0
        if len(self.textSito.get())== 0 :
            errori +=1
        if len(self.textPort.get())== 0 :
            errori +=1
        if len(self.textPassword.get())== 0 :
            errori +=1
        if len(self.textUser.get())== 0 :
            errori +=1
        if len(self.textHost.get())== 0:
            errori +=1

        if errori > 0 :
            tkMessageBox.showerror("Attenzione", "Errore durante il salvataggio\n Alcuni campi sono vuoti")
        else:
            datiConn = {"nome": self.textSito.get(),
                               "host": self.textHost.get(),
                               "username": self.textUser.get(),
                               "password": self.textPassword.get(),
                               "port": self.textPort.get()}
            classeScrittura = properties.GestioneProperties()
            scrittura = classeScrittura.scriviFile(datiConn)
            if scrittura == 0:
                tkMessageBox.showerror("Errore Salvataggio Dati","Errore durante il salvataggio dei dati connessione FTP")
            elif scrittura ==1:
                tkMessageBox.showinfo("Scrittura Completata","Il Salvataggio dei dati di connessione avvenuto correttamente")
            self.destroy

def main():
    root = Tk()
    #root.geometry("350x750+300+300")
    root.geometry("250x200")
    root.resizable(width=False, height=False)
    app = SalvaParametri(root)
    root.iconbitmap(os.path.join(os.path.dirname(__file__), '../', 'resources/ftp.ico'))
    app.pack_propagate(0)
    app.grid_propagate(0)
    root.mainloop()


if __name__ == '__main__':
    main()



