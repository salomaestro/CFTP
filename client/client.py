import socket, os, time, configparser, logging

class Client:
    PATH = os.path.dirname(__file__)
    LOGPATH = os.path.join(PATH, "logs")
    CONFIGPATH = os.path.join(PATH, "clientconfig.ini")
    LOGFORMAT = "%(levelname)s : %(asctime)s : %(message)s"

    def __init__(self, profile):
        config = configparser.ConfigParser()
        config.read(self.CONFIGPATH)

        host = config[str(profile)]

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.addr = self.ip, self.port = host["host"], int(host["port"])

        try:
            self.client.connect(self.addr)
            self.bufsize = self.client.recv(100).decode()
            print("Connected to server. GO FOR COMMAND!...")
        except:
            print("Unable to connect...")
            exit()

    @staticmethod
    def safesend(conn, content):
        out = conn.send(str(content).encode())
        conn.recv(100).decode()
        return out

    @staticmethod
    def saferecv(conn):
        out = conn.recv(100).decode()
        conn.send(str.encode("0"))
        return out

    def send_file(self, filename=None, path=None):
        if filename is None:
            filename = input("Filename: ")
        if path is None:
            path = self.PATH

        filesize = os.path.getsize(os.path.join(path, filename))

        self.safesend(self.client, filename)
        self.safesend(self.client, filesize)

        with open(filename, "rb") as file:
            c = 0

            while c <= filesize:
                data = file.read(int(self.bufsize))

                if not data: break

                self.client.send(data)

                c += len(data)
        
        print(f"{filename} sent. Transfer complete.")
        self.client.close()

if __name__ == "__main__":
    cli = Client("DEFAULT")
    cli.send_file()