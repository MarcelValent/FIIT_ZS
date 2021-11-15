import socket
import threading

global clear
class KeepAlive(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = threading.Event()


    def stop(self):
        self.stop = True
        print("Communication terminated.")

    def send(self, port, ip, info):
        if not self.stop:
            while True:
              print("Communication successful")


def startserver():
    print("Port you want to listen on: ", end="")
    port = int(input())

def startclient():
    print("Port you want to send to: ", end="")
    port = int(input())

def main():
    clear = "\n" * 100
    print(clear)
    print("For role server type \"server\"")
    print("For role client type \"client\"")
    print("To close the programme type \"quit\"")
    role = input()
    if role == "server":
        startserver()
        print("If you want to change role type \"change\"")
        c = input()
        if c == "change":
            main()
    elif role == "client":
        startclient()
        print("If you want to change role type \"change\"")
        c = input()
        if c == "change":
            main()
    elif role == "quit":
        return 0

main()
