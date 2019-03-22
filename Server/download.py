import socket

def main():
    tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # create tcp socket
    des_ip_port=("192.168.1.102",4566) # set destination ip and port
    tcp_socket.connect(des_ip_port) # connect des_ip_port

    document=input("document_name:")
    tcp_socket.send(document.encode("utf-8"))

    recv_document=tcp_socket.recv(1024*1024*1024) # accept document which maxsize are 1G
    if(recv_document):
        with open(document,"wb") as f: # make document write to disk
            f.write(recv_document)

if __name__=="__main__":
    main()
