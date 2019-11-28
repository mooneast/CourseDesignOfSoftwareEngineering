from tkinter import *
from tkinter.ttk import *
import sys
import platform
import serial
import time
import threading

ser = serial.Serial()
sp_list = ['COM1', 'COM2']


def COMOpen():
    global running
    if not isOpened.isSet():
        try:
            ser.timeout = 1
            ser.xonxoff = 0
            ser.port = comx.get()
            ser.baudrate = int(baud.get())
            print(ser.port)
            ser.open()
            running = True
            print(running)
            t = threading.Thread(target=recevie, args=(ser,))
            t.start()
        except Exception:
            print('COM Open Error!')
        else:
            isOpened.set()
            Open.set('close')
    else:
        running = False
        ser.close()
        isOpened.clear()
        Open.set('open serial')


def Submit():
    s1 = inputbox.get().encode()
    print('s1\n')
    datain = ser.write(s1)


def recevie(obj):
    global running
    print('start:\n')
    while (running == True):
        rx_len = obj.inWaiting()
        if (rx_len):
            s0 = obj.read(rx_len)
            print('s0\n')
            txt0.insert(END, s0)
    print('stop:\n')


def test():
    dataout = ser.read()
    txt0.insert(0.0, dataout)


if __name__ == "__main__":
    isOpened = threading.Event()
    root = Tk()
    root.title('RS-232串口通信')
    txt0 = Text(root, width=40, height=15, border=5)
    txt0.pack(side='top')
    sec0 = Frame(root, border=4)
    sec0.pack(side='top', anchor='w')
    sec1 = Frame(root, border=4)
    sec1.pack(side='top', anchor='w')
    sec2 = Frame(root, border=4)
    sec2.pack(side='top', anchor='w')
    sec3 = Frame(root, border=4)
    sec3.pack(side='top', anchor='w')
    sec4 = Frame(root, border=4)
    sec4.pack(side='top', anchor='w')

    comx = StringVar(root, sp_list[0])
    Label(sec0, text='串   口: ').pack(side='left')
    Combobox(sec0, text=comx, values=sp_list, width='12').pack(side='left')

    Open = StringVar(root, '打开串口')
    Button(sec0, textvariable=Open, width=12, command=COMOpen).pack(side='left')

    baud = StringVar(root, "9600")
    Label(sec1, text='波特率: ').pack(side='left')
    Combobox(sec1, textvariable=baud, values=['4800', '9600', '19200'], width='12').pack(side='left')

    bit = StringVar(root, "8")
    Label(sec2, text='位   长: ').pack(side='left')
    Combobox(sec2, textvariable=bit, values=['5', '7', '8'], width='12').pack(side='left')

    stop = StringVar(root, "1")
    Label(sec3, text='停止位: ').pack(side='left')
    Combobox(sec3, textvariable=bit, values=['1', '1.5', '2'], width='5').pack(side='left')

    inputbox = StringVar(root, '')
    Label(sec4, text='输   入: ',).pack(side='left')
    Entry(sec4, width=35, textvariable=inputbox).pack(side='left')

    Send = StringVar(root, '发送')
    Button(sec4, textvariable=Send, width=9, command=Submit).pack(side='left')



    isOpened = threading.Event()
root.mainloop()
