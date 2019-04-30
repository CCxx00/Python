import socket
import re
import select

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
        # create epoll
        self.epl=select.epoll()
        # make epoll listen tcp_socket
        self.epl.register(self.tcp_socket.fileno(),select.EPOLLIN)
        self.client_socket_dict=dict()

    def epoll_server(self):
        # default blocking,not blocking when recepted msg
        fd_list=self.epl.poll()
        for fd,event in fd_list:
            if fd==self.tcp_socket.fileno():
                # wait client connecting,create new client socket that is communicated
                self.client_socket,self.client_addr=self.tcp_socket.accept()
                print(self.client_addr)
                # make epoll listen client_socket
                self.epl.register(self.client_socket.fileno(),select.EPOLLIN)
                self.client_socket_dict[self.client_socket.fileno()]=self.client_socket
            else:
                # accept msg of client
                client_socket=self.client_socket_dict[fd]
                rfile_name=client_socket.recv(1024).decode("utf-8")
                if rfile_name=='':
                    # close client socket
                    client_socket.close()
                else:
                    self.response(rfile_name,client_socket)

    def response(self,rfile_name,client_socket):
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
                client_socket.send(response_headers.encode("utf-8"))
                # server send the requested html bodys to client
                client_socket.send(response_body)
                f.close()
            except Exception as ret:
                response_headers="HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404"
                client_socket.send(response_headers.encode("utf-8"))
                # server send the requested data to client
                # client_socket.send(response_body)
                print("No file %s"%file_name)

    def close_tcp(self):
        # close tcp socket
        self.tcp_socket.close()

def main():
    server=tcp_server()
    while True:
        server.epoll_server()
    server.close_tcp()

if __name__=="__main__":
    main()
