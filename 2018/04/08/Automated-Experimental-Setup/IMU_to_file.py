# 03 April 2018 
# Reads in (arduino) serial port line by line, printing out on terminal. 
# Also opens tkinter window. Pressing any key in there writes the next serial line to a file
# In the terminal, Ctrl-C twice will exit the program. 
# Author: nrw
import os
import serial
import tty
import time
import tkinter as tk
import threading
from datetime import datetime

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop#459131
class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry('300x200')
        label = tk.Label(self.root, text="Press any key to append to file")
        label.pack()
        text = tk.Text(self.root, background='black', foreground='white', font=('Comic Sans MS', 12))
        text.pack()
        self.root.bind('<KeyPress>', self.onKeyPress)
        self.root.mainloop()

    def onKeyPress(self, event):
        print('Key pressed!')
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode()
        data += x 
        try:
            outf.write(data)
            outf.flush()
            print('done writing')
        except IOError as ioex: 
            print("I/O error({0}): {1}".format(ioex.errno, os.strerror(ioex.errno)))


app = App()
print('Now we can continue running code while mainloop runs!')

baud  = 115200
strtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
fname = strtime + '_accel_data.txt'
fmode = 'ab'
reps  = 100


outf = open(fname,fmode)

# https://stackoverflow.com/questions/17815686/detect-key-input-in-python
if os.path.exists('/dev/ttyACM0'):
    addr  = '/dev/ttyACM0'
else:
    addr  = '/dev/ttyACM1'

print('using addr', addr)

port = serial.Serial(addr,baud)
while 1:
    x = port.readline()
    print(x)


