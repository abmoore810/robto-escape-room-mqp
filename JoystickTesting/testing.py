from __future__ import division
import time
import flask
from flask import Response
import threading
import atexit
import RobtoCamTest
# Import the PCA9685 module.
#import Adafruit_PCA9685 #--- add back in
from flask import Flask, render_template, request, send_from_directory
#import RPi.GPIO as GPIO #--- add back in
#testing file

pi_ip_address='localhost'#'130.215.9.186' #'0.0.0.0'#'192.168.0.32' # replace 192.168.0.107 with your Raspberry Pi IP address

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685() #--- add back in
#pwm.set_pwm_freq(60)#--- add back in



#TODO
#make robot keep checking its values for how to move. use python time???
#make it so that if it has not recieved anything from the html for a while, it stops moving

   
   
   
   
   
#  ___   ___  ___  _   _  ___   ___   ____ ___  ____  
# / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \ 
#| |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
# \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
#                  (____/ 
# Osoyoo Raspberry Pi Web Camera Control Robot Car
# tutorial url: https://osoyoo.com/?p=32066


from enum import Enum

class CamDirection(Enum):
    NONE = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class CarDirection(Enum):
    NONE = 0
    FORWARD = 1
    FOR_RIGHT = 2
    TURN_RIGHT = 3
    BACK_RIGHT = 4
    BACK = 5
    BACK_LEFT = 6
    TURN_LEFT = 7
    FOR_LEFT = 8
    
class Button(Enum):
    OFF = 0
    ON = 1

cam = RobtoCamTest.Camera()
#with this variable cam, can access the object's properties
    #in order to get the information from the vision processing code



#app = Flask(__name__) #keep commented


#GPIO.setmode(GPIO.BCM) # GPIO number  in BCM mode #--- add back in
#GPIO.setwarnings(False) #--- add back in
#define actuators GPIOs #--- add back in
#IN1 = 23 #--- add back in
#IN2 = 24 #--- add back in
#IN3 = 27 #--- add back in
#IN4 = 22 #--- add back in
#ENA = 0  #Right motor speed PCA9685 port 0 #--- add back in
#ENB = 1  #Left motor speed PCA9685 port 1 #--- add back in
#move_speed = 1800  # Max pulse length out of 4096 #--- add back in
#turn_speed = 1500 #--- add back in

servo_ctr = 320 #ultrasonic sensor facing front

# servo_rgt = 150 #ultrasonic sensor facing left
# servo_lft = 500 #ultrasonic sensor facing right


LRservo_cur = servo_ctr
UDservo_cur = servo_ctr
LRcam_servo = 15 #left/right camera servo
UDcam_servo = 14 #up/down camera servo

maxRight = 120
maxLeft = 550
maxUp = 190
maxDown = 424
step = 3#20

#initialize GPIO status variables
#IN1Sts = 0 #--- add back in
#IN2Sts = 0 #--- add back in
#ENASts = 0 #--- add back in
#IN3Sts = 0 #--- add back in
#IN4Sts = 0 #--- add back in
#ENBSts = 0 #--- add back in


        
        
def changespeed(speed):
    print("changeSpeed") #--- only for testing
    #pwm.set_pwm(ENB, 0, speed) #--- add back in
    #pwm.set_pwm(ENA, 0, int(speed*.95)) #--- add back in

# Define motor control  pins as output
# GPIO.setup(IN1, GPIO.OUT)    #--- add back in
# GPIO.setup(IN2, GPIO.OUT)  #--- add back in
# GPIO.setup(IN3, GPIO.OUT)    #--- add back in
# GPIO.setup(IN4, GPIO.OUT)  #--- add back in


#todo: make a hashmap/hashtable thing, for inputs from html file
#e.g.: "elif cmd=='back_right':", replace long "if else" statements like these


def stopcar():
    #print("stopping car")
    return #--- only for testing
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    changespeed(0)  

def backward():
    #print("going back")
    return #--- only for testing
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    changespeed(move_speed)
    
def forward():
    #print("going forward")
    return #--- only for testing
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    changespeed(move_speed)

def turnright():
    #print("turning right")
    return #--- only for testing
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    changespeed(turn_speed)
    
def turnleft():
    #print("turning left")
    return #--- only for testing
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    changespeed(turn_speed)
    
