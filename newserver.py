import socket
import threading

host="localhost"
port=9999


s_clients=[]
s_user_names=[]
r_clients=[]
r_user_names=[]
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()





def transfer(client,user_name,file_name,file_size,message):
    try:
        send(client,f"Do you want to recieve {file_name.decode()} from {user_name}".encode())
        confirm=recieve(client)
        if confirm==b"y":
            send(client,file_size)
            file_size=recieve(client)
            send(client,message)
        index=r_clients.index(client)
        user_name=r_user_names[index]
        r_clients.remove(client)
        r_user_names.remove(user_name)
        return confirm

    except Exception as e:
        print(f"error transfer: {e}")
        client.close()




def send(client,message):
    try:
        while True:
            sent=client.send(message)
            message=message[sent:]
            if message==b"":
                client.send("<END>".encode())
                break
    except Exception as e:
        print(f"error send: {e}")
        client.close()


def recieve(client):
    message=b""
    while True:
        try:
            recv_message=client.recv(1024)
            if recv_message:
                message+=recv_message
                if(message[-5:]==b"<END>"):
                    return message[:-5]
        except Exception as e:
            print(f"error recieve: {e}")
            client.close()
            break
            

def s_handle(client):
    try:
        while True:
            usernames=' '.join(r_user_names)
            send(client,usernames.encode())
            user_name=recieve(client).decode()
            if user_name!="":
                break
        send(client,user_name.encode())
        file_name=recieve(client)
        send(client,file_name)
        file_size=recieve(client)
        send(client,file_size)
        data=recieve(client)
        index=r_user_names.index(user_name)
        reciever=r_clients[index]
        index=s_clients.index(client)
        user_name=s_user_names[index]
        confirm=transfer(reciever,user_name,file_name,file_size,data)
        if confirm==b'y':
            send(client,"sending file...".encode())
        else:
            send(client,"failed to send file...".encode())
        s_clients.remove(client)
        s_user_names.remove(user_name)

    
    except:
        index=s_clients.index(client)
        user_name=s_user_names[index]
        s_clients.remove(client)
        s_user_names.remove(user_name)






def choose(client,user_name):
    while True:   
        try: 
            choice=recieve(client).decode()

            if choice=='s':
                s_user_names.append(user_name)
                s_clients.append(client)
                s_handle(client)

            elif choice=='r':
                r_user_names.append(user_name)
                r_clients.append(client)
                while True:
                    if user_name not in r_user_names:
                        break
            
            else:
                print(f"{user_name} has left.")
                client.close()
        except Exception as e:
            print(f"{user_name} has left.")
            client.close()
            break






def start_conn():
    while True:
        try:
            client,address=server.accept()
            print(f"Connected with {address}")
            user_name=recieve(client).decode()
            print(f"user_name of client is {user_name}")
            thread=threading.Thread(target=choose,args=(client,user_name))
            thread.start()
        except KeyboardInterrupt:
            print("Server is closed.")
            break



start_conn()
