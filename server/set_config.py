import configparser as cp

config = cp.ConfigParser()

config["LOCALTEST_WIN"] = {
    "BUFSIZE" : 1024,
    "HOST" : "192.168.1.149",
    "PORT" : 4321
}

config["DEFAULT"] = {
    "BUFSIZE" : 1024,
    "HOST" : "185.3.95.92",
    "PORT" : 4321
}

with open("serverconfig.ini", "w") as configfile:
    config.write(configfile)