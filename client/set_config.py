import configparser as cp

config = cp.ConfigParser()

config["DEFAULT"] = {
    "HOST" : "185.3.95.92",
    "PORT" : 4321
}

config["LOCALTEST_WIN"] = {
    "HOST" : "192.168.1.149",
    "PORT" : 4321
}

config["TEST"] = {
    "HOST" : "123.123.1.0",
    "PORT" : 1111
}

with open("clientconfig.ini", "w") as configfile:
    config.write(configfile)