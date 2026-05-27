import socket

NETLINK_USERSOCK = 18

def send_to_kernel(data):
    try:
        s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_USERSOCK)
        s.bind((0, 0))
        s.send(data.encode())
        s.close()
    except Exception as e:
        print(f"Netlink error: {e}")
