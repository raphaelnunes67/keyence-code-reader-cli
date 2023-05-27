import click
import socket
import re

def perform_read(host: str, port: int) -> None:
    """
    Perform a read.

    :param host: host device
    :type host: str
    :param port: port device
    :type port: str

    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))

        request_data = [0x1B, 0x4C, 0x4F, 0x4E, 0x0D]  # [ESC]LON[CR]
        finish_data = [0x4C, 0x4F, 0x46, 0x46, 0x0D]  # LOFF[CR]

        s.send(bytearray(request_data))

        received_data = s.recv(1024)

        s.send(bytearray(finish_data))

        print("Received data:")
        print(received_data.decode('utf-8'))

        s.close()

    except OSError:
        print('Was not possible to establish a connection...')


def perform_tuning(host: str, port: int, bank) -> None:
    """
    Perform tuning of target bank.

    :param host: host device
    :type host: str
    :param port: port device
    :type port: str
    :param bank: bank
    :type bank: int

    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))

        s.sendall('FTUNE\r'.encode())

        ftune_result = s.recv(1024).decode('utf-8')

        print("FTUNE result:")
        print(ftune_result)

        if ftune_result.index('OK') != -1:
            s.sendall(f'TUNE, {bank}\r'.encode())

            tune_result = s.recv(1024).decode('utf-8')

            print("TUNE result:")
            print(tune_result)

            s.sendall('TQUIT\r'.encode())

            s.recv(1024).decode('utf-8')

        s.close()

    except OSError:
        print('Was not possible to establish a connection...')


def clear_buffer(host: str, port: int) -> None:
    """
    Clear SR-1000's buffer.

    :param host: host device
    :type host: str
    :param port: port device
    :type port: str

    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))

        s.sendall('BCLR\r'.encode())

        reset_result = s.recv(1024).decode('utf-8')

        print('CLEAR RESULT:')
        print(reset_result)

        s.close()

    except OSError:
        print('Was not possible to establish a connection...')


def get_version(host: str, port: int) -> None:
    """
    Version confirmation.

    :param host: host device
    :type host: str
    :param port: port device
    :type port: str

    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))

        s.sendall('KEYENCE\r'.encode())

        version = s.recv(1024).decode('utf-8')

        print('VERSION RESULT:')
        print(version)

        s.close()

    except OSError:
        print('Was not possible to establish a connection...')


def set_time(host: str, port: int, time:str) -> None:
    """
    Set time in SR1000.

    :param host: host device
    :type host: str
    :param port: port device
    :type port: str

    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))

        s.sendall(f'TMSET,{time}\r'.encode())

        result = s.recv(1024).decode('utf-8')

        print('SET TIME: ')
        print(result)

        s.close()

    except OSError:
        print('Was not possible to establish a connection...')


def get_time(host: str, port: int) -> None:
    """
    Get current time in SR1000.

    :param host: host device
    :type host: str
    :param port: port device
    :type port: str

    """

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))

        s.sendall('TMGET\r'.encode())

        time = s.recv(1024).decode('utf-8')

        print('GET TIME: ')
        print(time)

        s.close()

    except OSError:
        print('Was not possible to establish a connection...')


@click.command()
@click.option('--operation', '-o', help='Select operation', required=True)
@click.option('--bank', '-b', help='Select a specific bank, default: 1', default=1)
@click.option('--host', '-h', help='SR1000 host', required=True)
@click.option('--port', '-p', help='SR1000 port, default: 9004', default=str(9004))
@click.option('--time', '-t', help='time to set', default=str(20230101000000))
def main(operation: str, bank: int, host: str, port: str, time: str):

    host_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

    port_regex = re.compile(r"^[1-9][0-9]{0,3}$|^0$")


    if not host_pattern.match(host):
        print('Invalid host')

    if not port_regex.match(port):
        print('Invalid port')

    else:
        port = int(port)

        if operation == 'tune':
            perform_tuning(host, port, bank)

        elif operation == 'read':
            perform_read(host, port)

        elif operation == 'version':
            get_version(host, port)

        elif operation == 'clear':
            clear_buffer(host, port)

        elif operation == 'set-time':
            set_time(host, port, time)

        elif operation == 'get-time':
            get_time(host, port)

        else:
            print('Operation invalid')



if __name__ == '__main__':
    main()