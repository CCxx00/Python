import socket
import re
import multiprocessing

class tcp_server():
    def __init__(self):
        # create tcp socket
        self.tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # repeat to use same port
        self.tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # src_ip,src_port
        src_ip_port=("",4566)
        # tcp server bind ip and port
        self.tcp_socket.bind(src_ip_port)
        # make tcp socket become listen mode
        self.tcp_socket.listen(128)

    def listen_client(self):
        # wait client connecting,create new client socket that is communicated
        self.client_socket,self.client_addr=self.tcp_socket.accept()
        print(self.client_addr)

    def response(self):
        while True:
            # accept msg of client
            rfile_name=self.client_socket.recv(1024).decode("utf-8")
            if rfile_name=='':
                break
            # get file_name by re
            ret=re.search(r'/[^ ]*',rfile_name.split('\n')[0])
            file_name=None
            # if no ret,file_name is None
            if ret:
                file_name=ret.group()
            # print(file_name)

            # if no file,not send data
            if file_name:
                try:
                    if file_name=='/':
                        file_name='/index.html'
                    f=open('./html'+file_name,'rb')
                    response_body=f.read()
                    response_headers="HTTP/1.1 200 OK\r\nContent-Length:%d\r\n\r\n"%len(response_body)
                    # server send the requested html headers to client
                    self.client_socket.send(response_headers.encode("utf-8"))
                    # server send the requested html bodys to client
                    self.client_socket.send(response_body)
                    f.close()
                except Exception as ret:
                    response_headers="HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404"
                    self.client_socket.send(response_headers.encode("utf-8"))
                    # server send the requested data to client
                    # client_socket.send(response_body)
                    print("No file %s"%file_name)

        # close client socket
        self.client_socket.close()

    def close_tcp(self):
        # close tcp socket
        self.tcp_socket.close()

def main():
    server=tcp_server()
    while True:
        server.listen_client()
        p=multiprocessing.Process(target=server.response())
        p.start()
    server.close_tcp()

if __name__=="__main__":
    main()
