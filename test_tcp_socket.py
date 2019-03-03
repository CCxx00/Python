import socket

def send_msg():
    # create udp socket
    udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # des_ip,des_port
    des_ip_port=("192.168.1.102",8080)

    while True:
        # input by keyboard
        msg=input("input msg:")
        # send msg by socke
        udp_socket.sendto(msg.encode("utf-8"),des_ip_port)

    # close socket
    udp_socket.close()

def accept_msg():
    # create udp socket
    udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # src_ip_port
    src_ip_port=("",4566)
    # set src_ip_port
    udp_socket.bind(src_ip_port)

    while True:
        # accept msg by socke
        accept_msg=udp_socket.recvfrom(1024)
        # print accept_msg
        print(accept_msg[0].decode("utf-8"))

    # close socket
    udp_socket.close()

def main():
    accept_msg()

if __name__=="__main__":
    main()
