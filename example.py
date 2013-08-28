import uniddeconnector
import params

class MyClient(uniddeconnector.Client):
    def send_ping(self):
        pass
    def read_event(self,data):
        print data
        
    def custom_handlers(self):
        self.event=uniddeconnector.Event()
        
    def handle_close(self):
        self.close()
        self.event.disconnected()
        self.buffer=''
        #self.Auth()



if __name__ == "__main__":
    server = MyClient(params.host, params.port, params.login, params.password)
    server.scheduler.asyncoreLoop(timeout=0.01)