def turnCam():#camDir):
    #print("turning cam: " + str(camDir))
    return #--- only for testing
    global LRservo_cur, UDservo_cur
    #print(camDir)
    #if camDirX == CamDirection.NONE.value:
        
    #el
    if camDirX == CamDirection.RIGHT.value:
        LRservo_cur = LRservo_cur - step  #120
        print(LRservo_cur)
        if LRservo_cur <= maxRight:
            LRservo_cur = maxRight            
        pwm.set_pwm(LRcam_servo, 0, LRservo_cur)
    elif camDirX == CamDirection.LEFT.value:
        LRservo_cur = LRservo_cur + step #500
        print(LRservo_cur)
        if LRservo_cur >= maxLeft:
            LRservo_cur = maxLeft            
        pwm.set_pwm(LRcam_servo, 0, LRservo_cur)
    #el
    if camDirY == CamDirection.UP.value:
        UDservo_cur = UDservo_cur - step #120
        print(UDservo_cur)
        if UDservo_cur <= maxUp:
            UDservo_cur = maxUp            
        pwm.set_pwm(UDcam_servo, 0, UDservo_cur)
    elif camDirY == CamDirection.DOWN.value:
        UDservo_cur = UDservo_cur + step #500
        print(UDservo_cur)
        if UDservo_cur >= maxDown:
            UDservo_cur = maxDown            
        pwm.set_pwm(UDcam_servo, 0, UDservo_cur)
    # if camDir == CamDirection.NONE.value:
        # return
    # elif camDir == CamDirection.RIGHT.value:
        # LRservo_cur = LRservo_cur - step  #120
        # print(LRservo_cur)
        # if LRservo_cur <= maxRight:
            # LRservo_cur = maxRight            
        # pwm.set_pwm(LRcam_servo, 0, LRservo_cur)
    # elif camDir == CamDirection.LEFT.value:
        # LRservo_cur = LRservo_cur + step #500
        # print(LRservo_cur)
        # if LRservo_cur >= maxLeft:
            # LRservo_cur = maxLeft            
        # pwm.set_pwm(LRcam_servo, 0, LRservo_cur)
    # elif camDir == CamDirection.UP.value:
        # UDservo_cur = UDservo_cur - step #120
        # print(UDservo_cur)
        # if UDservo_cur <= maxUp:
            # UDservo_cur = maxUp            
        # pwm.set_pwm(UDcam_servo, 0, UDservo_cur)
    # elif camDir == CamDirection.DOWN.value:
        # UDservo_cur = UDservo_cur + step #500
        # print(UDservo_cur)
        # if UDservo_cur >= maxDown:
            # UDservo_cur = maxDown            
        # pwm.set_pwm(UDcam_servo, 0, UDservo_cur)
        

def centerCam():
    print("centering cam")
    return #--- only for testing
    global LRservo_cur, UDservo_cur
    LRservo_cur = servo_ctr
    UDservo_cur = servo_ctr 
    pwm.set_pwm(LRcam_servo, 0, LRservo_cur)
    pwm.set_pwm(UDcam_servo, 0, UDservo_cur)
    
#initialize robot
stopcar()
#pwm.set_pwm(LRcam_servo, 0, servo_ctr)#--- add back in
#pwm.set_pwm(UDcam_servo, 0, servo_ctr)#--- add back in
time.sleep(2)

running = True

carDir = CarDirection.NONE.value

camDirX = CamDirection.NONE.value
camDirY = CamDirection.NONE.value
cam_center = False
buttonVals = [0,0,0,0,0,0,0,0,0]
# forwards = 0
# backwards = 0
# left = 0
# right = 0


# camleft = 0
# camright = 0
# camup = 0
# camdown = 0
#camcenter = 0

def update(dt):
        #if python 3.10 or above, can use "match", works like switch statements 
        if carDir == CarDirection.NONE.value:
            stopcar()
        elif carDir == CarDirection.FORWARD.value:
            forward()
            #print("forward")
        elif carDir == CarDirection.BACK.value:
            backward()
            #print("backward")
        elif carDir == CarDirection.TURN_RIGHT.value:
            turnright()
           # print("turn right")
        elif carDir == CarDirection.TURN_LEFT.value:
            turnleft()
            #print("turn left")
        # elif carDir == CarDirection.FOR_LEFT.value:
            # #print("front left")
        # elif carDir == CarDirection.FOR_RIGHT.value:
            # #print("front right")
        # elif carDir == CarDirection.BACK_LEFT.value:
            # #print("back right")
        # elif carDir == CarDirection.BACK_RIGHT.value:
            #print("back right")
        #else:
            #print("carDir: " + str(carDir))
            #stopcar()
            
        if cam_center:
            centerCam()
        else:
            turnCam()
            # turnCam(camDirX)
            # turnCam(camDirY)
            # if camDirX == CamDirection.RIGHT.value:
