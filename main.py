import sys
import os
import socket
import time
import struct
import select
from checksum import calc_checksum

ECHO_REQUEST = 8
ECHO_RESPONSE = 0

TIMEOUT = 5
MAX_TIME_TO_LIVE = 30

def print_timeout(ttl, first_time):
    print('{0}\t{1} ms\t***.***.***.***\t(Timeout)'.
        format(ttl,
            int((time.time() - first_time) * 1000.00)))

def print_str(ttl, first_time, addr, hostname):
    print('{0}\t{1} ms\t{2}\t{3}'.
        format(ttl,
            int((time.time() - first_time) * 1000.00),
                 addr[0],
                 hostname))

def get_package(id):
    initial_checksum = 0
    initial_icmp_package = struct.pack("bbHHh",
                                 ECHO_REQUEST,
                                 ECHO_RESPONSE,
                                 initial_checksum,
                                 id,
                                 1)

    calculated_checksum = calc_checksum(initial_icmp_package)
    icmp_package = struct.pack("bbHHh",
                         ECHO_REQUEST,
                         ECHO_RESPONSE,
                         calculated_checksum,
                         id,
                         1)
    return icmp_package

def ping(dest_addr, icmp_socket, time_to_live, id):

    icmp_package = get_package(id)

    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, time_to_live)

    icmp_socket.sendto(icmp_package, (dest_addr, 1400))

    start_time = time.time()
    socketResponse = select.select([icmp_socket], [], [], TIMEOUT)
    if socketResponse[0] == []:
        print_timeout(time_to_live, start_time)
        return False

    recv_packet, addr = icmp_socket.recvfrom(1024)

    hostname = ''
    try:
        host_inf = socket.gethostbyaddr(addr[0])
        if host_inf:
            hostname = host_inf[0]
    except:
        hostname = 'Unknown'

    print_str(time_to_live, start_time, addr, hostname)

    if addr[0] == dest_addr:
        return True

    return False

def get_socket():
    icmp_proto = socket.getprotobyname("icmp")
    try:
        icmp_socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_RAW,
                                    icmp_proto)
        return icmp_socket
    except socket.error as exception:
        print("Error " + exception)

def main():

    dest_host = sys.argv[1]
    dest_addr = socket.gethostbyname(dest_host)

    time_to_live = 1
    id = 1

    while (time_to_live < MAX_TIME_TO_LIVE):
        icmp_socket = get_socket()

        if (ping(dest_addr, icmp_socket, time_to_live, id)):
            icmp_socket.close()
            break

        time_to_live += 1
        id += 1
        icmp_socket.close()
    os._exit(0)

main()
