import json
import socket
import random

localDNS_IP = '127.0.0.1'
localDNS_PORT = 53000

myIp = '127.0.0.1'
myPort = 53001


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((myIp, myPort))



def makeDNSquery(inputAddr):
    DNSid = random.randint(0, 0xFFFFFFFFFFFF)
    DNSid = str(hex(DNSid))
    
    query = {
        "TransactionID": DNSid,
        "Domain": web
    }
    return json.dumps(query), DNSid


def sendDNSquery(inputAddr):
    query, DNSid = makeDNSquery(inputAddr)
    print(query)
    sock.sendto(query.encode(), (localDNS_IP, localDNS_PORT))
    return DNSid
    
    
def recieveQuery(qID):
    recievedQid = ""
    while(recievedQid != qID):
        response, localDNSid = sock.recvfrom(512)
        print(response.decode())
        response = json.loads(response.decode())
        recievedQid = response["TransactionID"]
    print(response)
    return response["value"]
    
    
def checkCache(web):
    data = ""
    with open ("/home/badar/Desktop/Assignments/Cyber & Network/localCache.txt") as file:
        data = (file.read())

    if len(data)>0:
        data = json.loads(data)
        for i in data:
            if data[i]["domain"] == web:
                return data[i]["ip"]
        return False
    else:
        return False
    
def updateCache(domain, ip):
    newRec = {"domain": domain, "ip": ip}
    with open ("/home/badar/Desktop/Assignments/Cyber & Network/localCache.txt") as file:
        data = (file.read())
        data.replace("\'", "\"")
    if len(data)>0:
        data = json.loads(data)
        for i in data:
            if data[i]["domain"] == web:
                data[i]["ip"] = ip
        data[len(data)] = newRec
        with open ("/home/badar/Desktop/Assignments/Cyber & Network/localCache.txt", "w") as file:
            data = json.dumps(data)
            file.write(data)
    else:
        #newRec = json.dumps()
        with open ("/home/badar/Desktop/Assignments/Cyber & Network/localCache.txt", "w") as file:
            data = json.dumps({0:newRec})
            file.write(data)
    
    
while True:
    web = input("Web: ")
    #check local cache
    if(checkCache(web)):
        print("Cache Found: ",checkCache(web))
    else:
        print("Cache Not Found")
        #send query to local DNS
        DNSid = sendDNSquery(web)
        
        #Recieve Query
        try:
            ip = recieveQuery(DNSid)
            
            updateCache(web, ip)
        except:
            print("Domain not Found")

    break

print('Connection Closed')
sock.close()