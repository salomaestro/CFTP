import socket, logging, os, configparser, time, sys
from _thread import start_new_thread

class Server:
    PATH = os.path.dirname(__file__)
    LOGPATH = os.path.join(PATH, "logs")
    RECVPATH = os.path.join(PATH, "recieved")
    CONFIGPATH = os.path.join(PATH, "serverconfig.ini")
    # LOGFORMAT = "%(asctime)s-%(clientip)-15s-%(profile)s-%(message)s"
    LOGFORMAT = "%(levelname)s : %(asctime)s : %(message)s"

    def __init__(self, profile=None):
        config = configparser.ConfigParser()
        config.read(self.CONFIGPATH)

        # setup logger
        logging.basicConfig(filename=os.path.join(self.LOGPATH, "server.log"), level=logging.DEBUG, filemode="w", format=self.LOGFORMAT)

        # Ask user for what user profile it wants to load.
        if profile is None:
            profile = self._ask_profile(self._find_avaliable_users(config))

        self.user = config[profile]

        self.bufsize = int(self.user["bufsize"])

        self.host = self.ip, self.port = self.user["host"], int(self.user["port"])

        self._set_up_server()

        self.today_recieve_dir = os.path.join(self.RECVPATH, self._make_date_dir())

    def _make_date_dir(self):
        
        today = time.strftime("%d%m%y", time.localtime())
        
        if not today in os.listdir(self.RECVPATH):
            os.makedirs(os.path.join(self.RECVPATH, today))
            logging.debug(f"Making directory for {today}.")

        return today
    
    def run(self):
        
        print("Waiting for connection")
        while True:
            try:
                # Accept client connections.
                conn, addr = self.s.accept()

                self.today_recieve_dir = os.path.join(self.RECVPATH, self._make_date_dir())
            
                logging.info(f"Connected to {addr}")

                # Start a new thread for each client.
                start_new_thread(self.threaded_client, (conn,))

            except KeyboardInterrupt as e:
                logging.critical("KeyboardInterrupt. Closing server.")
                sys.exit()

    def _recv_file(self, conn):

        filename = self.saferecv(conn)
        filesize = self.saferecv(conn)

        logging.info(f"Starting file transfer of {filename} at {filesize} b.")

        try:
            with open(os.path.join(self.today_recieve_dir, filename), "wb") as file:
                c = 0

                start_time = time.time()

                while c <= int(filesize):
                    data = conn.recv(self.bufsize)

                    if not data: break

                    file.write(data)

                    c += len(data)

                stop_time = time.time()

            logging.info(f"File transfer complete. Took {stop_time - start_time:.1f}s.")

        except Exception as e:
            logging.error(e)

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

    def threaded_client(self, conn):
        conn.send(str(self.bufsize).encode())

        self._recv_file(conn)

        conn.close()

    def _set_up_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        try:
            self.s.bind(self.host)
        except socket.error as e:
            print(f"Unable to start server at address {self.ip}:{self.port}")
            logging.error(e)
            exit(0)
        self.s.listen(5)

        # Log that server is up.
        logging.info(f"Server started at host - {self.ip}, port - {self.port}")

    @staticmethod
    def _ask_profile(available_users):
        while True:
            print("Avaliable users:")
            for key, item in available_users.items():
                print(f"{key} - {item}")
            print("")
            selection = input("Choose user from the aboves (press enter for default): ")

            if not selection:
                return "DEFAULT"
            
            if int(selection) in available_users:
                return available_users[int(selection)]

            print("====================\nNot an option!")
            
    @staticmethod
    def _find_avaliable_users(config):
        """ Finds avaliable users stored in config file for server
        
        Args
        ----
        config : ConfigParser
            Parser of configs.
        
        Returns : dict
            Dictionary of avaliable users where keys are arbitrary selectable int's
            and items are users.
        """
        return {i:configuser for i,configuser in enumerate(config.sections(), start=1)}

if __name__ == "__main__":
    s = Server()
    s.run()