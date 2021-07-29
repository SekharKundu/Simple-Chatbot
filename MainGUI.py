import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

import tensorflow as tf
from tensorflow import keras
model = keras.models.load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


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

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Chatbot: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

base = Tk()
base.title("CHATBOT ~ Simple chat bot")
base.geometry("800x500")
base.resizable(width=FALSE, height=FALSE)
base.iconbitmap(default=resource_path("icon.ico"))

def about():
        messagebox.showinfo(title="About", message= "This is a summer project made by Shantanu Swargeary(GAU-C-17/062) and Sekhar Kundu(GAU-C-17/067), CIT KOKRAJHAR")
        container.pack(side='top',expand = True)

menu = Menu(base)
base.config(menu=menu) 
filemenu = Menu(menu,tearoff=False)
menu.add_cascade(label='Option', menu=filemenu)
filemenu.add_command(label='About', command=about)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=base.destroy)

style = Style() 
style.configure('TButton', font =
               ('calibri', 20, 'bold'), 
                foreground = 'grey')


ChatLog = Text(base ,bd=3, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = ttk.Button(base, text="Send", width="12" ,style = 'TButton',command=send)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)

scrollbar.place(x=770,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=770)
EntryBox.place(x=6, y=401, height=90, width=580)
SendButton.place(x=590, y=401, height=90,width=200)

base.mainloop()
