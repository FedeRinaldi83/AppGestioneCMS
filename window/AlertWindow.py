"""
Finestra di alert
Caricamento CMS su server
Autore : Federico Rinaldi
Web: http://www.federicorinaldi.com
Version : 1.0
"""
from Tkinter import *
import os

class AlertWindow(Frame):

    messaggio = ""

    def __init__(self,parent,message):
        #super(AlertWindow, self).__init__()
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("ATTENZIONE")
        self.pack(fill=BOTH, expand=True)
        self.createWidget(message)
        print message
        self.messaggio = message

    def createWidget(self,message):

        labelTitolo = Label(self, text="Attenzione si e' verificato un problema")
        labelTitolo.grid(row=0, column=0, pady=5,padx=13)

        labelMessaggio =  Label(self, text=message)
        labelMessaggio.grid(row=3,column=0)



def main(message):
    root = Tk()
    # root.geometry("350x750+300+300")
    root.geometry("250x150")
    root.resizable(width=False, height=False)
    app = AlertWindow(root,message)
    app.pack_propagate(0)
    app.grid_propagate(0)
    root.mainloop()

if __name__ == '__main__':
    main()
