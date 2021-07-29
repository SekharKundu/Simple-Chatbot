import os
import tkinter
from tkinter import *
from tkinter import messagebox 
from tkinter import ttk
from tkinter.ttk import * 
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)	

base = Tk()
base.title("CHATBOT ~ A Simple Chat Bot")
base.geometry("800x500")
base.resizable(width=FALSE, height=FALSE)
base.iconbitmap(default=resource_path("icon.ico"))
def about():
        messagebox.showinfo(title="About", message= "This is a 6th Semester(CSE) Information Security Project Submitted by :\nShantanu Swargeary (GAU-C-17/062), CIT KOKRAJHAR")
        container.pack(side='top',expand = True)

menu = Menu(base)
base.config(menu=menu) 
filemenu = Menu(menu,tearoff=False)
menu.add_cascade(label='Option', menu=filemenu)
filemenu.add_command(label='About', command=about)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=base.destroy)

style = Style() 
style1 = Style()
style.configure('TButton', font =
               ('calibri', 20, 'bold'), 
                foreground = 'grey')
style1.configure('TEntry', font =
               ('Arial', 20))


ChatLog = Text(base ,bd=3, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = ttk.Button(base, text="Send", width="12" ,style = 'TButton')

#Create the box to enter message
EntryBox = ttk.Entry(base,style="TEntry")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=770,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=760)
EntryBox.place(x=6, y=401, height=90, width=580)
SendButton.place(x=590, y=401, height=90,width=200)

base.mainloop()
