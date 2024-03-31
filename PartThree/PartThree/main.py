from socket import *
serverPort = 9966  #port 9966
serverSocket = socket(AF_INET, SOCK_STREAM)  # create tcp welcoming socket for server
serverSocket.bind(('', serverPort))  #binding the socket to give it address
serverSocket.listen(1)  #server begins listening for incoming tcp request
print('Welcome to our project\n')
print('Done by Shahd,Dana')

# respond to request
# can be of type css,html,jpg,npg
def respond_to_request(requestType, addr):
    #respond_to_request("main_en.html", addr)
    try:

        file = open(requestType, "rb")  # open the file in binary format for reading,  rb = binary
        #eg   file= open("main_en.html", "rb") #opening the file
    except (IOError, FileNotFoundError):  # if File Not Found, open error page
        print('Exception: file not found I/O exception')
        Error_not_found(addr) #send response 404, and open error page
    else:
        # if the file is found
        #"main_en.html"
        dot = requestType.index('.')
        # "main_en.html"
        # take the string after the dot, here for example the result is html
        extension = requestType[dot + 1:]
        ###################create response message
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())  #succesful,header 200: ok
        print("HTTP/1.1 200 OK")
        # send the requested file with the related Content-Type.
        if extension == "html":
            connectionSocket.send("Content-Type: text/html \r\n".encode())

        elif extension == "css":
            connectionSocket.send("Content-Type: text/css \r\n".encode())

        elif extension == "jpg":
             connectionSocket.send("Content-Type: image/jpg \r\n".encode())

        elif extension == "png":
            connectionSocket.send("Content-Type: image/png \r\n".encode())
#########################################create the end of response message
        connectionSocket.send("\r\n".encode())# indicate the end of the message
        result = file.read()  # read the file
        connectionSocket.send(result)  # send requested file

# open error page when called
def Error_not_found(addr):
    #create responde messsage
    connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())  #header 404: error
    print("HTTP/1.1 404 Not Found")
    #The file to send is html file type
    connectionSocket.send("Content-Type: text/html \r\n".encode())
    connectionSocket.send("\r\n".encode())  # end header


    f = open("error.html", "rb") #opening the file ,'rb'  mode  = binary format , to read without needing to encode
    connectionSocket.send(f.read()) #sending the file content
    # print The IP and port number of the client
    connectionSocket.send(f"<br><br> <b> <font size=+4> <center> IP: {addr[0]} <br> port: {addr[1]}<br> </b> </center></font>" .encode())
    connectionSocket.send("</body> </html>".encode())


# This function deals with the 307 response (redirect)
def redirect  (requestType,addr):

    extension = requestType #the string name of the file(go,so,bzu)
    # create response message
    # header 404: Temporary Redirect
    connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
    print("HTTP/1.1 307 Temporary Redirect")
    # because we eill redirect to another page, so basically we need the url location
    connectionSocket.send("Content-location: <url>\r\n".encode())
##################################
    if extension  == "cr": #if the extension on the request is (go), go to google.com
        connectionSocket.send("location: https://www.cornell.edu/ \r\n".encode())
        connectionSocket.send("\r\n".encode())


    if extension  == "so": #if the extension on the request is (so), go to stackoverflow website
        connectionSocket.send("location: https://stackoverflow.com/ \r\n".encode())
        connectionSocket.send("\r\n".encode())


    if extension  == "rt": #if the extension on the request is (bzu), go to Birzeit University website
        connectionSocket.send("location: https://ritaj.birzeit.edu/ \r\n".encode())
        connectionSocket.send("\r\n".encode())




while True:  #loop forever
    # set up TCP connection----> connection oriented
    print("--connection set up")
    connectionSocket, addr = serverSocket.accept() #server waits on accept() for incoming requests,new socket created on return
    sentence = connectionSocket.recv(1024).decode()  #read bytes from socket
    print(addr)
    print(sentence) #prints the response received

    # find the request type from request message
    header = sentence.split('\n') # split the request message at newline character
    type_Slash = header[0].split()[1]  # extract the type from the header, header[0] = eg. GET /ar HTTP/1.1
    #header[0].split()[1] = eg. ar

    # print(header)
    #print('type_Slash is '+ type_Slash)

    type = type_Slash.lstrip('/')  # remove the (/) from the left of the string
    print("You are working on : " +type)
####################################################
    if type.lower() == "en":  # if the requested type is "en", the page to send is the main_en.html
        respond_to_request("main_en.html", addr) # page to open + address
    elif type.lower() == "":  # if the request is not followed by anything, the page to send is the main_en.html
        respond_to_request("main_en.html", addr)
    elif type.lower() == "ar": # if the requested type is "ar", open the arabic version (main_ar.html) is sent
        respond_to_request("main_ar.html", addr)
    elif type.lower() == "index.html":  # if the requested type is "index.html", open the arabic version (main_en.html) is sent
        respond_to_request("main_en.html", addr)
 ####################################################
    elif type.lower().__contains__(".png"):  # if the request is a .png file then  we should  send the png image
        respond_to_request(type, addr)
    elif type.lower().__contains__(".jpg"):  # if the request is a .png file then  we should  send the jpg image
        respond_to_request(type, addr)
    elif type.lower().__contains__(".css"):  # if the request is a .css file then the we should send the requested css file
        respond_to_request(type, addr)
    elif type.lower().__contains__(".html"):  # if the request is contains  ".html" at the end, then the we should send the requested html file
        respond_to_request(type, addr)
 ####################################################
        #the status code 307 Temporary Redirect to redirect the following
    elif type.lower() == "cr": #If the request is /go then redirect to google website
        redirect (type,addr)
    elif type.lower() == "so": # If the request is /so then redirect to stackoverflow.com website
        redirect (type,addr)
    elif type.lower() == "rt": # If the request is /bzu then redirect to birzeit university website
        redirect (type,addr)

####################################################

    else:  # if the request is not valid, for example requesting a non-existent page or image, open error page
        Error_not_found(addr)

#####################################################
    connectionSocket.close()  #close connection to this client but not welcoming socket, terminating and closing the TCP connection

