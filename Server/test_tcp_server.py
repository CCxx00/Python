import socket

def main():
    # create tcp socket
    tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # src_ip,src_port
    src_ip_port=("",4566)
    # tcp server bind ip and port
    tcp_socket.bind(src_ip_port)
    # make tcp socket become listen mode
    tcp_socket.listen(128)
    # wait client connecting,create new client socket that is communicated
    client_socket,client_addr=tcp_socket.accept()
    print(client_addr)
    # accept msg of client
    file_name=client_socket.recv(1024).decode("utf-8")
    print(file_name)

    if file_name:
        try: # if no file,not send data
            f=open(file_name,'rb')
            client_socket.send(f.read()) # server send mag to client to express success communication
        except Exception as ret:
            print("No file %s"%file_name)

    # close client socket
    client_socket.close()
    # close tcp socket
    tcp_socket.close()

if __name__=="__main__":
    main()
