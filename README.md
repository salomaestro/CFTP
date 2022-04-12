# Server - Client - File transfers with Python Sockets

*Christian salomonsen*

---

## **TOC**

1. [***Server***](#server)
    1. [***Server profile setup***](#server-profile-setup)
    2. [***Server parser***](#server-parser)
2. [***Client***](#client)
    1. [***Client profile setup***](#client-profile-setup)
3. [***Requirements***](#requirements)


## **Server**
---
The server is started by executing,

``` vim
$ ./start_server.py
```
This does however mean you already need to have configurations set up properly.

### **Server profile setup**
---

To correctly setup configurations in the server, open [`server/set_config.py`](server/set_config.py) and follow the standard template, either create a new profile:

``` python
config["MY_PROFILE"] = {
    "HOST" : "192.168.0.x",    # Both local and remote works.
    "PORT" : 1111,             # Be aware; not all ports will work.
    "BUFSIZE": 1024            # Set size of buffer (1024 works well).
}
```

or change the **DEFAULT** profile:

``` python
config["DEFAULT"] ) {
    "HOST" : "192.168.0.x",
    "PORT" : 1111,
    "BUFSIZE": 1024
}
```

### **Server parser**
---

Let's take a look back at how we can setup our server with the new profiles we just made. In your shell to start server with the **DEFAULT** profile, type:

``` vim
$ ./start_server.py
```

Or list the avaliable profiles:

``` vim
$ ./start_server.py -l
```

Then select one of the listed profiles:

``` vim
$ ./start_server.py MY_PROFILE
```

Furthermore a clever thing to do is to add `start_server.py` to **PATH** (`export PATH=$PATH:path_to_dir_of_script`).

To run the script in the background on your system or remote server use:

``` vim
$ screen -d -m start_server.py MY_PROFILE
```


## **Client**
---

To send a file to the server from a client system use:

``` vim
start_client.py -f my_file.txt
```

To see the avaliable profiles use:

``` vim
start_client.py -l
```

And to send file using different profile use:

``` vim
start_client.py MY_PROFILE -f my_file.txt
```

### **Client profile setup**

To correctly setup configurations on the client side, open [`client/set_config.py`](client/set_config.py), add or edit an existing user profile using:

``` python
config["MY_PROFILE"] = {
    "HOST" : "192.168.0.255",    # Ip adress to send file to.
    "PORT" : 1111
}
```

Or edit the **DEFAULT** profile:

``` python
config["DEFAULT"] = {
    "HOST" : "192.168.0.255",    # Ip adress to send file to.
    "PORT" : 1111
}
```

---

## **Requirements**