#!/usr/bin/python
# -*- coding: utf-8 -*-


from Tkinter import *
from ttk import Frame, Button, Style
from socket import *
from multiprocessing import Process
import sys, socket, select










def loggingIn():
    print "loggingIn"
    
    global username, s
    
    host = entryA.get()
    try:
        port = int(entryB.get())
    except:
        errorText.set("Port needs to be a number")
        return
    
    username = entryC.get()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print "Unable to connect"
        errorText.set("Unable to connect")
        return
     
    print 'Connected to remote host. You can start sending messages'
    #Don't go to send, open new gui, then wait for such
    terminateLogin()
    
    
    p1 = Process(target = chat_GUI)
    p1.start()
    p2 = Process(target = listen)
    p2.start()
    
    

def terminateLogin():
    print 'about to destroy'
    rootL.destroy()
    
    
def listen():
    
    socket_list = [s]
     
    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
    
    for sock in read_sockets:            
        if sock == s:
            # incoming message from remote server, s
            data = sock.recv(4096)
            if not data:
                print '\nDisconnected from chat server'
                sys.exit()
            else :
                #print data
                sys.stdout.write(data)
                sys.stdout.write('[Me] '); sys.stdout.flush()     
            
        else :
            # user entered a message
            msg = sys.stdin.readline()
            s.send(msg)
            sys.stdout.write('[Me] '); sys.stdout.flush() 
    
    
    
    
    
    """
    if len(onlineUsers) == 0:
         
        Logged_On_List.append(usrname[:-1])
         
        List_Updater()
         
    try:
 
        rdata = sock.recv(2048)
 
        if rdata:
             
            print_(rdata)
             
            rootM.after(100, receive)
             
    except:
        rootM.after(100, receive)
    """
    
    
    

def send():
    print "send"
    
        
    



#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------


def chat_GUI():
    global rootC, entry, userList, statusBar, displayText, users, status
    
    rootC = Tk()
    
    rootC.title("Babble")
    rootC.style = Style()
    rootC.style.theme_use("alt")
    w = 500
    h = 350
    rootC.geometry("%dx%d+50+25" % (w, h))
    
    bottomFrame = Frame(rootC)
    bottomFrame.pack(side = BOTTOM, fill = X)
    
    Button(bottomFrame, text = "Send", command=send).pack(side = RIGHT, fill=Y)
    entry = Text(bottomFrame, height=2, spacing1=2, spacing2=2, spacing3=2, wrap=WORD)
    entry.pack(fill=X)
    entry.focus()
    entry.bind("<Return>", (lambda event: send()))
    
    users = StringVar()
    users.set("Babble Test\nChatting Room")
    userList = Label(rootC, relief=GROOVE, textvariable=users)
    userList.pack(side=LEFT, fill=Y)
    
    status = StringVar()
    status.set("Connected and chatting as " + username)
    statusBar = Label(rootC, textvariable=status)
    statusBar.pack(side=TOP, fill=X)
    
    displayScrollbar = Scrollbar(rootC)
    displayText = Text(rootC, relief = SUNKEN, wrap=WORD)
    displayScrollbar.config(command = displayText.yview)
    displayText.config(yscrollcommand = displayScrollbar.set)
    displayScrollbar.pack(side = RIGHT, fill = Y)
    displayText.pack(side = BOTTOM, fill=BOTH)
    
    
    
    rootC.mainloop()

#---------------------------------------------------------------------------------------------------------

def login_GUI():
    global rootL, entryA, entryB, entryC, errorText, errors, loginButton
    
    rootL = Tk()
                                                            #Base
    rootL.title("Babble Login")
    rootL.style = Style()
    rootL.style.theme_use("alt")
    w = 250
    h = 150
    rootL.geometry("%dx%d+50+25" % (w, h))
                                                            #Base
    rowBuffer = Frame(rootL)                    
    labelBuffer = Label(rowBuffer, text=" ")    #Buffer @ top of App
    labelBuffer.pack()
    rowBuffer.pack(side = TOP, fill = X)        
                                                            #Host/Ip/Username
    rowA = Frame(rootL)
    labelA = Label(rowA, width = 10, text="IP:")
    entryA = Entry(rowA, width = 15)
    rowA.pack(side = TOP, fill = X)
    labelA.pack(side = LEFT)
    entryA.pack(side = LEFT, expand=NO)
    
    rowB = Frame(rootL)
    labelB = Label(rowB, width = 10, text="Port:")
    entryB = Entry(rowB, width = 15)
    rowB.pack(side = TOP, fill = X)
    labelB.pack(side = LEFT)
    entryB.pack(side = LEFT, expand=NO)
    
    rowC = Frame(rootL)
    labelC = Label(rowC, width = 10, text="Username:")
    entryC = Entry(rowC, width = 15)
    rowC.pack(side = TOP, fill = X)
    labelC.pack(side = LEFT)
    entryC.pack(side = LEFT, expand=NO)                                                        
                                                            #Host/Ip/Username
                                                            #Login Button/Errors
    errorText = StringVar()
    errorText.set("")
    errors = Label(rootL, textvariable=errorText)
    errors.pack(side=BOTTOM) 
    loginButton = Button(rootL, text = "Login", command = (lambda: loggingIn()))
    loginButton.pack(side = TOP)
                                                            #Login Button/Errors
    
    
    rootL.mainloop()

#---------------------------------------------------------------------------------------------------------


def main():
    
    login_GUI()
    #chat_GUI()

#---------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()  
