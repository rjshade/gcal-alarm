import sys, os, time, serial

class arduino:
    init = False
    def __init__(self, path):
        self.connection = serial.Serial( path, 9600 )
        self.init = True

    def __del__(self):
        if self.init:
            self.connection.close()

    def isOpen(self):
        return self.connection.isOpen()

    def writeLine(self, line):
        if self.isOpen():
            for i in range(0, len(line)):
                self.connection.write(line[i])
                time.sleep(0.1)

