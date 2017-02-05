"""
Finestra principale Applicazione
Caricamento CMS su server
Autore : Federico Rinaldi
Web: http://www.federicorinaldi.com
Version : 1.0
"""
import os

from Tkinter import *
import ttk
import window.SalvaSito as salvaSito
import window.ScaricaCMS as GestCms
import functions.CaricaFilesFTP as FTPUp
import tkMessageBox

class Main(Frame):

    listaCms = None
    labelStato = None
    barra = None
    caricasito = None

    def __init__(self,parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("App Caricamento CMS")
        self.pack(fill=BOTH,expand=True)
        self.parent.config(menu=self.createMenuFile)
        self.createWidget()


    def createWidget(self):
        labelSceltaCms = Label(self,text="Scegli il CMS da caricare")
        labelSceltaCms.grid(row=0,column=0,sticky=NW,pady=5)
        #labelSceltaCms.pack(side=LEFT, anchor=N, padx=5, pady=5)


        self.listaCms = ttk.Combobox(self)
        self.trovaCMS()
        #listaCms.pack(side=RIGHT,anchor=N,padx=5, pady=5)
        self.listaCms.grid(row=0,column=1,sticky=NE,pady=5)

        labelradio = Label(self,text="Scegli come vuoi caricare il CMS su server")
        labelradio.grid(row=2,column=0,columnspan=2,sticky=W,pady=5)
        var = IntVar()
        var.set(1)
        scompatta = Radiobutton(self,text="Scompatta",variable=var,value=1)
        #scompatta.pack(side=LEFT,anchor=N,padx=25,pady=5)
        scompatta.grid(row=3,column=0,sticky=W,pady=5)
        caricasingolo = Radiobutton(self,text="Carica file zip",variable=var,value=2)
        #caricasingolo.pack(side=RIGHT,anchor=N,padx=30,pady=5)
        caricasingolo.grid(row=3,column=0,columnspan=2,pady=5)

        separatore = ttk.Separator(self,orient=HORIZONTAL)
        separatore.grid(row=4,column=0,columnspan=2,sticky=W,pady=5)

        self.caricasito = Button(self,text="Carica Sito",width=15,command=lambda:self.validaECarica(self.listaCms.get(),var))
        self.caricasito.grid(row=5,column=1,columnspan=1,sticky=E,pady=5)

        self.barra = ttk.Progressbar(self,orient=HORIZONTAL,length=355,value=0)
        self.barra.grid(row=7,column=0,columnspan=2,sticky=W,pady=5)

        #pulsanteRefresh = Button(self,text="Ricarica la lista dei CMS",command=self.trovaCMS)
        #pulsanteRefresh.grid(row=8,column=0,columnspan=1,sticky=W,pady=5,padx=5)
        self.labelStato = Label(self)
        self.labelStato.grid(row=8,column=0,columnspan=1,sticky=W,pady=5,padx=5)

    def validaECarica(self,cms,radio):
            if cms == "Seleziona un CMS":
                tkMessageBox.showerror("Errore","Scegliere un CMS dalla Lista")
                return
            elif cms == "Non sono presenti elementi nella lista":
                tkMessageBox.showerror("Errore", "Caricare la lista dei cms prima di eseguire l'upload su server")
                return

            comeUnzippare = None
            if radio.get() == 1:
                comeUnzippare = "unzip"
            else:
                comeUnzippare="zip"

            ftp = FTPUp.CaricaFtp(self.barra,self.labelStato)
            self.labelStato['text'] = "Sto unzippando il file " + cms + ".zip"
            self.caricasito['state'] = "disabled"
            self.caricasito.update_idletasks()
            self.labelStato.update_idletasks()
            ftp.unzipAndUpload(cms,comeUnzippare)
            self.labelStato['text'] = ""
            self.labelStato.update_idletasks()
            self.caricasito['state']="normal"
            self.caricasito.update_idletasks()

    def trovaCMS(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'binaries/'))
        files = []
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                nomeSito,archivio = name.split(".")
                files.append(nomeSito)
        if len(files) <= 0:
            files.append("Non sono presenti elementi nella lista")
        else :
            files.insert(0,"Seleziona un CMS")

        self.listaCms['values'] = files
        self.listaCms.current(0)


    def centerWindow(self):
        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    @property
    def createMenuFile(self):
        gestioneScaricamento = GestCms.main
        menubar = Menu(self)
        #imgExit = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'resources/exit.ico'))
        fileMenu = Menu(menubar,tearoff=0)
        fileMenu.add_command(label="Exit",command=self.parent.destroy)
        settingmenuitem = Menu(menubar, tearoff=0)
        settingmenuitem.add_command(label="Opzioni", command=self.apriOpzioni)
        settingmenuitem.add_command(label="Scarica CMS Aggiornati",command=gestioneScaricamento)
        menubar.add_cascade(label="File",menu=fileMenu)
        menubar.add_cascade(label="Impostazioni",menu=settingmenuitem)
        menubar.add_cascade(label="Aggiorna lista CMS",command=self.trovaCMS)

        return menubar

    def apriOpzioni(self):
        salvaSito.main()



def main():
    root = Tk()
    #root.geometry("350x750+300+300")
    root.geometry("360x400")
    root.resizable(width=False, height=False)
    root.iconbitmap(os.path.join(os.path.dirname(__file__), '', 'resources/upload.ico'))
    app = Main(root)
    app.pack_propagate(0)
    app.grid_propagate(0)
    root.mainloop()


if __name__ == '__main__':
    main()