# #             print(repr(CamDirection.RIGHT))
                # turnCam(CamDirection.RIGHT.value)
            # elif camDirX == CamDirection.LEFT.value:
    # #             print(repr(CamDirection.LEFT))
                # turnCam(CamDirection.LEFT.value)
            # if camDirY == CamDirection.UP.value:
    # #             print(repr(CamDirection.UP))
                # turnCam(CamDirection.UP.value)
            # elif camDirY == CamDirection.DOWN.value:
# #                 print(repr(CamDirection.DOWN))
                # turnCam(CamDirection.DOWN.value)
app = Flask(__name__, static_url_path='')


@app.route("/")
def hello():
   return render_template('testing.html')#render_template('testing.html')
   
@app.route("/data")
def recieve1():#buttonvals,moveAxesVal,camAxesVals):
    global carDir, camDirX, camDirY, buttonVals
    tempCar = int(request.args.get('car'))
    if(tempCar>=0 and tempCar <=8):#TODO check if valid
        carDir = tempCar
    #print(carDir)
    tempCams = request.args.get('cam')
    tempCamsX = int(tempCams[0])
    tempCamsY = int(tempCams[1])
    if(True): #TODO check if valid
        camDirX = tempCamsX
        camDirY = tempCamsY
    #print("X: " + str(tempCamsX) + ", Y: " + str(tempCamsY))
    
    tempButtons = request.args.get('buttons')
    if(len(tempButtons) == 9):
        for i in range(9):
            butVal = int(tempButtons[i])
            if(butVal == 0 or butVal == 1):
                buttonVals[i] = butVal
                #print(str(buttonVals[i]))
    #print("recieved")
    return render_template('testing.html')
    
@app.route("/<buttonvals>/<moveAxesVal>/<camAxesVals>")
def recieve(buttonvals,moveAxesVal,camAxesVals):
    #print("recieved")
    return render_template('testing.html')


#buttonvals will be 9 digits, either 0 or 1, in button order. 
    #nothing in between. eg "010101010"
    #can do a for loop, 0-9, take the value at each index of the string, 
    #then interpret each as an int and compare against current button values
    
#moveAxesVal is an int between 0-8, 
    #matches CarDirection enum

#camAxesVals is 2 ints, not separated by spaces,
    #first is x axis, either 0, 1, or 2.
    #second is y axis, either 0, 3, or 4.
    #matches CamDirection enum
    
    

