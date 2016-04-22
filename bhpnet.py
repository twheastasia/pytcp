#utf-8
import sys
import socket
import getopt
import threading
import subprocess


listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print "BHP Net Tool"
    print ""
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listien"
    print "-e --execute=file_to_run"
    print "-c --command"
    print "-u --upload=destination"
    print ""
    print "Examples:"
    print "bhpnet.py -t 192.168.1.106 -p 55555 -l -c"
    print "bhpnet.py -t 192.168.1.106 -p 55555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.1.106 -p 55555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDE' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    print "start"
    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port >0:
        buffer = sys.stdin.read()

        client_sender(buffer)

    if listen :
        server_loop()
