
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication

from T2G.TachyReader import TachyReader


class TachyTestFixture(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        self.tachyReader = TachyReader(QSerialPort.Baud9600)
        self.tachyReader.setPort('COM11')
        self.pollingThread = QThread()
        self.tachyReader.moveToThread(self.pollingThread)
        self.pollingThread.start()
        self.tachyReader.lineReceived.connect(self.vertexReceived)
        self.tachyReader.beginListening()
        self.lineCount = 0

    def vertexReceived(self, line):
        print(line)
        self.lineCount += 1
        if self.lineCount > 3:
            self.tachyReader.shutDown()

    def shutDown(self):
        self.tachyReader.shutDown()

if __name__ == '__main__':
    portNames = [port.portName() for port in QSerialPortInfo.availablePorts()]
    for portName in portNames:
        print(portName)
    testFixture = TachyTestFixture(sys.argv)
    testFixture.exec_()
    testFixture.shutDown()

