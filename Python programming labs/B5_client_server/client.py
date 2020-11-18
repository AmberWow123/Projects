# description: This client program shows a menu of setting new path, showing files, showing directories, and quit for the user to choose
#              then, this program will check if the input is valid or not, and then send the user input to server, and then it will receive the returned value from server
#              then this program will call the print function to print it out, and prompt the user again, until the user wants to quite

import socket
import pickle
import os

def prompt(currD) :
    ''' prompt the user to input the choice, ask for new path if the user wants to set new path, and return it '''
    while True :
        print("\ns. set path\nf. show files\nd. show dirs\nq. quit")
        choice = input("Enter choice: ")   
        if choice == "s" :
            newD = input("Enter new path starting from current directory: ")
            return choice + (os.path.join(currD, newD))
        if choice in "sfdq" and len(choice) == 1 :
            return choice + currD
        print("invalid input")

def printFunctS(value) :
    ''' print new path, or print invalid if the path is invalid '''
    if value == "n":
        print("invalid path")
    else :
        print("New path:" + value)
    
def printFunctF(value, currD, choice) :
    ''' print the files or directories under the current directory '''
    if value :
        print("Files" if choice == "f" else "Directories", "found under", currD)
        for ele in value :
            print(ele)
    else :
        print("No files under" if choice == "f" else "No directory under", currD)
        
def main() :
    ''' first send a request to server to print the current directory, prompt the user to choose what to do
        , send user input to server to get the returned value, if the user input q then end the loop, if the user input s, change the current directory if the returned value for choice s is valid
        when the server send back the returned value, call the print function'''
    HOST = '127.0.0.1'
    PORT = 5578
    
    with socket.socket() as s :
        s.connect((HOST, PORT))
        print("Client connect to:", HOST, "port:", PORT)
        s.send("c".encode("utf-8"))
        currD = s.recv(1024).decode('utf-8')    # current directory
        print("\nCurrent Directory:", currD)
        promptInput = prompt(currD)  
        s.send(promptInput.encode('utf-8'))

        while promptInput[0] != "q" :
            choiceL = promptInput[0]
            path = promptInput[1]  
            
            fromServerb = s.recv(1024)
            newObj = pickle.loads(fromServerb)
            
            if choiceL == "s" :
                if newObj != "n" :
                    currD = newObj   # change the current dir to new dir
                printFunctS(newObj)
            else :
                printFunctF(newObj, currD, choiceL)
            
            promptInput = prompt(currD)
            s.send(promptInput.encode('utf-8'))
main()
