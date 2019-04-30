import socket
import re
import threading

class WSGIServer():
    def __init__(self,port):
        # create tcp socket
        self.tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # repeat to use same port
        self.tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # src_ip,src_port
        src_ip_port=("",port)
        # tcp server bind ip and port
        self.tcp_socket.bind(src_ip_port)
        # make tcp socket become listen mode
        self.tcp_socket.listen(128)

    def listen_client(self):
        # wait client connecting,create new client socket that is communicated
        client_socket,client_addr=self.tcp_socket.accept()
        print(client_addr)
        return client_socket

    def response(self,client_socket):
        while True:
            # accept msg of client
            rfile_name=client_socket.recv(1024).decode("utf-8")
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
                    # send Content-Length to browser for setting long-clink
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

        # close client socket
        client_socket.close()

    def close_tcp(self):
        # close tcp socket
        self.tcp_socket.close()

    def run_server(self):
        while True:
            p=threading.Thread(target=self.response,args=(self.listen_client(),))
            p.start()

def main():
    # import sys
    # print(sys.argv) # 获取命令行输入值
    # frame=__import__(frame_name) # 变量导入模块的方法
    # app=getattr(frame,app_name) # 获取模块相应函数
    wsgi_server=WSGIServer(4566)
    wsgi_server.run_server()
    wsgi_server.close_tcp()

if __name__=="__main__":
    main()
