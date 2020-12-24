import threading
import socket
from collections import namedtuple
from threading import Lock

# global variables
udp_ip = "127.0.0.1"
udp_port1 = 5005
udp_port2 = 4000
hashMap = {}
lock = Lock()


def string_to_data_package(s):
    dataPackage = namedtuple("dataPackage", "id data")
    id, data = s.split('#')
    d = dataPackage(id=id, data=data)
    return d


def string_to_header_package(s):
    headerPackage = namedtuple("headerPackage", "id num_of_data_packages data")
    id, num_of_data_packages, data = s.split('#')
    h = headerPackage(id=id, num_of_data_packages=num_of_data_packages, data=data)
    return h


def received_all_data(id):
    lock.acquire()
    if hashMap[id][0] is None:
        lock.release()
        return False
    else:
        if int(hashMap[id][0].num_of_data_packages) == len(hashMap[id][1]):
            lock.release()
            return True
        else:
            lock.release()
            return False


def write_to_disk(id):
    print("Packages are written to disk- id: "+id+"\n")
    lock.acquire()
    file = open("output.txt", "a")
    file.write("------HEADER PACKAGE------\n")
    file.write("id:"+id+"\n")
    file.write("number of data packages: "+hashMap[id][0].num_of_data_packages+"\n")
    file.write("data: "+hashMap[id][0].data+"\n")
    for d in hashMap[id][1]:
        file.write("----DATA PACKAGE----\n")
        file.write("id:"+id+"\n")
        file.write("data: "+d.data+"\n")
    file.write("------------------------------------------------------------------------------------------------\n")
    file.close()
    lock.release()


def channel_1_listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((udp_ip, udp_port1))
    print("Channel 1 is ON\n")
    while True:
        data, unused = sock.recvfrom(1024)  # buffer size is 1024 bytes

        # creating a data package from the data received in buffer
        d = string_to_data_package(data.decode())

        lock.acquire()
        # if a package with this id didn't received yet
        if hashMap.get(d.id) is None:
            data_package_lst = [d]
            hashMap[d.id] = [None, data_package_lst]

        # if a package with this id did received (a record with this id exists)
        else:
            hashMap[d.id][1].append(d)
        lock.release()
        # if all packages for this id received
        if received_all_data(d.id):
            write_to_disk(d.id)


def channel_2_listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((udp_ip, udp_port2))
    print("Channel 2 is ON\n")
    while True:
        data, unused = sock.recvfrom(1024)  # buffer size is 1024 bytes

        # creating a header package from the data received in buffer
        h = string_to_header_package(data.decode())

        lock.acquire()
        # if a data package with this id didn't received yet
        if hashMap.get(h.id) is None:
            data_package_lst = []
            hashMap[h.id] = [h, data_package_lst]

        # if a data package with this id did received (a record with this id exists)
        else:
            hashMap[h.id][0] = h

        lock.release()
        # if all packages for this id received
        if received_all_data(h.id):
            write_to_disk(h.id)


def main():
    # create threads and run them
    channel_1_listener = threading.Thread(target=channel_1_listen)
    channel_2_listener = threading.Thread(target=channel_2_listen)
    channel_1_listener.start()
    channel_2_listener.start()


if __name__ == "__main__":
    main()
