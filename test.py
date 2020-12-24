import threading
import socket
from collections import namedtuple
import string
import random

# global variables
udp_ip = "127.0.0.1"
udp_port1 = 5005
udp_port2 = 4000
id_arr = []
num_of_data_packages_arr = []
TEST_NUM_OF_HEADERS = 5
TEST_NUM_OF_DATA = 5


def data_package_to_string(d):
    return d.id + "#" + d.data


def header_package_to_string(h):
    return h.id + "#" + h.num_of_data_packages + "#" + h.data


def channel_1_send():
    # create a data package struct
    dataPackage = namedtuple("dataPackage", "id data")

    #create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #create and send data packages
    for i in range(len(id_arr)):
        for j in range (num_of_data_packages_arr[i]):
            data_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=498))
            d = dataPackage(id=str(id_arr[i]), data=data_str)
            message = data_package_to_string(d)
            sock.sendto(str.encode(message), (udp_ip, udp_port1))


def channel_2_send():
    # create a header package struct
    headerPackage = namedtuple("dataPackage", "id num_of_data_packages data")

    # create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

    # create and send header packages
    for i in range(len(id_arr)):
        data_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=47))
        h = headerPackage(id=str(id_arr[i]), num_of_data_packages=str(num_of_data_packages_arr[i]), data=data_str)
        message = header_package_to_string(h)
        sock.sendto(str.encode(message), (udp_ip, udp_port2))


def main():
    # create a random id's array and random num of data packages's array
    for i in range(TEST_NUM_OF_HEADERS):
        id_arr.append(random.randint(0,99))
        num_of_data_packages_arr.append(random.randint(0,TEST_NUM_OF_DATA))

    # create threads and run them
    channel_1_sender = threading.Thread(target=channel_1_send)
    channel_2_sender = threading.Thread(target=channel_2_send)
    channel_1_sender.start()
    channel_2_sender.start()
    channel_1_sender.join()
    channel_2_sender.join()


if __name__ == "__main__":
    main()