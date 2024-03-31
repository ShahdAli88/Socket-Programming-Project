import socket


def main():
    cs_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a TCP socket using socket 

    #connect it to the server local host on port 9955 
    cs_user.connect(('localhost', 9955)) 

    #ask the client to enter the ID of student
    student_id = input("Please enter your ID .\n").strip() 

    cs_user.sendall(student_id.encode('utf-8')) 
    #send this data to the server and after encoding it using UTF-8 

    response= cs_user.recv(1024) 
    #recieved data from the server  
    if response:
        print("Received response :", response.decode('utf-8')) #print the response after decoding it 

    else:
        #if there was no response due to the user entering wrong ID 
        print ("There was no response got received from the server.\n")

    #close the client socket of the user
    cs_user.close()


main()