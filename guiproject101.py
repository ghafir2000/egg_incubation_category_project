from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import serial
import cv2
import os
from one_egg_sample import take_one_photo_and_predict
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from command import ArduinoCommand 
from time import sleep, strftime
from holders import egg_holder
from move_eggs import hatch, move_egg_out
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #  refresh_window
         self.update_timer = QTimer()
         self.update_timer.timeout.connect(self.refresh_window)
         self.update_timer.start(100)
         self.time_left2 = 20 * 60 
         self.time_left6 = 60 * 60 
         self.label_arm_value = 0
         self.label_camera_value = 0
         self.cap = cv2.VideoCapture('path_to_your_video.mp4')
         

    
         MainWindow.setObjectName("MainWindow")
         MainWindow.resize(695, 402)
         self.centralwidget = QtWidgets.QWidget(MainWindow)
         self.centralwidget.setObjectName("centralwidget")
         self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
         self.tabWidget.setGeometry(QtCore.QRect(0, 0, 701, 371))
         font = QtGui.QFont()
         font.setPointSize(11)
         self.tabWidget.setFont(font)
         self.tabWidget.setObjectName("tabWidget")
         self.tab = QtWidgets.QWidget()
         self.tab.setObjectName("tab")

        #   label of tab1
         self.label1 = QtWidgets.QLabel(self.tab)
         self.label1.setGeometry(QtCore.QRect(0, 0, 691, 341))
         self.label1.setText("")
         self.label1.setPixmap(QtGui.QPixmap("photo1.jpeg"))
         self.label1.setScaledContents(True)
         self.label1.setObjectName("label1")

            #  label read Temperature of incubator
         self.temp_incubator = QtWidgets.QLabel(self.tab)
         self.temp_incubator.setGeometry(QtCore.QRect(10, 50, 401, 41))
         self.temp_incubator.setStyleSheet('background: white; color: black;') 
         self.temp_incubator.setFrameShape(QtWidgets.QFrame.StyledPanel)
         font = QtGui.QFont()
         font.setPointSize(18)
         self.temp_incubator.setFont(font)
         self.temp_incubator.setObjectName("temp_incubator")

            #  label read Humidity of incubat
         self.hum_incubator = QtWidgets.QLabel(self.tab)
         self.hum_incubator.setGeometry(QtCore.QRect(10, 120, 401, 41))
         self.hum_incubator.setStyleSheet("background-color: white; color: black;") 
         self.hum_incubator.setFrameShape(QtWidgets.QFrame.StyledPanel)
         font = QtGui.QFont()
         font.setPointSize(18)
         self.hum_incubator.setFont(font)
         self.hum_incubator.setObjectName("temp_incubator")
         
         self.Egg1= QtWidgets.QPushButton("Toggle", self.tab, clicked =  lambda : self.check_egg_state(Egg_1_state))
         self.Egg1.setGeometry(QtCore.QRect(10, 170, 20, 40))
         self.Egg1.setFont(font)
         self.Egg1.setObjectName("Egg1")
         
         
         self.Egg2= QtWidgets.QPushButton("Toggle", self.tab, clicked =  lambda : self.check_egg_state(Egg_2_state))
         self.Egg2.setGeometry(QtCore.QRect(40, 170, 20, 40))
         self.Egg2.setFont(font)
         self.Egg2.setObjectName("Egg2")
         
         self.Egg3= QtWidgets.QPushButton("Toggle", self.tab, clicked =  lambda : self.check_egg_state(Egg_3_state))
         self.Egg3.setGeometry(QtCore.QRect(70, 170, 20, 40))
         self.Egg3.setFont(font)
         self.Egg3.setObjectName("Egg3")
         
         self.Egg4= QtWidgets.QPushButton("Toggle", self.tab, clicked =  lambda : self.check_egg_state(Egg_4_state))
         self.Egg4.setGeometry(QtCore.QRect(100, 170, 20, 40))
         self.Egg4.setFont(font)
         self.Egg4.setObjectName("Egg4")
         
         self.Egg5= QtWidgets.QPushButton("Toggle", self.tab, clicked =  lambda : self.check_egg_state(Egg_5_state))
         self.Egg5.setGeometry(QtCore.QRect(130, 170, 20, 40))
         self.Egg5.setFont(font)
         self.Egg5.setObjectName("Egg5")
         
         self.Egg6= QtWidgets.QPushButton("Toggle", self.tab, clicked =  lambda : self.check_egg_state(Egg_6_state))
         self.Egg6.setGeometry(QtCore.QRect(160, 170, 20, 40))
         self.Egg6.setFont(font)
         self.Egg6.setObjectName("Egg6")
        
         self.Egg7= QtWidgets.QPushButton("Toggle", self.tab ,clicked =  lambda : self.check_egg_state(Egg_7_state))
         self.Egg7.setGeometry(QtCore.QRect(190, 170, 20, 40))
         self.Egg7.setFont(font)
         self.Egg7.setObjectName("Egg7")
         
         self.Egg8= QtWidgets.QPushButton("Toggle", self.tab ,clicked =  lambda : self.check_egg_state(Egg_8_state))
         self.Egg8.setGeometry(QtCore.QRect(220, 170, 20, 40))
         self.Egg8.setFont(font)
         self.Egg8.setObjectName("Egg8")

         self.Egg9= QtWidgets.QPushButton("Toggle", self.tab ,clicked =  lambda : self.check_egg_state(Egg_9_state))
         self.Egg9.setGeometry(QtCore.QRect(250, 170, 20, 40))
         self.Egg9.setFont(font)
         self.Egg9.setObjectName("Egg9")
         
         self.label_date = QtWidgets.QLabel(self.tab)
         self.label_date.setGeometry(QtCore.QRect(435, 10, 235, 41))
         self.label_date.setStyleSheet(" color: white;") 
         self.label_date.setFrameShape(QtWidgets.QFrame.StyledPanel)
         font = QtGui.QFont()
         font.setPointSize(18)
         self.label_date.setFont(font)
         self.label_date.setObjectName("label_date")


         self.auto= QtWidgets.QPushButton("Toggle", self.tab)
         self.auto.setGeometry(QtCore.QRect(550, 200, 101, 51))
         font = QtGui.QFont()
         self.auto.setCheckable(True)
         font.setPointSize(16)
         self.auto.setFont(font)
         self.auto.setObjectName("auto")

         
         self.off = QtWidgets.QPushButton(self.tab,clicked = lambda : self.shutdown() )
         self.off.setGeometry(QtCore.QRect(550, 270, 101, 51))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.off.setFont(font)
         self.off.setObjectName("off")

        #    label of tab2
         self.tabWidget.addTab(self.tab, "")
         self.tab_2 = QtWidgets.QWidget()
         self.tab_2.setObjectName("tab_2")


         self.emerg_incubator = QtWidgets.QPushButton(self.tab,clicked = lambda : self.EMERGENCY())
         self.emerg_incubator.setGeometry(QtCore.QRect(20, 270, 111, 51))
         font.setPointSize(13)
         self.emerg_incubator.setFont(font)
         self.emerg_incubator.setStyleSheet('background-color : red; color : red;')  
         self.emerg_incubator.setObjectName("emerg_incubator")
         self.emerg_incubator.setText("Emergency")




         self.label2 = QtWidgets.QLabel(self.tab_2)
         self.label2.setGeometry(QtCore.QRect(0, 0, 691, 341))
         self.label2.setText("")
         self.label2.setPixmap(QtGui.QPixmap("photo1.jpeg"))
         self.label2.setScaledContents(True)
         self.label2.setObjectName("label2")

        #  label read Temperature of hatcher
         self.temp_hatcher = QtWidgets.QLabel(self.tab_2)
         self.temp_hatcher.setGeometry(QtCore.QRect(10, 50, 401, 41))
         font = QtGui.QFont()
         self.temp_hatcher.setStyleSheet("background-color: white; color: black;") 
         self.temp_hatcher.setFrameShape(QtWidgets.QFrame.StyledPanel)
         font.setPointSize(18)
         self.temp_hatcher.setFont(font)
         self.temp_hatcher.setObjectName("temp_hatcher")

        #   label read Humidity of hatcher
         self.hum_hatcher = QtWidgets.QLabel(self.tab_2)
         self.hum_hatcher.setGeometry(QtCore.QRect(10, 120, 401, 41))
         font = QtGui.QFont() 
         self.hum_hatcher.setStyleSheet("background-color: white; color: black;") 
         self.hum_hatcher.setFrameShape(QtWidgets.QFrame.StyledPanel)
         font.setPointSize(18)
         self.hum_hatcher.setFont(font)
         self.hum_hatcher.setObjectName("hum_hatcher")


       
         self.emerg_hatcher = QtWidgets.QPushButton(self.tab_2,clicked = lambda : self.EMERGENCY())
         self.emerg_hatcher.setGeometry(QtCore.QRect(20, 270, 111, 51))
         font.setPointSize(13)
         self.emerg_hatcher.setFont(font)
         self.emerg_hatcher.setStyleSheet("background-color: red; color: red;")  
         self.emerg_hatcher.setObjectName("emerg_incubator")
         self.emerg_hatcher.setText("Emergency")

         

            # label of tab3
         self.tabWidget.addTab(self.tab_2, "")
         self.tab_3 = QtWidgets.QWidget()
         self.tab_3.setObjectName("tab_3")


         self.label3 = QtWidgets.QLabel(self.tab_3)
         self.label3.setGeometry(QtCore.QRect(0, 0, 691, 341))
         self.label3.setText("")
         self.label3.setPixmap(QtGui.QPixmap("photo1.jpeg"))
         self.label3.setScaledContents(True)
         self.label3.setObjectName("label3")
        
         self.emerg_arm  = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.EMERGENCY())
         self.emerg_arm.setGeometry(QtCore.QRect(20, 270, 111, 51))
         font.setPointSize(13)
         self.emerg_arm.setFont(font)
         self.emerg_arm.setStyleSheet("background-color: red; color: red;")  
         self.emerg_arm.setObjectName("emerg_incubator")
         self.emerg_arm.setText("Emergency")


            #  Button to stop arm
         self.Stop_arm = QtWidgets.QPushButton(self.tab_3,clicked = lambda :move_arduino.my_serial_write("arm_stop"))
         self.Stop_arm.setGeometry(QtCore.QRect(80, 140, 121, 41))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.Stop_arm.setFont(font)
         self.Stop_arm.setObjectName("Stop_arm")

           
            #  Button to up arm
         self.UP_arm = QtWidgets.QPushButton(self.tab_3 ,clicked =  lambda : move_arduino.my_serial_write("arm_verti_stepper_0"))
         self.UP_arm.setGeometry(QtCore.QRect(0, 70, 131, 41))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.UP_arm.setFont(font)
         self.UP_arm.setObjectName("UP_arm")

        #   Button to down arm
         self.DOWN_arm = QtWidgets.QPushButton(self.tab_3 ,clicked =  lambda : move_arduino.my_serial_write("arm_verti_stepper_1"))
         self.DOWN_arm.setGeometry(QtCore.QRect(170, 70, 121, 41))
         self.DOWN_arm.setObjectName("DOWN_arm")

        #   Keyboard of arm
         self.number_1 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("1"))
         self.number_1.setGeometry(QtCore.QRect(460, 100, 51, 31))
         self.number_1.setObjectName("number_1")
         self.number_2 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("2"))
         self.number_2.setGeometry(QtCore.QRect(520, 100, 51, 31))
         self.number_2.setObjectName("number_2")
         self.number_3 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("3"))
         self.number_3.setGeometry(QtCore.QRect(580, 100, 51, 31))
         self.number_3.setObjectName("number_3")
         self.number_5 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("5"))
         self.number_5.setGeometry(QtCore.QRect(520, 140, 51, 31))
         self.number_5.setObjectName("number_5")
         self.number_6 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("6"))
         self.number_6.setGeometry(QtCore.QRect(580, 140, 51, 31))
         self.number_6.setObjectName("number_6")
         self.number_4 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("4"))
         self.number_4.setGeometry(QtCore.QRect(460, 140, 51, 31))
         self.number_4.setObjectName("number_4")
         self.number_9 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("9"))
         self.number_9.setGeometry(QtCore.QRect(580, 180, 51, 31))
         self.number_9.setObjectName("number_9")
         self.number_8 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("8"))
         self.number_8.setGeometry(QtCore.QRect(520, 180, 51, 31))
         self.number_8.setObjectName("number_8")
         self.number_7 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("7"))
         self.number_7.setGeometry(QtCore.QRect(460, 180, 51, 31))
         self.number_7.setObjectName("number_7")
         self.number_0 = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("0"))
         self.number_0.setGeometry(QtCore.QRect(580, 220, 51, 31))
         self.number_0.setObjectName("number_0")

            # label to store value Keyboard the arm
         self.outputarmLabel = QtWidgets.QLabel(self.tab_3)
         self.outputarmLabel.setGeometry(QtCore.QRect(460, 40, 171, 51))
         self.outputarmLabel.setStyleSheet("background-color: white; color: black;") 
         label_arm_value = self.outputarmLabel.text()
         font = QtGui.QFont()
         font.setPointSize(13)
         self.outputarmLabel.setFont(font)
         self.outputarmLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
         self.outputarmLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
         self.outputarmLabel.setObjectName("outputarmLabel")

        #   Button to move the arm
         
         self.accept_arm = QtWidgets.QPushButton(self.tab_3 ,clicked =  lambda : (move_arduino.my_serial_write(f"arm_hori_stepper_{self.label_arm_value}"),self.press_it("clear")))
         self.accept_arm.setGeometry(QtCore.QRect(500, 270, 101, 41))
         self.accept_arm.setObjectName("accept_arm")

         self.clear_arm = QtWidgets.QPushButton(self.tab_3,clicked = lambda : self.press_it("clear"))
         self.clear_arm.setGeometry(QtCore.QRect(460, 220, 111, 31))
         self.clear_arm.setObjectName("clear_arm")


         self.vacume = QtWidgets.QPushButton("Toggle",self.tab_3,clicked =  lambda :self.check_vacume())
         self.vacume.setGeometry(QtCore.QRect(270, 200, 101, 41))
         font = QtGui.QFont()
         self.vacume.setCheckable(True)
         font.setPointSize(14)
         self.vacume.setFont(font)
         self.vacume.setObjectName("vacume")  


         self.solenoid = QtWidgets.QPushButton("Toggle",self.tab_3,clicked =  lambda : self.check_selenoid())
         self.solenoid.setGeometry(QtCore.QRect(270, 260, 101, 41))
         font = QtGui.QFont()
         self.solenoid.setCheckable(True)

         font.setPointSize(14)
         self.solenoid.setFont(font)
         self.solenoid.setObjectName("solenoid")



         self.tabWidget.addTab(self.tab_3, "")
         self.camera = QtWidgets.QWidget()
         self.camera.setObjectName("camera")


         self.label4 = QtWidgets.QLabel(self.camera)
         self.label4.setGeometry(QtCore.QRect(0, 0, 691, 341))
         self.label4.setText("")
         self.label4.setPixmap(QtGui.QPixmap("photo1.jpeg"))
         self.label4.setScaledContents(True)
         self.label4.setObjectName("label4")

         self.UP_camera = QtWidgets.QPushButton(self.camera,clicked = lambda : move_arduino.my_serial_write("leds_stepper_1"))
         self.UP_camera.setGeometry(QtCore.QRect(10, 80, 121, 41))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.UP_camera.setFont(font)
         self.UP_camera.setObjectName("UP_camera")


         self.DOWN_camera = QtWidgets.QPushButton(self.camera,clicked = lambda : move_arduino.my_serial_write("leds_stepper_0"))
         self.DOWN_camera.setGeometry(QtCore.QRect(160, 80, 121, 41))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.DOWN_camera.setFont(font)
         self.DOWN_camera.setObjectName("DOWN_camera")





         self.camera_camera = QtWidgets.QPushButton(self.camera,clicked = lambda : self.take_photo())
         self.camera_camera.setGeometry(QtCore.QRect(90, 140, 121, 41))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.camera_camera.setFont(font)
         self.camera_camera.setObjectName("camera_camera")

         
         self.emerg_camera= QtWidgets.QPushButton(self.camera,clicked = lambda : self.EMERGENCY())
         self.emerg_camera .setGeometry(QtCore.QRect(20, 270, 111, 51))
         font.setPointSize(13)
         self.emerg_camera.setFont(font)
         self.emerg_camera.setStyleSheet("background-color: red; color: red;")  
         self.emerg_camera.setObjectName("emerg_incubator")
         self.emerg_camera.setText("Emergency")


         self.outputcameraLabel = QtWidgets.QLabel(self.camera)
         self.outputcameraLabel.setGeometry(QtCore.QRect(460, 20, 171, 51))
         label_camera_value = self.outputcameraLabel.text()
         font = QtGui.QFont()
         font.setPointSize(13)
         self.outputcameraLabel.setFont(font)
         self.outputcameraLabel.setStyleSheet("background-color: white; color: black;") 
         self.outputcameraLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
         self.outputcameraLabel.setFrameShadow(QtWidgets.QFrame.Plain)
         self.outputcameraLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
         self.outputcameraLabel.setObjectName("outputcameraLabel")



         self.number_1c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("1"))
         self.number_1c.setGeometry(QtCore.QRect(460, 80, 51, 31))
         self.number_1c.setObjectName("number_1c")
         self.number_2c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("2"))
         self.number_2c.setGeometry(QtCore.QRect(520, 80, 51, 31))
         self.number_2c.setObjectName("number_2c")
         self.number_3c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("3"))
         self.number_3c.setGeometry(QtCore.QRect(580, 80, 51, 31))
         self.number_3c.setObjectName("number_3c")
         self.number_4c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("4"))
         self.number_4c.setGeometry(QtCore.QRect(460, 120, 51, 31))
         self.number_4c.setObjectName("number_4c")
         self.number_5c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("5"))
         self.number_5c.setGeometry(QtCore.QRect(520, 120, 51, 31))
         self.number_5c.setObjectName("number_5c")
         self.number_6c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("6"))
         self.number_6c.setGeometry(QtCore.QRect(580, 120, 51, 31))
         self.number_6c.setObjectName("number_6c")
         self.number_7c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("7"))
         self.number_7c.setGeometry(QtCore.QRect(460, 160, 51, 31))
         self.number_7c.setObjectName("number_7c")
         self.number_8c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("8"))
         self.number_8c.setGeometry(QtCore.QRect(520, 160, 51, 31))
         self.number_8c.setObjectName("number_8c")
         self.number_9c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("9"))
         self.number_9c.setGeometry(QtCore.QRect(580, 160, 51, 31))
         self.number_9c.setObjectName("number_9c")
         self.number_0c = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("0"))
         self.number_0c.setGeometry(QtCore.QRect(580, 200, 51, 31))
         self.number_0c.setObjectName("number_0c")


         self.Accepy_camera = QtWidgets.QPushButton(self.camera,clicked =  lambda : (move_arduino.my_serial_write(f"camera_stepper_{self.label_camera_value}"),self.select("clear")))
         self.Accepy_camera.setGeometry(QtCore.QRect(490, 260, 101, 41))
         self.Accepy_camera.setObjectName("Accepy_camera")

         self.clear_camera = QtWidgets.QPushButton(self.camera,clicked = lambda : self.select("clear"))
         self.clear_camera.setGeometry(QtCore.QRect(460, 200, 111, 31))
         self.clear_camera.setObjectName("clear_camera")
         
         self.pred_label = QtWidgets.QLabel(self.camera)
         self.pred_label.setGeometry(QtCore.QRect(240, 140, 191, 181))
         self.pred_label.setText("")
         self.pred_label.setPixmap(QtGui.QPixmap("photo_2024-07-29_14-39-59.jpg"))
         self.pred_label.setScaledContents(True)
         self.pred_label.setObjectName("pred_label")


         self.tabWidget.addTab(self.camera, "")
         self.tab_4 = QtWidgets.QWidget()
         self.tab_4.setObjectName("tab_4")

         
         self.label5 = QtWidgets.QLabel(self.tab_4)
         self.label5.setGeometry(QtCore.QRect(0, 0, 691, 341))
         self.label5.setText("")
         self.label5.setPixmap(QtGui.QPixmap("photo1.jpeg"))
         self.label5.setScaledContents(True)
         self.label5.setObjectName("label5")

         self.open = QtWidgets.QPushButton(self.tab_4,clicked =  lambda : env_arduino.my_serial_write("wins_up"))
         self.open.setGeometry(QtCore.QRect(10, 40, 111, 51))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.open.setFont(font)
         self.open.setObjectName("open")


         self.Close = QtWidgets.QPushButton(self.tab_4,clicked =  lambda : env_arduino.my_serial_write("wins_down"))
         self.Close.setGeometry(QtCore.QRect(10, 110, 111, 51))
         font = QtGui.QFont()
         font.setPointSize(16)
         self.Close.setFont(font)
         self.Close.setObjectName("Close")

         self.emerg_warning = QtWidgets.QPushButton(self.tab_4,clicked = lambda : self.EMERGENCY())
         self.emerg_warning  .setGeometry(QtCore.QRect(20, 270, 111, 51))
         font.setPointSize(13)
         self.emerg_warning .setFont(font)
         self.emerg_warning .setStyleSheet("background: red; color: red;") 
         self.emerg_warning .setObjectName("emerg_incubator")
         self.emerg_warning .setText("Emergency")


         self.tm2 = QtWidgets.QLabel(self.tab_4)
         self.tm2.setGeometry(QtCore.QRect(340, 10, 331, 41))
         self.tm2 .setStyleSheet("background: white; color: black;") 
         self.tm2 .setFont(font)
         self.tm2.setFrameShape(QtWidgets.QFrame.StyledPanel)
         self.tm2.setObjectName("tm2")
        


         self.tm6 = QtWidgets.QLabel(self.tab_4)
         self.tm6.setGeometry(QtCore.QRect(340, 80, 331, 41))
         self.tm6 .setStyleSheet("background: white; color: black;") 
         self.tm6 .setFont(font)
         self.tm6.setFrameShape(QtWidgets.QFrame.StyledPanel)
         self.tm6.setObjectName("tm6") 


         self.in3days = QtWidgets.QLabel(self.tab_4)
         self.in3days.setGeometry(QtCore.QRect(340, 150, 331, 41))
         self.in3days.setFrameShape(QtWidgets.QFrame.StyledPanel)
         self.in3days.setStyleSheet("background: white; color: black;") 
         self.in3days.setObjectName("in3days")
         self.in3days .setFont(font)



         self.in18days = QtWidgets.QLabel(self.tab_4)
         self.in18days.setGeometry(QtCore.QRect(340, 210, 331, 41))
         self.in18days.setFrameShape(QtWidgets.QFrame.StyledPanel)
         self.in18days.setFont(font)
         self.in18days .setStyleSheet("background: white; color: black;") 
         self.in18days.setObjectName("in18days")


         self.hatcher = QtWidgets.QLabel(self.tab_4)
         self.hatcher.setGeometry(QtCore.QRect(340, 280, 331, 41))
         self.hatcher.setFrameShape(QtWidgets.QFrame.StyledPanel)
         self.hatcher.setStyleSheet("background: white; color: black;") 
         self.hatcher.setFont(font)

         self.hatcher.setObjectName("hatcher")


         self.tabWidget.addTab(self.tab_4, "")
         MainWindow.setCentralWidget(self.centralwidget)
         self.menubar = QtWidgets.QMenuBar(MainWindow)
         self.menubar.setGeometry(QtCore.QRect(0, 0, 695, 22))
         self.menubar.setObjectName("menubar")
         MainWindow.setMenuBar(self.menubar)
         self.statusbar = QtWidgets.QStatusBar(MainWindow)
         self.statusbar.setObjectName("statusbar")
         MainWindow.setStatusBar(self.statusbar) 

         self.retranslateUi(MainWindow)
         self.tabWidget.setCurrentIndex(0)
         QtCore.QMetaObject.connectSlotsByName(MainWindow)
         
    def take_photo(self):
        move_arduino.my_serial_write("LED_1")
        take_one_photo_and_predict() 
        move_arduino.my_serial_write("LED_0")
        self.pred_label.setPixmap(QtGui.QPixmap("output_of_0_.jpg"))


    def press_it(self,pressed):
          if pressed == "clear":
              self.outputarmLabel.setText("0")
          else:
              if self.outputarmLabel.text() =="0":
                  self.outputarmLabel.setText("")
              self.outputarmLabel.setText(f'{self.outputarmLabel.text()}{pressed}')
              self.label_arm_value = self.outputarmLabel.text()



    def select(self,selected):
          if selected == "clear":
              self.outputcameraLabel.setText("0")
          else:
              if self.outputcameraLabel.text() =="0":
                  self.outputcameraLabel.setText("")
              self.outputcameraLabel.setText(f'{self.outputcameraLabel.text()}{selected}')
              self.label_camera_value = self.outputcameraLabel.text()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "chick-in"))
        self.temp_hatcher.setText(_translate("MainWindow", "Temperature:"))
        self.hum_hatcher.setText(_translate("MainWindow", "Humidity:"))
        self.off.setText(_translate("MainWindow", "OFF"))
        self.emerg_hatcher.setText(_translate("MainWindow", "Emergancy"))
        self.label_date.setText(_translate("MainWindow", "Date"))

        self.auto.setText(_translate("MainWindow", "Auto"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Control of the incubator "))
        self.temp_incubator.setText(_translate("MainWindow", "Temperature:"))
        self.hum_incubator.setText(_translate("MainWindow", "Humidity:"))
        self.Egg1.setText(_translate("MainWindow", "E1"))
        self.Egg2.setText(_translate("MainWindow", "E2"))
        self.Egg3.setText(_translate("MainWindow", "E3"))
        self.Egg4.setText(_translate("MainWindow", "E4"))
        self.Egg5.setText(_translate("MainWindow", "E5"))
        self.Egg6.setText(_translate("MainWindow", "E6"))
        self.Egg7.setText(_translate("MainWindow", "E7"))
        self.Egg8.setText(_translate("MainWindow", "E8"))
        self.Egg9.setText(_translate("MainWindow", "E9"))
        
        self.emerg_incubator.setText(_translate("MainWindow", "Emergancy"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Control of the hatcher"))
        self.emerg_arm.setText(_translate("MainWindow", "Emergancy"))
        self.Stop_arm.setText(_translate("MainWindow", "Stop"))
        self.UP_arm.setText(_translate("MainWindow", "UP"))
        self.DOWN_arm.setText(_translate("MainWindow", "DOWN"))
        self.number_1.setText(_translate("MainWindow", "1"))
        self.number_2.setText(_translate("MainWindow", "2"))
        self.number_3.setText(_translate("MainWindow", "3"))
        self.number_5.setText(_translate("MainWindow", "5"))
        self.number_6.setText(_translate("MainWindow", "6"))
        self.number_4.setText(_translate("MainWindow", "4"))
        self.number_9.setText(_translate("MainWindow", "9"))
        self.number_8.setText(_translate("MainWindow", "8"))
        self.number_7.setText(_translate("MainWindow", "7"))
        self.number_0.setText(_translate("MainWindow", "0"))
        self.accept_arm.setText(_translate("MainWindow", "Accept"))
        self.outputarmLabel.setText(_translate("MainWindow", "0"))
        self.clear_arm.setText(_translate("MainWindow", "clear"))
        self.vacume.setText(_translate("MainWindow", "vacume"))
        self.solenoid.setText(_translate("MainWindow", "solenoid"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Control of the arm"))
        self.UP_camera.setText(_translate("MainWindow", "UP"))
        self.DOWN_camera.setText(_translate("MainWindow", "DOWN"))
        self.camera_camera.setText(_translate("MainWindow", "Camera"))
        self.emerg_camera.setText(_translate("MainWindow", "Emergancy"))
        self.outputcameraLabel.setText(_translate("MainWindow", "0"))
        self.number_1c.setText(_translate("MainWindow", "1"))
        self.number_2c.setText(_translate("MainWindow", "2"))
        self.number_3c.setText(_translate("MainWindow", "3"))
        self.number_4c.setText(_translate("MainWindow", "4"))
        self.number_5c.setText(_translate("MainWindow", "5"))
        self.number_6c.setText(_translate("MainWindow", "6"))
        self.number_7c.setText(_translate("MainWindow", "7"))
        self.number_8c.setText(_translate("MainWindow", "8"))
        self.number_9c.setText(_translate("MainWindow", "9"))
        self.number_0c.setText(_translate("MainWindow", "0"))
        self.Accepy_camera.setText(_translate("MainWindow", "Accept"))
        self.clear_camera.setText(_translate("MainWindow", "clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.camera), _translate("MainWindow", "camera"))
        self.open.setText(_translate("MainWindow", "Open_wins"))
        self.Close.setText(_translate("MainWindow", "Close_wins"))
        self.emerg_warning.setText(_translate("MainWindow", "Emergancy"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Warnings"))



    
    def hat_refresh(self):
        if env_arduino.hat_tem > 0 :
            
            self.temp_hatcher.setText("the temperature is  "+str(env_arduino.hat_tem))
            if 37.8 >= env_arduino.hat_tem >= 37.2:
                self.temp_hatcher.setStyleSheet('background : white ; color: green;') 
            elif env_arduino.hat_tem < 37.2:
                self.temp_hatcher.setStyleSheet('background : white ; color: blue;') 
            else:
                self.temp_hatcher.setStyleSheet('background : white ; color: red;') 
                
        if env_arduino.hat_hum > 0 :
            self.hum_hatcher.setText("the humidity is  "+str(env_arduino.hat_hum))
            if 60 >= env_arduino.hat_hum >=50:
                self.hum_hatcher.setStyleSheet('background : white ; color: green;') 
            elif env_arduino.hat_hum < 50:
                self.hum_hatcher.setStyleSheet('background : white ; color: blue;') 
            else :
                self.hum_hatcher.setStyleSheet('background : white ; color: red;') 
            # self.temp_hatcher.setStyleSheet('color: green;')
        # print("you preesed") 


    def inc_refresh(self):
        if env_arduino.inc_tem > 0 :
            self.temp_incubator.setText("the temperature is  "+str(env_arduino.inc_tem))
            if 37.8 >= env_arduino.inc_tem >= 37.2:
                self.temp_incubator.setStyleSheet('background : white ; color: green;') 
            elif env_arduino.inc_tem <=37.2:
                self.temp_incubator.setStyleSheet('background : white ; color: blue;') 
            else:
                self.temp_incubator.setStyleSheet('background : white ; color: red;') 



        if env_arduino.inc_hum > 0 :
            self.hum_incubator.setText("the humidity is  "+str(env_arduino.inc_hum))
            if 60 >= env_arduino.inc_hum >=50:
                self.hum_incubator.setStyleSheet('background : white ; color: green;') 
            elif env_arduino.inc_hum < 50:
                self.hum_incubator.setStyleSheet('background : white ; color: blue;') 
            else :
                self.hum_incubator.setStyleSheet('background : white ; color: red;') 
        # self.temp_incubator.setStyleSheet('color: green;')
        # print("you preesed") 

    def shutdown(self):
        app.exec_()
        sleep(2)
        os.system("sudo shutdown -h now")    
        
    def EMERGENCY(self):
        move_arduino.my_serial_write("EMERGENCY")
        env_arduino.my_serial_write("EMERGENCY")


    def check_vacume(self):
        if self.vacume.isChecked():
            move_arduino.my_serial_write("vacume_1")
        else:
            move_arduino.my_serial_write("vacume_0")


    def check_selenoid(self):
        if self.solenoid.isChecked():
            move_arduino.my_serial_write("selenoid_1")
        else:
            move_arduino.my_serial_write("selenoid_0")

    def check_auto(self):
        if self.auto.isChecked():
            move_arduino.my_serial_write("auto")
        else:
            move_arduino.my_serial_write("auto")

    def refresh_window(self):
        env_arduino.read_values()
        self.hat_refresh()
        self.inc_refresh()
        self.update_timer2()
        self.update_timer6()
        self.update_background()
        
        # print("Received data from Arduino:",env_arduino.hat_hum)   
    
        current_time = strftime("%Y-%m-%d %H:%M:%S")
        self.label_date.setText(current_time)
        
        inc_holder.check_eggs()
        inc_holder.update_eggs_time()
        pos, action  = inc_holder.dequeue()
        
        if action == "hatch":
            hatch(pos)
        elif action == "move_out":
            move_egg_out(pos)
        
    def update_background(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
            ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label1.setPixmap(pixmap)
        self.label2.setPixmap(pixmap)
        self.label3.setPixmap(pixmap)
        self.label4.setPixmap(pixmap)
        self.label5.setPixmap(pixmap)
        
        
    def update_timer2(self):
        if self.time_left2 > 0:
            self.time_left2 -= 0.1
            minutes, seconds = divmod(self.time_left2, 60)
            time_format = f"{int(minutes):02}:{int(seconds):02}"
            self.tm2.setText(time_format)
        else:
            
            # self.time_left = 1200  
            self.tm2.setText("20:00")
        
        if env_arduino.read_line() == "auto_wins_up" :
            self.time_left2 = 20 * 60
            self.tm2.setText('20:00')

        
    def update_timer6(self):
        if self.time_left6 > 0:
            self.time_left6 -= 0.1
            minutes, seconds = divmod(self.time_left6, 60)
            time_format = f"{int(minutes):02}:{int(seconds):02}"
            self.tm6.setText(time_format)
        else:
            
            # self.time_left = 1200  
            self.tm6.setText("60:00")
        
        if move_arduino.read_line() == "moved_servo" :
            self.time_left6 = 60 * 60
            self.tm6.setText('60:00')

    # def update_timer(self):
    #     if self.time_left > 0:
    #         self.time_left -= 1
    #         minutes, seconds = divmod(self.time_left, 60)
    #         self.label.setText(f'{minutes:02}:{seconds:02}')
    #     else:
    #         self.timer.stop()
    #         self.label.setText('20:00') 

        # self.tm2.setText(current_time-old_time)
        # self.tm6.setText(current_time)


if __name__ == "__main__":
    import sys
    move_arduino, env_arduino = ArduinoCommand.find_arduinos()
    inc_holder = egg_holder()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())