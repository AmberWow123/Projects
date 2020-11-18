# description: This server program will handle the request sent from client, 
#              and call the corresponding function of the input choice sent,
#              after it get the returned value from the corresponding function,
#              it sends the returned value back to client. 
#              The server program will use multithreading to interact with multiple clients, and the number typed in command line after the py file is the number of clients which multithreading will handle


import socket
import os
import pickle
import threading
import sys
import glob

def getCurrentDir() :
    ''' return the current directory '''
    return os.getcwd()

def changeCurrentDir(newD) :
    ''' return "n" if the path is invalid, return the changed current directory if valid'''
    if not os.path.isdir(newD) :
        return "n"
    else :
        os.chdir(newD)
        return os.getcwd()
    
def listAllFiles(currD) :
    ''' return a list of file names under the current directory '''
    return [ele.name    for ele in os.scandir(currD)    if ele.is_file()]
    #return glob.glob(os.path.join(currD, "*"))
    
def listAllDirs(currD) :
    ''' return a list of directories and subdirectories under the current directory '''
    return [os.path.join(path, d)    for (path, dirList, fileList) in os.walk(currD)    for d in dirList]

def interactUser(fctList, s) :
    ''' timeout if the clients are not connected within 10 seconds, receive the first data choice from client to send the current directory back,
        then keep receiving the choices from clients, and send the returned value back to client
        if the choice is s, then change the current directory, loop until the data choice is q, then quit'''
    try :
        s.settimeout(10)
        s.listen()
        (conn, addr) = s.accept()     # blocking
        requestFromClient = conn.recv(1024).decode("utf-8")
        conn.send(fctList[requestFromClient]().encode('utf-8'))
        print("sending", fctList[requestFromClient]())
        
        while True:
            fromClient = conn.recv(1024).decode('utf-8')                     
            choice = fromClient[0]
            path = fromClient[1:]
            
            if choice == 'q':
                break
            if choice == "s" :
                newPath = path
                b = pickle.dumps(fctList[choice](newPath))
            else :
                b = pickle.dumps(fctList[choice](path))
            conn.send(b)    
    except socket.timeout :
        print("timeout")
        
def main() :
    ''' show id of server and hostname, check if there is any command line error, if input on command line is valid then run the threads, starts to receive the data from clients'''
    request = {"c" : getCurrentDir, "s" : changeCurrentDir, "f" : listAllFiles, "d" : listAllDirs}
    HOST = "localhost"      
    PORT = 5578
    with socket.socket() as s :
        s.bind((HOST, PORT))
        if len(sys.argv) != 2 or not sys.argv[1].isdigit():
            print("Usage: server.py num_of_clients\n") 
        elif int(sys.argv[1]) >= 5 :
            print("The max number of clients < 5\n")         
        else :
            print("Server is up. hostname:", HOST, "port:", PORT)
            print(getCurrentDir())            
            threadsL = []
            for i in range(int(sys.argv[1])) :
                t = threading.Thread(target = interactUser, args = (request,s))
                threadsL.append(t)
            for t in threadsL:
                t.start()
            for t in threadsL :
                t.join()                
      
main()     
        