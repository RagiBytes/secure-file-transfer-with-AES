import socket
from Crypto.Cipher import AES
import os

key=b"abcdefghijklmnop"
nonce=b"ponmlkjihgfedcba"
file_name=None
file_size=None

host="localhost"
port=9999

user_name=input("Enter Username: ")

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))


def encrypt(data):
    cipher=AES.new(key,AES.MODE_EAX,nonce)
    return cipher.encrypt(data)

def decrypt(data):
    cipher=AES.new(key,AES.MODE_EAX,nonce)
    return cipher.decrypt(data)


def read_file(file_name):
    file=open(file_name,"rb")
    return file.read()

def write_file(data):
    file=open(input("Enter name for recieved file: "),"wb")
    file.write(decrypt(data))


def send(message):
    try:
        while True:
            sent=client.send(message)
            message=message[sent:]
            if message==b"":
                client.send("<END>".encode())
                break
    except Exception as e:
        print(f"Error send: {e}")



def recieve():
    message=b""
    while True:
        try:
            recv_message=client.recv(1024)
            if recv_message:
                message+=recv_message
                if message[-5:]==b"<END>":
                    return message[:-5]
        except Exception as e:
            print(f"error recieve: {e}")
            
def read():
    username=recieve()
    choice=input(f"{username} wants to transfer a file,\nEnter 'y' for yes,\nEnter any other value for no: ")
    if choice=="y":
        send(choice.encode())
        file_size=recieve()
        send(file_size)
        data=recieve()
        write_file(data)

    else:
        return



def write():
    username=None
    user_names=[]
    while username not in user_names:
        usernames=recieve().decode()
        user_names=usernames.split()
        print(f"The users ready to recieve data are: {usernames}.")
        username=input("Enter recievers Username, press ENTER to refresh: ")
        if username =="":
            send(username.encode())
            print("Refreshing...")
        elif username not in user_names:
            print(f"{username} not found...")
        
        else:
            send(username.encode())
            username=recieve().decode()
            print(f"sending files to {username}")
            break
    file_name=input("Enter file name to be transferred: ")
    file_size=os.path.getsize(file_name)
    send(file_name.encode())
    file_name=recieve().decode()
    send(str(file_size).encode())
    file_size=recieve().decode()
    data=encrypt(read_file(file_name))
    send(data)
    



def main():
    send(user_name.encode())
    while True:
        choice=input("Enter 's' to send a file,\nEnter 'r' to recieve a file,\n Enter anything else to quit: ")
        send(choice.encode())
        print(choice)

        if choice=='s':
            write()            
        elif choice=='r':
            read()
        else:
            client.close()
            break



    


if __name__=="__main__":
    main()