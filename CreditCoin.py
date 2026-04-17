import tkinter
from tkinter import *
import math
import random
from threading import Thread 
from collections import defaultdict
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import time
from tkinter import messagebox
from TrustedAuthority import *
import base64
from hashlib import sha1
from datetime import datetime
from web3 import Web3, HTTPProvider
import json

global vehicles
global labels
global vehicle_x
global vehicle_y
global text, tf1
global canvas
global vehicle_list
global key
global ta
global compute_time

def saveDataBlockChain(currentData): #calling to save data in blockchain
    global details
    global contract
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CreditCoinContract.json'
    deployed_contract_address = '0x9e9AEeEBbc1b4a5A46f016De9b77202ae366148A'
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails()
    details+=currentData
    msg = contract.functions.setData(details).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def readDetails(): #calling to read data from blockchain
    global details
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CreditCoinContract.json' #industrial contract code
    deployed_contract_address = '0x9e9AEeEBbc1b4a5A46f016De9b77202ae366148A' #hash address to access industrail contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    details = contract.functions.getData().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]
    return details        

def calculateDistance(iot_x,iot_y,x1,y1):
    flag = False
    for i in range(len(iot_x)):
        dist = math.sqrt((iot_x[i] - x1)**2 + (iot_y[i] - y1)**2)
        if dist < 80:
            flag = True
            break
    return flag

def createNetwork():
    global vehicles, labels, vehicle_x, vehicle_y, canvas
    vehicles = []
    vehicle_x = []
    vehicle_y = []
    labels = []
    canvas.update()
    x = 5
    y = 350
    vehicle_x.append(x)
    vehicle_y.append(y)
    name = canvas.create_oval(x,y,x+40,y+40, fill="blue")
    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text="Cloud Server")
    labels.append(lbl)
    vehicles.append(name)

    for i in range(1,20):
        run = True
        while run == True:
            x = random.randint(100, 450)
            y = random.randint(50, 600)
            flag = calculateDistance(vehicle_x,vehicle_y,x,y)
            if flag == False:
                vehicle_x.append(x)
                vehicle_y.append(y)
                run = False
                name = canvas.create_oval(x,y,x+40,y+40, fill="red")
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 8 italic bold",text="V"+str(i))
                labels.append(lbl)
                vehicles.append(name)
    
def generateKey():
    text.delete('1.0', END)
    global key
    global ta
    ta = TrustedAuthority()
    key = ta.getKey()
    private_key = sha1(key).hexdigest()
    text.insert(END,"Public Key : "+str(key)+"\n")
    text.insert(END,"Private or Secret Key : "+str(private_key)+"\n")
    
    
def startCommunication(text,canvas,line1,line2,x1,y1,x2,y2,x3,y3):
    class SimulationCommunicationThread(Thread):
        def __init__(self,text,canvas,line1,line2,x1,y1,x2,y2,x3,y3): 
            Thread.__init__(self) 
            self.canvas = canvas
            self.line1 = line1
            self.line2 = line2
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.x3 = x3
            self.y3 = y3
            self.text = text
            
 
        def run(self):
            time.sleep(1)
            for i in range(0,3):
                self.canvas.delete(self.line1)
                self.canvas.delete(self.line2)
                time.sleep(1)
                self.line1 = canvas.create_line(self.x1, self.y1,self.x2, self.y2,fill='black',width=3)
                self.line2 = canvas.create_line(self.x2, self.y2,25, 370,fill='black',width=3)
                time.sleep(1)
            self.canvas.delete(self.line1)
            self.canvas.delete(self.line2)
            canvas.update()
                
    newthread = SimulationCommunicationThread(text,canvas,line1,line2,x1,y1,x2,y2,x3,y3) 
    newthread.start()
    #newthread.join()

def updateIncentive(replier1, replier2):
    global compute_time
    x1 = vehicle_x[replier1]
    y1 = vehicle_y[replier1]

    x2 = vehicle_x[replier2]
    y2 = vehicle_y[replier2]
    start = time.time()
    msg = tf1.get()
    enc = ta.encrypt("V"+str(replier1)+"#"+msg+"#"+str(x1)+"#"+str(y1))
    verification_hashcode = sha1(enc).hexdigest()
    enc = str(base64.b64encode(enc),'utf-8')+"#"+str(datetime.fromtimestamp(time.time()))+"#"+str(verification_hashcode)+"#1"
    saveDataBlockChain(enc+"\n")
    end = time.time()
    compute_time.append(end-start)
    start = time.time()
    enc = ta.encrypt("V"+str(replier2)+"#"+msg+"#"+str(x2)+"#"+str(y2))
    verification_hashcode = sha1(enc).hexdigest()
    enc = str(base64.b64encode(enc),'utf-8')+"#"+str(datetime.fromtimestamp(time.time()))+"#"+str(verification_hashcode)+"#1"
    saveDataBlockChain(enc+"\n")
    end = time.time()
    compute_time.append(end-start)
    

