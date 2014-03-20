#!/usr/bin/python
import asyncore
import traceback
from time import sleep
import socket
import errno
from sys import path
path.append('../asyncore_scheduler')
from asyncore_scheduler import Task, Scheduler


class Event():
    @staticmethod
    def connected(server=None):
        print 'Connected to %s' % server
    @staticmethod
    def disconnected(server=None):
        print 'Disconnected from %s' % server
    @staticmethod
    def error():
        print "my error start"
        print traceback.format_exc()
        print "my error stop"


class Client(asyncore.dispatcher):
    scheduler = Scheduler()

    def __init__(self, host, port, login, password, event=Event(), **kwargs):

        self.event = event
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.cutted_line = ''
        self.task1 = Task(start=2, repeatable=True, interval=3, function=self.send_ping)
        self.scheduler.addTask(self.task1)
        self.Auth()
        self.kwargs = kwargs
        self.custom_handlers()
        self.custom_init()

    def custom_init(self):
        pass

    def read_event(self, data):
        print data

    def send_ping(self):
        if self.connected:
            self.buffer = '> ping \n'

    def custom_handlers(self):
        pass

    def Auth(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))
        self.buffer = '%s\n%s\n' % (self.login, self.password)
        self.socket.settimeout(10.0)
        self.event.connected(server=self.host)

    def handle_error(self):
        if socket.errno in ( errno.ECONNREFUSED, errno.ECONNABORTED, errno.ECONNRESET, errno.ENETUNREACH):
            self.event.error()
            sleep(10)
            return
        self.event.error()

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()
        self.event.disconnected(server=self.host)
        sleep(10)
        self.buffer = ''
        self.Auth()

    def handle_read(self):
        raw = self.recv(8192)
        if "Access denied" in raw:
            print "Access denied %s", self.host
            return
        if self.cutted_line != '':
            raw = self.cutted_line + raw
            self.cutted_line = ''
        ignore_words = [test in raw for test in ('Login', 'Password', "Access", "Connector", "Copyright")]
        if any(ignore_words):
            return
        if raw[-2:] == '\r\n':
            data = raw.splitlines()
        else:
            data = raw.splitlines()
            if len(data) > 0:
                self.cutted_line = data.pop()

        for line in data:
            self.read_event(line)

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]