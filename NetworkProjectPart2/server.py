import socket
import time
import os
import ctypes

def check_connection(cs_user):
    data = cs_user.recv(1024).decode('utf-8').strip() #recieved data from the client 

    #print the student ID
    print(f"Received student ID: {data}\n")

    #check if it's a valid student ID which is one of our group memeber 
    if data == "1200031" or data == "1200183" :

        #send message to the client that the screen will be locked in 10 seconds
        cs_user.sendall("Server:Locking screen in 10 seconds\n".encode('utf-8'))

        #also print the message in the server that the screen will be locked in 10 seconds 
        print("Server: The operating system will lock screen after 10 seconds\n")

        #wait 10 seconds 
        time.sleep(10)

        #call the function to lock the screen 
        lock_screen()
        
    else:
        #display an error message that incorrent ID "not from the group"
        cs_user.sendall("Server: Error - Invalid student ID\n".encode('utf-8'))
        print("Server: Error - Invalid student ID")

    #close the connection of the server
    cs_user.close()

def lock_screen():

    print("Server: Locking the screen now")
    #function the check the operating system of the user if its windows or linux
    os_name = os.name #get the system type
    if os_name == 'posix':  #incase of linux and MAC 
        os.system("gnome-screensaver-command -l")  #lock the screen 
    elif os_name == 'nt':  #for windows
        ctypes.windll.user32.LockWorkStation() #lock the screen in windows command 
        

def main():
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #create a TCP socket  identifing AF_INET and SOCK_STREAM give us TCP socket

    server_s.bind(('localhost', 9955)) #bind the server to specified port which is 9955
    server_s.listen() #listen for any incomming connections 

    print("Server is listening on port 9955")

    while True:
        cs_user, client_IPaddress = server_s.accept() #accept an incoming connection

        #print once we get a connection
        print(f"Connection from {client_IPaddress}")

        #then check the connection 
        check_connection(cs_user)


main()