def runSimulation():
    text.delete('1.0', END)
    global key, ta, compute_time
    compute_time = []
    start = time.time()
    initiator = int(vehicle_list.get())
    initiator_x = vehicle_x[initiator]
    initiator_y = vehicle_y[initiator]
    msg = tf1.get()
    enc = ta.encrypt("V"+str(initiator)+"#"+msg+"#"+str(initiator_x)+"#"+str(initiator_y))
    verification_hashcode = sha1(enc).hexdigest()
    text.insert(END,"User privacy announce message: "+str(enc)+"\n")
    text.insert(END,"Trace Manager Verification Code: "+str(verification_hashcode)+"\n")
    enc = str(base64.b64encode(enc),'utf-8')+"#"+str(datetime.fromtimestamp(time.time()))+"#"+str(verification_hashcode)+"#0"
    saveDataBlockChain(enc+"\n")
    end = time.time()
    compute_time.append(end-start)
    repliers = []
    for i in range(1,20):
        temp_x = vehicle_x[i]
        temp_y = vehicle_y[i]
        if i != initiator and temp_x < initiator_x and i not in repliers:
            dist = math.sqrt((initiator_x - temp_x)**2 + (initiator_y - temp_y)**2)
            if dist < 300:
                repliers.append(i)
    for i in range(len(repliers)):
        distance = 10000
        neighbour = -1    
        for k in range(1,20):
            if k not in repliers and k != initiator:
                temp_x = vehicle_x[i]
                temp_y = vehicle_y[i]
                replier_x = vehicle_x[k]
                replier_y = vehicle_y[k]
                dist = math.sqrt((replier_x - temp_x)**2 + (replier_y - temp_y)**2)
                if dist < distance:
                    distance = dist
                    neighbour = k
        if neighbour != -1:
            updateIncentive(repliers[i],neighbour)
            text.insert(END,"Initiator = "+str(initiator)+" Replier = "+str(repliers[i])+" Replier = "+str(neighbour)+"\n")
            line1 = canvas.create_line(vehicle_x[initiator]+20, vehicle_y[initiator]+20,vehicle_x[repliers[i]]+20, vehicle_y[repliers[i]]+20,fill='black',width=3)
            line2 = canvas.create_line(vehicle_x[repliers[i]]+20, vehicle_y[repliers[i]]+20,vehicle_x[neighbour]+20, vehicle_y[neighbour]+20,fill='black',width=3)
            startCommunication(text,canvas,line1,line2,(vehicle_x[initiator]+20),(vehicle_y[initiator]+20),(vehicle_x[repliers[i]]+20),(vehicle_y[repliers[i]]+20),(vehicle_x[neighbour]+20),(vehicle_y[neighbour]+20))
    
    

def TMVerification():
    global datas
    global ta
    text.delete('1.0', END)
    arr = readDetails().split("\n")
    for i in range(len(arr)):
        temp = arr[i].split("#")
        data = base64.b64decode(temp[0])
        decrypt = ta.decrypt(data)
        decrypt = decrypt.decode("utf-8")
        values = decrypt.split("#")
        #text.insert(END,str(values)+" "+temp[1]+" "+temp[2]+" "+temp[3]+"\n")
        text.insert(END,"Vehicle ID : "+values[0]+"\n")
        text.insert(END,"Sent Message : "+values[1]+"\n")
        text.insert(END,"Vehicle X Location : "+values[2]+"\n")
        text.insert(END,"Vehicle Y Location : "+values[3]+"\n")
        text.insert(END,"Date & Time : "+temp[1]+"\n")
        text.insert(END,"Verification Hashcode : "+temp[2]+"\n")
        text.insert(END,"Incentive Value : "+temp[3]+"\n\n")

def graph():
    global compute_time
    requests = []
    for i in range(len(compute_time)):
        requests.append("Req No"+str(i))
    height = compute_time
    bars = requests
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.title("Average Computation Time for Request, Reply & Verification")
    plt.show()

def Main():
    global text, tf1
    global canvas
    global vehicle_list
    root = tkinter.Tk()
    root.geometry("1300x1200")
    root.title("CreditCoin: A Privacy-Preserving Blockchain-Based Incentive Announcement Network for Communications of Smart Vehicles")
    root.resizable(True,True)
    font1 = ('times', 12, 'bold')

    canvas = Canvas(root, width = 800, height = 700)
    canvas.pack()

    l1 = Label(root, text='Initiator Vehicle')
    l1.config(font=font1)
    l1.place(x=820,y=10)

    vehicles_id = []
    for i in range(1,20):
        vehicles_id.append(str(i))
    vehicle_list = ttk.Combobox(root,values=vehicles_id,postcommand=lambda: vehicle_list.configure(values=vehicles_id))
    vehicle_list.place(x=970,y=10)
    vehicle_list.current(0)
    vehicle_list.config(font=font1)

    l2 = Label(root, text='Message to Send:')
    l2.config(font=font1)
    l2.place(x=820,y=60)

    tf1 = Entry(root,width=20)
    tf1.config(font=font1)
    tf1.place(x=970,y=60)

    createButton = Button(root, text="Create Vehicle Network", command=createNetwork)
    createButton.place(x=820,y=110)
    createButton.config(font=font1)

    taButton = Button(root, text="Trusted Authority Key Generation", command=generateKey)
    taButton.place(x=820,y=160)
    taButton.config(font=font1)

    ccButton = Button(root, text="Run CreditCoin Simulation", command=runSimulation)
    ccButton.place(x=820,y=210)
    ccButton.config(font=font1)

    tmButton = Button(root, text="Trace Manager Verification", command=TMVerification)
    tmButton.place(x=820,y=260)
    tmButton.config(font=font1)

    graphButton = Button(root, text="Computation Time Graph", command=graph)
    graphButton.place(x=1050,y=260)
    graphButton.config(font=font1)


    text=Text(root,height=20,width=60)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=820,y=310)
    
    
    root.mainloop()
   
 
if __name__== '__main__' :
    Main ()
    
