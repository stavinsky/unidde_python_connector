import uniddeconnector
import params

class MyClient(uniddeconnector.Client):
    def read_event(self,data):
        print data
                



if __name__ == "__main__":
    server = MyClient(params.host, params.port, params.login, params.password)
    server.scheduler.asyncoreLoop(timeout=0.01)

"""
################### Sample params.py #######################
#!/usr/bin/python
login = 'test'
password = 'test'
host = 'host'
port = 2222
"""
