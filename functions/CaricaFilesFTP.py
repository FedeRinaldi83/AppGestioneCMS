"""
Gestione del caricamento del/dei files su server
Caricamento CMS su server
Autore : Federico Rinaldi
Web: http://www.federicorinaldi.com
Version : 1.0
"""
from ftplib import FTP
import ftplib
import GestioneProperties as Prop
import zipfile
import os

import tkMessageBox

class CaricaFtp():

    progressBar = None
    maxLength = None
    labelStato = None

    def __init__(self,barra,label):
        self.progressBar = barra
        self.labelStato = label

    def unzipAndUpload(self,cmsDaCaricare,come):
        properties = Prop.GestioneProperties()
        datiConnessioneFtp = properties.leggiFile()

        if come == "unzip":
            tempDir = os.path.join(os.path.dirname(__file__), '../', 'binaries/temp')
            zipLocation = os.path.join(os.path.dirname(__file__), '../', 'binaries/')
            if not os.path.exists(tempDir):
                os.makedirs(tempDir)
            try:
                #self.deleteDir(tempDir)
                zipFile = zipfile.ZipFile(zipLocation+cmsDaCaricare+".zip",'r')
                zipFile.extractall(tempDir)
                zipFile.close()
            except zipfile.BadZipfile:
                tkMessageBox.showerror("Errore di compressione", "Errore durante l'unzip del file di cms")


            try:
                ftp = FTP(datiConnessioneFtp['host'])
                ftp.login(datiConnessioneFtp['username'], datiConnessioneFtp['password'])
            except ftplib.error_perm:
                tkMessageBox.showerror("Errore FTP","Errore durante la fase di login al server ftp")
                ftp.close()

            except ftplib.all_errors:
                tkMessageBox.showerror("Errore FTP", "Errore di connessione al server ftp")
                ftp.close()

            try:
                self.labelStato.config(text="")
                self.labelStato.update_idletasks()
                self.labelStato['text'] = "Sto caricando i files su server FTP..."
                self.labelStato.update_idletasks()
                self.uploadThis(tempDir,ftp)
            except ftplib.all_errors:
                tkMessageBox.showerror("Errore FTP","Errore durante il caricamento dei file sul server")
                ftp.close()
            except os.error:
                tkMessageBox.showerror("Errore di sistema", "Errore durante la lettura o creazione di cartelle")
                ftp.close()
            finally:
                ftp.close()


    #SISTEMARE BARRA PROGRESS e GESTIRE CODA FALLITA e RETRY
    def uploadThis(self,tempDir,ftp):
        files = os.listdir(tempDir)
        self.maxLength = os.path.getsize(tempDir)
        #self.maxLength = self.getSize(tempDir)
        os.chdir(tempDir)
        for f in files:
            if os.path.isfile(tempDir + r'\{}'.format(f)):
                fh = open(f, 'rb')
                #ftp.sendcmd("TYPE I")
                ftp.storbinary('STOR %s' % f, fh,1024,self.aggiornaBarra)
                fh.close()
            elif os.path.isdir(tempDir + r'\{}'.format(f)):
                ftp.mkd(f)
                ftp.cwd(f)
                self.uploadThis(tempDir + r'\{}'.format(f),ftp)
        ftp.cwd('..')
        os.chdir('..')


    def aggiornaBarra(self,block):
        sizeWritten = len(block)
        self.progressBar['maximum'] = self.maxLength
        self.progressBar['value'] = sizeWritten
        self.progressBar.update_idletasks()

