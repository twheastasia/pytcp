
import sys
import socket
import threading

def receive_from(remote_socket):
    print "in receive_from"

def hexdump(remote_buffer):
    print "int hexdump"

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    print "in proxy_handler"
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)

    print "[*] Listening  on %s:%d" % (local_host, local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        print "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print "Usage: ./tcpProxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]"
        print "Example: ./tcpProxy.py 127.0.0.1 9000 192.168.1.106 9000 True"
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

main()
