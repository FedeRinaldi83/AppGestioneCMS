"""
Finestra di informazioni sullo scaricamento dei CMS da internet
Caricamento CMS su server
Autore : Federico Rinaldi
Web: http://www.federicorinaldi.com
Version : 1.0
"""

from Tkinter import *
import os
import ttk
import urllib2
import time
import sys
import functions.GestioneProperties as GestProp




class DownloadCms(Frame):

    qualeStoScaricando = None
    urlDaScaricare = None
    barraDiScaricamento = None
    labelScaricamento = None

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("Aggiornamento CMS")
        self.pack(fill=BOTH, expand=True)
        self.createWidget()


    def createWidget(self):
        labelTitolo = Label(self, text="Sto Scaricando il CMS")
        labelTitolo.grid(row=0, column=0, pady=5, padx=13)

        self.labelScaricamento = Label(self,text=self.qualeStoScaricando)
        self.labelScaricamento.grid(row=3,column=0)

        self.barraDiScaricamento = ttk.Progressbar(self,orient=HORIZONTAL,length=250)
        self.barraDiScaricamento.grid(row=4,column=0)

        pulsantScarica = Button(self,text="Scarica!",width=15,command=self.scaricaDaSito)
        pulsantScarica.grid(row=5,column=0,pady=5)

    def scaricaDaSito(self):
        gestioneProp = GestProp.GestioneProperties()
        sitiDaScaricare = gestioneProp.leggiCmsDaScaricare()
        for key,sito in sitiDaScaricare.items():
            sitoDaLavorare,url = sito.split('=')
            self.qualeStoScaricando = sitoDaLavorare
            self.urlDaScaricare = url
            self.eseguiDownload(sitoDaLavorare,url)


    def eseguiDownload(self,sito,url):
        dataOraOdierna = time.strftime("%d-%m-%Y-%H-%M-%S")
        nomeFileScaricato = sito+".zip"
        pathFileLocale = os.path.join(os.path.dirname(__file__), '../', 'binaries/'+nomeFileScaricato)
        u = urllib2.urlopen(url)
        meta = u.info()
        file_size = int(meta.getheaders('Content-Length')[0])

        # save downloaded file to TEMP directory
        f = open(os.path.join(os.environ['TEMP'], pathFileLocale), 'wb')

        downloaded_bytes = 0
        block_size = 1024 * 8
        while True:
            buffer = u.read(block_size)
            if not buffer:
                break

            f.write(buffer)
            downloaded_bytes += block_size
            self.labelScaricamento['text']=" "
            self.labelScaricamento.update_idletasks()
            self.labelScaricamento['text'] = self.qualeStoScaricando
            self.barraDiScaricamento['maximum'] = file_size
            self.barraDiScaricamento['value'] = downloaded_bytes
            self.barraDiScaricamento.update_idletasks()
            self.labelScaricamento.update_idletasks()



        f.close()
        self.labelScaricamento['text']="Completato!"
        self.labelScaricamento.update_idletasks()

    def report(count, blockSize, totalSize):
        print count + " "+blockSize+" "+totalSize
        percent = int(count * blockSize * 100 / totalSize)
        sys.stdout.write("\r%d%%" % percent + ' complete')
        sys.stdout.flush()

def main():
    root = Tk()
    # root.geometry("350x750+300+300")
    root.geometry("250x200")
    root.resizable(width=False, height=False)
    app = DownloadCms(root)
    root.iconbitmap(os.path.join(os.path.dirname(__file__), '../', 'resources/download.ico'))
    app.pack_propagate(0)
    app.grid_propagate(0)
    root.mainloop()

if __name__ == '__main__':
    main()