# Tkinter and GPIO together 
# With class structure.
from gpiozero import LED
from Tkinter import *
import RPi.GPIO as GPIO
import time
import serial
import usb.core
import usb.util
import sensors


class MyApp(Frame):

    def __init__ (self, parent):

        self.myParent = parent
        self.myframe = Frame(parent)

        self.ser = serial.Serial('/dev/tnt1')  # open serial port
        self.ptt = LED(12)
 
        # Set up the frame geometry padding. 
        self.myframe.pack(padx="2m",pady="1m",ipadx="2m",ipady="1m")

        # Invoke the pseudo LED and control its colour based on GPIO pin 23
        colour = "green"
        self.canvas1 = Canvas(self.myframe, height=25, width=25)
        self.label = Label(self.myframe, text='PTT')
        self.led = self.canvas1.create_oval(5,5,20,20, fill=colour)
        self.label.pack(side=LEFT)
        self.canvas1.pack(side=LEFT)
        self.label2 = Label(self.myframe, text='SWR')
        self.swr = Label(self.myframe, text='1.1')
        self.label2.pack(side=LEFT)
        self.swr.pack(side=LEFT)
        self.update()

    def update(self):
        if self.ser.cts:
            self.ptt.on()
            colour = "red"
        else:
            self.ptt.off()
            colour = "green"

        sensors.init()
        in6=0
        in7=0
        swr=1
        try:
            for chip in sensors.iter_detected_chips():
                #print ('%s at %s' % (chip, chip.adapter_name))
                for feature in chip:
                    if feature.label == 'in6':
                        in6=feature.get_value()
                    if feature.label == 'in7':
                        in7=feature.get_value()
            #print ("in6",in6)
            #print ("in7",in7)
            if (in6 > 0 and in7 > 0  and in6 > in7) :
                fact = in7/in6
                if fact <> 1: 
                    swr = (1+fact)/(1-fact)
                    #print ("swr",swr)
                    self.swr['text']="1:{:.2f}   ".format(swr)
            else:
                   #if (in6 <=0 and in7<=0):
                   swr=1;
                   self.swr['text']="1:{:.2f}   ".format(swr)
        finally:
            sensors.cleanup()
            
            
        self.canvas1.itemconfig(self.led, fill=colour)
        self.myParent.timer = self.myParent.after(100,self.update)


# Main loop Tk link and class stuff.
root = Tk()
root.title("PTT/SWR")
myapp = MyApp(root)
root.mainloop()
