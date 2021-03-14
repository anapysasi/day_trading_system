import socket
import threading
from functools import reduce
import csv
import json
import argparse
import sys
import time
import datetime
import pandas as pd
import numpy as np
import random
from collections import defaultdict

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

class ThreadedServer(object):
    def __init__(self, host, opt):
        self.environment = {}
        self.environment['NoMode'] = {'points' : 0}
        self.environment['Occupancy'] = {'occupancy' : 0, 'points' : 0}
        self.host = host
        self.port = opt.port
        self.opt = opt
        self.state = self.environment[opt.mode if opt.mode else 'NoMode']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.lock = threading.Lock()

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(500)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            threading.Thread(target = self.sendCSVfile,args = (client,)).start()

    def handle_client_answer(self, obj):
        if self.opt.mode is not None and self.opt.mode == 'Occupancy':

            if 'Occupancy' not in obj:
                return
            self.lock.acquire()
            if self.state['occupancy'] == int(obj['Occupancy']):
                self.state['points'] += 1
            self.lock.release()
        return

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size).decode()
                if data:
                    # Set the response to echo back the recieved data
                    a = json.loads(data.rstrip('\n\r '))
                    self.handle_client_answer(a)

                    # client.send(response)
                else:
                    print('Client disconnected')
                    return False
            except:
                print('Client closed the connection')
                print("Unexpected error:", sys.exc_info()[0])
                client.close()
                return False

    def handleCustomData(self,buffer):
        if self.opt.mode is not None and self.opt.mode=='Occupancy':
            self.lock.acquire()
            buffer['date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.state['occupancy']= int(buffer['Occupancy'])
            buffer['Occupancy']=-1
            self.lock.release()

    def convertStringToJSON(self,st):
        return json.dumps(st, cls=NpEncoder)

    def handleCustomData(self,buffer):
        if self.opt.mode is not None and self.opt.mode=='Occupancy':
            self.lock.acquire()
            buffer['date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.state['occupancy']= int(buffer['Occupancy'])
            buffer['Occupancy']=-1
            self.lock.release()

    def sendStreamToClient(self,client,buffer, num_stocks):
        counter = 0
        for i in buffer:
            #self.handleCustomData(i)
            print(i)
            try:
                client.send((self.convertStringToJSON(i)+'\n').encode('utf-8'))
                counter += 1
                if counter == num_stocks:
                    time.sleep(self.opt.interval)
                    counter = 0
            except:
                print('End of stream')
                return False
        time.sleep(self.opt.interval)
        client.send((self.convertStringToJSON(self.state) + '\n').encode('utf-8'))
        return False

    def sendCSVfile(self, client):
        for f in self.opt.files:
            print('reading file %s...' % f)
            # csvfile = open(f, 'r')
            reader = pd.read_csv(f)
            # Lets get the symbols as a list
            symbols = list(set(np.array(reader['Symbol'])))
            # Number of symbols we want to choose
            num_to_select = self.opt.stocks
            # Random election of num_to_select Symbols
            list_of_random_items = random.sample(symbols, num_to_select)
            length = []
            for i in range(num_to_select):
                N = len(reader[reader['Symbol'] == list_of_random_items[i]])
                length.append(N)

            N = min(length)
            out = []

            for j in range(N):
                for i in range(num_to_select):
                    send = reader[reader['Symbol'] == list_of_random_items[i]]
                    send = send.iloc[j]
                    out.append(send.to_dict())
            self.sendStreamToClient(client, out, num_to_select)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='usage: tcp_server -p port [-f -m]')
    parser.add_argument('-f', '--files', nargs='+')
    parser.add_argument("-m", "--mode", action="store", dest="mode")
    parser.add_argument("-p", "--port", action="store", dest="port", type=int)
    parser.add_argument("-t", "--time-interval", action="store",
                        dest="interval", type=int, default=1)
    parser.add_argument("-s", "--stocks", action="store",
                        dest="stocks", type=int, default=1)

    opt = parser.parse_args()
    if not opt.port:
        parser.error('Port not given')

    # Code for Terminal: python tcp_server.py -p 9999 -f finance.csv

    # Added line of code
    # print(ThreadedServer('127.0.0.1', opt).sendCSVfile())

    ThreadedServer('127.0.0.1', opt).listen()
