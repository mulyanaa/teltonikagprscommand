import socket
from inputimeout import inputimeout
import time
import struct
from  crccheck.crc import Crc16Arc

def codec12_msg(message):
    buf = bytearray()
    content=message
    buf.extend(struct.pack('<I', 0))
    buf.extend(struct.pack('>I', len(content) + 8))

    buf.append(12)  # TeltonikaProtocolDecoder.CODEC_12

    buf.append(1)  # quantity

    buf.append(5)  # type

    buf.extend(struct.pack('>I', len(content)))

    buf.extend(map(ord, content))

    buf.append(1)  # quantity
# print(buf)
    crc_buf = buf[8:]
    print((buf.hex()).encode())
    print((crc_buf.hex()).encode())
    crc_int =int(Crc16Arc.calc(crc_buf))
    print(hex(crc_int))
    buf=buf+crc_int.to_bytes(4, 'big')
    print("Here is Codec 12 message")
    return bytes(buf)

def server_program():
    # get the hostname
    host = "127.0.0.1"
    port = 13213  

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1248)
        if not data:
            # if data is not received break
            time.sleep(0.5)
            break
        print("Data From Client")
        print(str(data.hex()))
        print(str(data.hex())[16:18])
        if (str(data.hex())[16:18] == "8e"):
            response_ = "000000" + str(data.hex())[18:20]
            time.sleep(5)
        
            print("sending response for AVL Ddata: " + response_)
            conn.send(bytes.fromhex(response_))  # send data to the client
            time.sleep(5)
            conn.send(codec12_msg("getinfo"))
        elif (str(data.hex())[16:18] == "08"):
            response_ = "000000" + str(data.hex())[18:20]
            time.sleep(5)
        
            print("sending response for AVL Ddata: " + response_)
            conn.send(bytes.fromhex(response_))  # send data to the client
        
        #data = inputimeout(prompt="masukan", timeout=10)
         

            
        elif (str(data.hex())[0:4] == "000f"):
            # sending confirmation when device send IMEI data
            conn.send(bytes.fromhex("01"))
            
        else:
            print("NOT CODEC 8 or 8E")
            print(str(data))
            
        print("")
        print("")
        print("")

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
