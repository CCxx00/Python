import socket

class tcp_server():
    def __init__(self):
        # create tcp socket
        self.tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # src_ip,src_port
        src_ip_port=("",4566)
        # tcp server bind ip and port
        self.tcp_socket.bind(src_ip_port)
        # make tcp socket become listen mode
        self.tcp_socket.listen(128)

    def response(self):
        # wait client connecting,create new client socket that is communicated
        client_socket,client_addr=self.tcp_socket.accept()
        print(client_addr)
        # accept msg of client
        file_name=client_socket.recv(1024).decode("utf-8")
        print(file_name)

        response_text="HTTP/1.1 200 OK\r\n\r\n"

        if file_name:
            try: # if no file,not send data
                f=open(file_name,'rb')
                response_text+=f.read()
                # server send the requested data to client
                client_socket.send(response_text.encode("utf-8"))
            except Exception as ret:
                print("No file %s"%file_name)

        # close client socket
        client_socket.close()

    def close_tcp(self):
        # close tcp socket
        self.tcp_socket.close()

def main():
    server=tcp_server()
    server.response()
    server.close_tcp()

if __name__=="__main__":
    main()