#todo: interpret on this end (as well) if button is being pressed again, 
#or if just being held down 
#(when repeatedly sent the same button press without the button release in between; 
#just check if its already the val being sent)
#@app.route("/<action>/<cmd>")
#def action(action,cmd):
    return render_template('testing.html')
    global carDir
    if action=='camera':
    #with new implementation, simply set camDirX to enum of direction of camAxesX,
        #and the same with camDirY and camAxesY
        if cmd=='forward':
            camDirX = CamDirection.NONE.value
            camDirY = CamDirection.UP.value
        elif cmd=='for_right':
            camDirX = CamDirection.RIGHT.value
            camDirY = CamDirection.UP.value
        elif cmd=='right':
            camDirX = CamDirection.RIGHT.value
            camDirY = CamDirection.NONE.value
        elif cmd=='back_right':
            camDirX = CamDirection.RIGHT.value
            camDirY = CamDirection.DOWN.value
        elif cmd=='back':
            camDirX = CamDirection.NONE.value
            camDirY = CamDirection.DOWN.value
        elif cmd=='back_left':
            camDirX = CamDirection.LEFT.value
            camDirY = CamDirection.DOWN.value
        elif cmd=='left':
            camDirX = CamDirection.LEFT.value
            camDirY = CamDirection.NONE.value
        elif cmd=='for_left':
            camDirX = CamDirection.LEFT.value
            camDirY = CamDirection.UP.value
        elif cmd== 'center':
            camDirX = CamDirection.NONE.value
            camDirY = CamDirection.NONE.value
        else:
            print("Camera, invalid value")
            
            
        # if cmd == 'right':
            # camDirX = CamDirection.RIGHT.value
        # elif cmd == 'left':
            # camDirX = CamDirection.LEFT.value
        # elif cmd == 'centerX':
            # camDirX = CamDirection.NONE.value
        # elif cmd == 'up':
            # camDirY = CamDirection.UP.value
        # elif cmd == 'down':
            # camDirY = CamDirection.DOWN.value
        # elif cmd == 'centerY':
            # camDirY = CamDirection.NONE.value
        # else:
            # print("camera, invalid value")
          
    elif action=='move':
        if cmd=='forward':
            carDir = CarDirection.FORWARD.value
            #print("forward")
        elif cmd=='for_right':
            carDir = CarDirection.FOR_RIGHT.value
            #print("for_right")
        elif cmd=='right':
            carDir = CarDirection.TURN_RIGHT.value
            #print("right")
        elif cmd=='back_right':
            carDir = CarDirection.BACK_RIGHT.value
            #print("back_right")
        elif cmd=='back':
            carDir = CarDirection.BACK.value
            #print("back")
        elif cmd=='back_left':
            carDir = CarDirection.BACK_LEFT.value
            #print("back_left")
        elif cmd=='left':
            carDir = CarDirection.TURN_LEFT.value
            #print("left")
        elif cmd=='for_left':
            carDir = CarDirection.FOR_LEFT.value
            #print("for_left")             
        elif cmd== 'center':
            carDir = CarDirection.NONE.value
            #print("center, no movement")
        else:
            print("move")
    elif action=='speed':
        if cmd=='high':
            print("speed changed to 75")
        elif cmd=='regular':
            print("speed changed to 50")
        elif cmd=='low':
            print("speed changed to 25")
        elif cmd=='zero':
            print("speed changed to 0")
        else:
            print("speed changed")
    else:
        print("action: " + action + "cmd: " + cmd)

    return render_template('testing.html')#render_template('testing.html')
    
    
@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(cam.start(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        
        
# def hello(self):
    # print("hello, Timer")
    # t = threading.Timer(3.0, hello)
    # t.start()
class MyThread(threading.Thread):
    #count = 0
    def __init__(self, event):
        global count
        threading.Thread.__init__(self)
        self.stopped = event
        #count = 0


    def run(self):
        #global count, e
        old_time = time.time()
        while not self.stopped.wait(.01):
            dt = time.time()-old_time
            update(dt)
            old_time = time.time()
            #time.sleep(.5)
            #count = count+1
           # print("my thread" + str(count))
            #if(count >10):
                #return
            
            # call a function
    
# class MyThread2(threading.Thread):
    # count = 0
    # def __init__(self, event):
        # global count
        # threading.Thread.__init__(self)
        # self.stopped = event
        # count = 0


    # def run(self):
        # global count, e
        # while True: #not self.stopped:
            # time.sleep(.5)
            # count = count+1
            # print("my thread" + str(count))
            # #if(count >10):
                # #return
            
            # # call a function

# def closeThreads():
    # global stopFlag
    # print("closing time")
    # stopFlag.set()
    
if __name__ == "__main__":
    stopFlag = threading.Event()
    thread = MyThread(stopFlag)
    thread.daemon=True
    thread.start()
    
    
    # t = threading.Timer(3.0, hello)
    # t.start()
    print("hello!!")
    #atexit.register(closeThreads)
    app.run(host=pi_ip_address, port=8000, debug=False)#set debug off??
    # counter = 0
    # while(True):
        # counter = counter+1
        # print(str(counter))
        # time.sleep(.5)
 
 

#In the code that started the timer, you can then set the stopped event to stop the timer.

# stopFlag = Event()
# thread = MyThread(stopFlag)
# thread.start()
# # this will stop the timer
# stopFlag.set()
   
#def repUpdate():
 #   i = 29
  #  while(running):
   #     i = i+1
    #    if i==30:
     #       i = 0
      #      update(.01)
#try:              
 #       pyglet.clock.schedule_interval(update, 0.01)
  #      pyglet.app.run()

#finally:
    #print("ending")
   # pwm.set_pwm(LRcam_servo, 0, servo_ctr)
    #pwm.set_pwm(UDcam_servo, 0, servo_ctr)
    #GPIO.cleanup()