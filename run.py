# "C:/Users/acer/.conda/envs/venv2/Lib/site-packages/mediapipe/modules;mediapipe/modules"
#E:/coop/GUI/pyqt5/images/images/LIFER_free-file.png
from ccmain import Ui_MainWindow
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *
from PIL import Image, ImageOps
import tensorflow as tf
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import math
import keyboard
import sys  
import os
import shutil
import speech_recognition as sr
from scipy.io import wavfile
from googletrans import Translator
import pyttsx3
import cv2
import mediapipe as mp
import keyboard
from time import sleep
import time
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from widgets import *
from app_settings import Settings
import soundfile
from scipy.io import wavfile
import string
from itertools import count
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
import os.path
from os import path
import unidecode
from ui_functions import *
from my_functions import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global i_tmp
        i_tmp = 0
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  
        self.setStyleSheet("Player {background: #000;}")     
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.uic.stackedWidget.setCurrentWidget(self.uic.home)
        self.uic.btn_home.clicked.connect(self.khiemthinh_page_button)
        self.uic.btn_widgets.clicked.connect(self.tran_page_button)
        self.uic.btn_new.clicked.connect(self.sl_button)
        self.uic.btn_save.clicked.connect(self.speech_to_sl_button)
        self.uic.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        # self.uic.toggleLeftBox.clicked.connect(self.openCloseLeftBox)
        # self.uic.settingsTopBtn.clicked.connect(self.openCloseRightBox)
        self.uic.closeAppBtn.clicked.connect(lambda: self.close())
        self.uic.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(self))
        self.uic.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())
        self.threadq = {}
        #EXCHANGE DATA
        self.uic.slide_time.sliderMoved.connect(self.setPosition)
        self.uic.upload_video_button.clicked.connect(self.link_to_video)
        self.uic.tran_video_button.clicked.connect(self.transition_video)
        self.uic.play_video_button.clicked.connect(self.show_video)
        self.uic.upload_recoder_button.clicked.connect(self.link_to_recoder)
        self.uic.size_ok_button_3.clicked.connect(self.font_size_word_1)
        self.uic.tran_recoder_button.clicked.connect(self.recoder_tran)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        #KHIEMTHINH_PAGE
        self.uic.lang_ok_button.clicked.connect(self.translate_text)
        self.uic.erase_button.clicked.connect(self.clean_word)
        self.uic.start_button.clicked.connect(self.tran_index_start)
        self.uic.end_button.clicked.connect(self.tran_index_stop)
        self.uic.size_ok_button.clicked.connect(self.font_size_word)
        #SL_PAGE
        self.uic.start_button_2.clicked.connect(self.start_capture_video)
        self.uic.end_button_2.clicked.connect(self.stop_capture_video)
        self.uic.lang_button.clicked.connect(self.start_translate_lang)
        #SPEECH_TO_SL
        self.uic.upload_gif_button.clicked.connect(self.link_to_gif)
        self.uic.upload_video_button_2.clicked.connect(self.link_to_video_gif)
        self.uic.cap_video_button.setEnabled(False)
        self.uic.upload_gif_button.setEnabled(False)
        self.uic.start_button_3.clicked.connect(self.start_thread_t2sl)
        self.uic.end_button_3.clicked.connect(self.stop_thread_t2sl)
        self.uic.cap_video_button.clicked.connect(self.start_get_video)
        self.uic.pushButton_3.clicked.connect(self.stop_get_video)
        self.uic.add_text_button.clicked.connect(self.get_name_def)
        self.uic.upload_video_button_2.setEnabled(False)
    def resizeEvent(self, event):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        reg = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(reg)
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
    def openCloseRightBox(self):
            UIFunctions.toggleRightBox(self, True)
    #STACKED_WIDGETS
    def speech_to_sl_button(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.speech_to_sl_page)
    def khiemthinh_page_button(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.khiemthinh_page)
    def tran_page_button(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.tran_page)
    def sl_button(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.sl_page)
    #FUNCTION OF EXCHANGING DATA
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    def positionChanged(self, position):
        self.uic.slide_time.setValue(position)
    def durationChanged(self, duration):
        self.uic.slide_time.setRange(0, duration)
    #FUNCTION OF KHIEMTHINH_PAGE
    def translate_text(self, tmp):
        t = Translator()
        if self.uic.lang_combox.currentText() == 'English':
            a = t.translate(tmp, dest= "en")
            self.uic.kt_text_2.setPlainText(str(a.text))
            print("Tiếng Anh " , a.text)
        elif self.uic.lang_combox.currentText() == 'Chinese':
            a = t.translate(tmp, dest= "zh-cn")
            self.uic.kt_text_2.setPlainText(str(a.text))
            print("Tiếng Trung " , a.text)
        elif self.uic.lang_combox.currentText() == 'Frence':
            a = t.translate(tmp, dest= "de")
            self.uic.kt_text_2.setPlainText(str(a.text))
            print("Tiếng Đức " , a.text)
        elif self.uic.lang_combox.currentText() == 'Tiếng Việt':
            a = t.translate(tmp, dest= "vi")
            self.stop_translate_lang
        return a
    def clean_word(self):
        global text_tmp
        text_tmp = []
    def tran_index_start(self):
        self.threadq[1]= get_voice(index = 1)
        self.threadq[1].start()
        self.threadq[1].print_text.connect(self.print_text)
        self.threadq[1].translate_text.connect(self.translate_text)
        
    def tran_index_stop(self):
        self.threadq[1].stop()
    def print_text(self, text):
        text = text.replace("Đức Giang","Đức Danh")
        self.uic.kt_text.setText(text)
        text = text.lower()
    def font_size_word(self):
        size = self.uic.size_text.toPlainText()
        self.uic.kt_text.setStyleSheet("  border-radius: 20px;\n"
"   background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.306818 rgba(63, 0, 64, 255), stop:0.886364 rgba(0, 27, 68, 255));\n"
"font: {}pt \"MS Shell Dlg 2\";\n".format(size))
# FUNCTION OF SL PAGE////////////////////////////////////////////////////////////////////////

    def stop_get_video(self):
        self.threadq[5].stop_get_video()
    def start_get_video(self):
        self.threadq[5] = Get_Video(index=1)
        self.threadq[5].start()
        self.threadq[5].signal_2.connect(self.show_wedcam_getvideo)

    def show_wedcam_getvideo(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.cap_video_label.setPixmap(qt_img)
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
#FUNCTION OF TRAN PAGE//////////////////////////////////////////////////////
    def recoder_tran(self):
        global ex
        # link = "C:/Users/acer/Desktop/cc.m4a"
        _, head = os.path.split(self.link_reco[0])
        head_tmp = head.replace("m4a","wav")
        print(head_tmp)
        print(head)
        link_1 = "E:/coop/GUI/pyqt5/{}".format(head)
        link_2 = "E:/coop/GUI/pyqt5/"
        check_exist = path.exists(link_1)
        shutil.copy(self.link_reco[0],link_1)
        os.system("ffmpeg -i {} {}".format(head, head_tmp))
        path_tmp = link_2 +"/"+ head_tmp
        print (path_tmp)
        # data, samplerate = soundfile.read(link_1)
        # soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
        recognizer = sr.Recognizer()
        with sr.AudioFile('{}'.format(path_tmp)) as source:
            recorded_audio = recognizer.listen(source)
            print("Done recording")
        try:
            print("Recognizing the text")
            text = recognizer.recognize_google(
                    recorded_audio, 
                    language="vi"
                )
            print("Decoded Text : {}".format(text))
        except Exception as ex:
            print(ex)
        self.uic.textEdit_2.setText(text)
    def link_to_recoder(self):
        self.link_reco = QFileDialog.getOpenFileName()
        self.uic.link_recoder_label_.setText(self.link_reco[0])
    def link_to_video(self):
        self.link = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        self.uic.link_video_label.setText(self.link[0])
        self.link_tmp = self.link[0]
        self.path=os.path.basename(self.link[0]).split('/')[-1]
        self.path = self.path.replace(" ","")
        self.src = 'E:/coop/GUI/pyqt5/{}'.format(self.path)
        c = path.exists(self.link_tmp)
        shutil.copyfile( self.link_tmp , self.src)
    def transition_video(self):
        os.system("autosrt -h")
        os.system("autosrt -S vi -D vi {}".format(self.path))
    def show_video(self):
        global i_tmp
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.src)))
        self.uic.textEdit_2.hide()
        if i_tmp == 0 :
            self.videoWidget = QVideoWidget()
            self.uic.verticalLayout_22.addWidget(self.videoWidget)
            self.mediaPlayer.error.connect(self.handleError)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            i_tmp = 1
    def handleError(self):
        print("Error: " + self.mediaPlayer.errorString())
    def stop_video(self):
        self.mediaPlayer.stop()
    def font_size_word_1(self):
        size_1 = self.uic.size_text_5.toPlainText()
        self.uic.textEdit_2.setStyleSheet("  border-radius: 20px;\n"
"   background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.306818 rgba(63, 0, 64, 255), stop:0.886364 rgba(0, 27, 68, 255));\n"
"font: {}pt \"Times New Roman\";\n".format(size_1))


#FUNCTION OF SL_PAGE////////////////////////////////////////////////////////////
    def stop_translate_lang(self):
        self.threadq[2].stop()

    def start_translate_lang(self):
        self.threadq[2] = translate_lang(index = 2)
        self.threadq[2].start()
        # self.threadq[2].translate_text.connect(self.translate_text)

    def stop_capture_video(self):
        self.uic.start_button.setEnabled(True)
        self.uic.end_button.setEnabled(False)
        self.threadq[3].stop()     

    def start_capture_video(self):
        self.threadq[3] = capture_video(index = 3)
        self.threadq[3].start()    
        self.uic.start_button.setEnabled(False)
        self.uic.end_button.setEnabled(True)
        self.threadq[3].signal.connect(self.show_wedcam)
        self.threadq[3].set_text.connect(self.set_text)

    def set_text(self, text):
        self.uic.textbox.setPlainText(str(text))

    def read_text_voice(self,text):
        text =self.uic.textEdit.toPlainText()
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        vi_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
        engine.setProperty("voice", vi_voice_id)
        engine.say(text)
        engine.runAndWait()

    def show_wedcam(self, cv_img):
        global label_temp
        #Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        #Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 250, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
#FUNCTION OF SPEECH_TO_SL /////////////////////////////////////
    def link_to_gif(self):
        global name_def
        self.link_gif = QFileDialog.getOpenFileName()
        self.uic.link_gif_text.setText(self.link_gif[0])
        head, tail = os.path.split(self.link_gif[0])
        tmp_add = "E:/coop/GUI/pyqt5/{}".format(tail)
        main_name = "{}.gif".format(name_def)
        shutil.move(self.link_gif[0],tmp_add)
        os.rename(tail,main_name )
        tmp_add_1 = "E:/coop/GUI/pyqt5/{}".format(main_name)
        main_add = "E:/coop/GUI/pyqt5/ISL_Gifs/{}".format(main_name)
        shutil.move(tmp_add_1,main_add)
    def link_to_video_gif(self):
        global name_def
        self.link_video = QFileDialog.getOpenFileName()
        self.uic.link_video_text.setText(self.link_video[0])
        head, tail = os.path.split(self.link_video[0])                       
        path_2_tmp = tail.replace(" ","")                                         
        index = path_2_tmp.index('.')
        my_str = path_2_tmp[:index] + '_1' + path_2_tmp[index:]                 
        head_tmp_2 = head +"/{}".format(my_str)
        shutil.copy(self.link_video[0],head_tmp_2)
        path_2_tmp_1 = my_str.replace("avi", "mp4")                             
        os.system("ffmpeg -i {} {}".format(head_tmp_2,path_2_tmp_1))         
        videoClip = VideoFileClip(path_2_tmp_1)
        path_3_tmp = path_2_tmp_1.replace("mp4","gif")                          
        videoClip.write_gif(path_3_tmp)                                         
        index = path_3_tmp.index('.')
        my_str_1 = path_3_tmp[:index] + '1' + path_3_tmp[index:] 
        head_tmp_1 = head +"/{}".format(path_3_tmp)
        head_tmp_2 = head +"/{}".format(my_str_1)                           
        shutil.copy(head_tmp_1,head_tmp_2)   
        change_name = tail.replace("avi", "gif")
        os.rename(my_str_1 ,change_name)                              
        link_gif_file = "E:/coop/GUI/pyqt5/ISL_Gifs/{}".format(change_name)
        head_tmp_3 = head +"/{}".format(change_name)
        shutil.copy(head_tmp_3,link_gif_file)
    def set_label_gif(self, gif):
        self.movie = QMovie(gif)
        self.movie.setScaledSize(QtCore.QSize(691,351))
        self.uic.image_sl.show()
        self.uic.image_sl.setMovie(self.movie)
        self.movie.start()
    def set_label_picture(self, pixmap):
        self.uic.image_sl.setPixmap(pixmap)
    def start_thread_t2sl(self):
        self.threadq[4] = t2sl(index = 1)
        self.threadq[4].start()    
        self.threadq[4].set_label_picture.connect(self.set_label_picture)
        self.threadq[4].set_label_gif.connect(self.set_label_gif)
    def stop_thread_t2sl(self):
        self.threadq[4].stop()     
    def get_name_def(self):
        global name_def
        name_def = self.uic.add_text_def.toPlainText()
        self.uic.upload_gif_button.setEnabled(True)
        self.uic.cap_video_button.setEnabled(True)
        self.uic.upload_video_button_2.setEnabled(True)
#///////////////////////////////////////////////////////////////////////////////////////////////////
#SPEECH_TO_SL
class t2sl(QThread):
    signal = pyqtSignal(object)
    set_label_picture = pyqtSignal(object)
    set_label_gif = pyqtSignal(object)
    def __init__(self, index= 0, name = '',):
        self.index = index
        self.name = name
        print("name ",self.name)
        print("start threading", self.index)
        super(t2sl, self).__init__()
    def tran_img(self, text, add_ce):
        a_tran = unidecode.unidecode(text)
        pixmap = QPixmap('E:/coop/GUI/pyqt5/letters/'+a_tran+'.jpg')
        pixmap5 = pixmap.scaled(751, 661)
        self.set_label_picture.emit(pixmap5)
        time.sleep(0.5)
        pixmap = QPixmap('E:/coop/GUI/pyqt5/letters/{}'.format(add_ce))
        pixmap5 = pixmap.scaled(751, 661)
        self.set_label_picture.emit(pixmap5)
        time.sleep(0.5)
    def tran_img_3w(self,text,text_add,add_ce):
        a_tran = unidecode.unidecode(text)
        pixmap = QPixmap('E:/coop/GUI/pyqt5/letters/'+a_tran+'.jpg')
        pixmap5 = pixmap.scaled(751, 661)
        self.set_label_picture.emit(pixmap5)
        time.sleep(0.5)
        pixmap = QPixmap('E:/coop/GUI/pyqt5/letters/{}'.format(text_add))
        pixmap5 = pixmap.scaled(751, 661)
        self.set_label_picture.emit(pixmap5)
        time.sleep(0.5)
        pixmap = QPixmap('E:/coop/GUI/pyqt5/letters/{}'.format(add_ce))
        pixmap5 = pixmap.scaled(751, 661)
        self.set_label_picture.emit(pixmap5)
        time.sleep(0.5)
    def run(self):
        r = sr.Recognizer()
        arr=['a','b','c','d','đ','e','f','g','h','i','j','k','l','m','n','o','p','q','r', 's','t','u','v','w','x','y','z']
        arr_mu_nguoc =['ă']
        arr_mu = ['ô','ê','â']
        arr_ngoac=['ơ','ư']
        arr_dau_sac = ['á','é','ó','ú','í','ý']
        arr_dau_huyen = ['à','è','ò','ù','ì','ỳ']
        arr_dau_nga =  ['ã','ẽ','õ','ũ','ĩ','ỹ']
        arr_dau_nang = ['ạ','ẹ','ọ','ụ','ị','ỵ']
        arr_dau_hoi = ['ả','ẻ','ỏ','ủ','ỉ','ỷ']
        arr_dau_sac_mu_nguoc = ['ắ']
        arr_dau_huyen_mu_nguoc = ['ằ']
        arr_dau_nang_mu_nguoc = ['ặ']
        arr_dau_nga_mu_nguoc = ['ẵ']
        arr_dau_hoi_mu_nguoc = ['ẳ']
        arr_dau_sac_mu = ['ố','ế','ấ']
        arr_dau_huyen_mu = ['ồ','ề','ầ']
        arr_dau_nang_mu = ['ộ','ệ','ậ']
        arr_dau_nga_mu = ['ỗ','ễ','ẫ']
        arr_dau_hoi_mu = ['ổ','ể','ẩ']
        arr_dau_sac_ngoac = ['ớ','ứ']
        arr_dau_huyen_ngoac = ['ờ','ừ']
        arr_dau_nang_ngoac = ['ợ','ự']
        arr_dau_nga_ngoac = ['ỡ','ữ']
        arr_dau_hoi_ngoac = ['ở','ử']
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source) 
                cnt_words=0
                while True:
                        print("I am Listening")
                        audio = r.listen(source)
                        text = "I am Listening"
                        i = 0
                        try:    
                                a=r.recognize_google(audio,language="vi-VI")
                                a = a.replace("Giang","Danh")
                                a = a.lower()
                                print('You Said: ' + a.lower())
                                for c in string.punctuation:
                                    a= a.replace(c,"")
                                    words = a.split(' ')
                                
                                link_path = "E:/coop/GUI/pyqt5/ISL_Gifs/{}.gif".format(a.lower())
                                data1 = path.exists(link_path)
                                c= len(words)
                                m = 0
                                if(a.lower()=='goodbye' or a.lower()=='good bye' or a.lower()=='bye'):
                                        print("oops!Time To say good bye")
                                        self.terminate()
                                if data1 == True:
                                    self.set_label_gif.emit(link_path)
                                    time.sleep(2)
                                else:
                                    for i in range (c):
                                        if  cnt_words == 0:
                                            if m < c-1:
                                                a = (words[m] +" "+ words[m+1])
                                            link_path = "E:/coop/GUI/pyqt5/ISL_Gifs/{}.gif".format(a)
                                            data = path.exists(link_path)
                                            if(data == True):
                                                self.set_label_gif.emit(link_path)
                                                time.sleep(2)
                                                m = m +2
                                            elif data == False:
                                                if m < c:
                                                    a = words[m]
                                                    m = m+1
                                                    cnt = 0
                                                    for i in range(len(a)):
                                                        if a[i] in arr_mu_nguoc:
                                                            add_acc = "dau_mu.jpg"
                                                            self.tran_img(a[i],add_acc)
                                                        elif a[i] in arr_mu:
                                                            add_acc = "dau_mu_chuan.jpg"
                                                            self.tran_img(a[i],add_acc )
                                                        elif a[i] in arr_ngoac:
                                                            add_acc = "dau_ngoac.jpg"
                                                            self.tran_img(a[i],add_acc )
                                                        elif a[i] in arr_dau_sac:
                                                            add_acc = "dau_sac.jpg"
                                                            self.tran_img(a[i],add_acc )
                                                        elif a[i] in arr_dau_huyen:
                                                            add_acc = "dau_huyen.jpg"
                                                            self.tran_img(a[i],add_acc )
                                                        elif a[i] in arr_dau_nga:
                                                            add_acc = "dau_nga.jpg"
                                                            self.tran_img(a[i],add_acc )
                                                        elif a[i] in arr_dau_nang:
                                                            add_acc = "dau_nang.jpg"
                                                            self.tran_img(a[i],add_acc )
                                                        elif a[i] in arr_dau_hoi:
                                                            add_acc = "dau_hoi.jpg"
                                                            self.tran_img(a[i],add_acc )
                                                        elif a[i] in arr_dau_sac_mu_nguoc:
                                                            add_acc = "dau_sac.jpg"
                                                            text_add = "dau_mu.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_huyen_mu_nguoc:
                                                            add_acc = "dau_huyen.jpg"
                                                            text_add = "dau_mu.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_nang_mu_nguoc:
                                                            add_acc = "dau_nang.jpg"
                                                            text_add = "dau_mu.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_nga_mu_nguoc:
                                                            add_acc = "dau_nga.jpg"
                                                            text_add = "dau_mu.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_hoi_mu_nguoc:
                                                            add_acc = "dau_hoi.jpg"
                                                            text_add = "dau_mu.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_sac_mu:
                                                            add_acc = "dau_sac.jpg"
                                                            text_add = "dau_mu_chuan.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_huyen_mu:
                                                            add_acc = "dau_huyen.jpg"
                                                            text_add = "dau_mu_chuan.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_nang_mu:
                                                            add_acc = "dau_nang.jpg"
                                                            text_add = "dau_mu_chuan.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_nga_mu:
                                                            add_acc = "dau_nga.jpg"
                                                            text_add = "dau_mu_chuan.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_hoi_mu:
                                                            add_acc = "dau_hoi.jpg"
                                                            text_add = "dau_mu_chuan.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_sac_ngoac:
                                                            add_acc = "dau_sac.jpg"
                                                            text_add = "dau_ngoac.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_huyen_ngoac:
                                                            add_acc = "dau_huyen.jpg"
                                                            text_add = "dau_ngoac.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_nang_ngoac:
                                                            add_acc = "dau_nang.jpg"
                                                            text_add = "dau_ngoac.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_nga_ngoac:
                                                            add_acc = "dau_nga.jpg"
                                                            text_add = "dau_ngoac.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        elif a[i] in arr_dau_hoi_ngoac:
                                                            add_acc = "dau_hoi.jpg"
                                                            text_add = "dau_ngoac.jpg"
                                                            self.tran_img_3w(a[i],text_add,add_acc )
                                                        else:
                                                            pixmap = QPixmap('letters/'+a[i]+'.jpg')
                                                            pixmap5 = pixmap.scaled(751, 661)
                                                            self.set_label_picture.emit(pixmap5)
                                                            time.sleep(0.5)
                                                            continue
                        except:
                               print(" ")
    def stop(self):
        print('Stopping thread...', self.index)
        self.terminate()
#///////////////////////////////////////////////////////////////////////////////////////////
#KHIEMTHINH
class get_voice(QThread):
    translate_text = pyqtSignal(object)
    signal = pyqtSignal(object)
    print_text = pyqtSignal(object)
    def __init__(self, index = 0):
        self.index = index
        print("Starting...", self.index)
        super(get_voice, self).__init__()
    def run (self):
        global text_tmp
        recognizer = sr.Recognizer()
        text_tmp = [""] 

        while True:
            try:
                with sr.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=1)
                    audio = recognizer.listen(mic)
                    text = recognizer.recognize_google(audio, language='vi')
            except:
                text = ""
            text_tmp.append(text)
            print( ' '.join(text_tmp))
            self.print_text.emit(' '.join(text_tmp))
    def stop(self):
        print("Stopped.", self.index)
        self.terminate()
#////////////////////////////////////////////////////////////////////////////////////////////
#SL_TO_TEXT
class capture_video(QtCore.QThread):
    
    signal = pyqtSignal(np.ndarray)
    set_text = pyqtSignal(object)
    read_text = pyqtSignal(object)
    def __init__(self, index= 0, name = ''):
        self.index = index
        self.name = name
        print("name ",self.name)
        print("start threading", self.index)
        super(capture_video, self).__init__()
    def cv2_to_pil(self,img): #Since you want to be able to use Pillow (PIL)
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    def pil_to_cv2(self,img):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    def classifier(self, cv2_img):
        image = self.cv2_to_pil(self.imgWhite)
        image = ImageOps.fit(image, self.size, Image.ANTIALIAS)
        # turn the image into a numpy array
        image_array = np.asarray(image)
        # Load the image into the array
        self.data[0] = image_array
        # run the inference
        prediction = self.model.predict(self.data)
        score = tf.nn.softmax(prediction[0])
        index = np.argmax(score)
        return score, index

    def run(self):
        offset = 20
        imgSize = 301
        self.img_height = 301
        self.img_width = 301
        self.size = (301, 301)
        self.data = np.ndarray(shape=(1, self.img_height,self.img_width,3), dtype=np.float32)
        a = [" "]
        labels =['A', 'B', 'D', 'G', 'H', 'L', 'N', 'O', 'U', 'cảm ơn', 'oke', 'tên là', 'tôi', 'xin chào', 'xin lỗi']
        model_dir = 'saved_model.h5'
        num_classes = len(labels)
        self.model = Sequential([
        layers.Rescaling(1. / 255, input_shape=(301, 301, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

        self.model.load_weights(model_dir)
        cap = cv2.VideoCapture(0)
        detector = HandDetector(maxHands=2)
        frame_cnt = 0
        while True:
            success, img = cap.read()
            frame_cnt+=1
            hands, img = detector.findHands(img)
            if frame_cnt % 40 == 0:
                if hands:
                    hand = hands[0]
                    x, y, w, h = hand['bbox']

                    self.imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  
                    imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

                    imgCropShape = imgCrop.shape

                    aspectRatio = h / w
                    if aspectRatio > 1:
                        k = imgSize / h
                        wCal = math.ceil(k * w)
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        self.imgWhite[:, wGap:wCal + wGap] = imgResize
                        prediction, index = self.classifier( self.imgWhite)

                    else:
                        k = imgSize / w
                        hCal = math.ceil(k * h) 
                        imgResize = cv2.resize(imgCrop-10, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        self.imgWhite[hGap:hCal + hGap, :] = imgResize
                        prediction, index = self.classifier( self.imgWhite)
                    print(prediction[index])
                    if prediction[index] > 0.99:
                        if a[-1] != labels[index]:
                            time.sleep(0.1)
                            a.append(labels[index])
                    self.set_text.emit(' '.join(a)  )
                    cv2.imshow("frame",self.imgWhite)
                    print(a)
            if keyboard.is_pressed(' '):
                a = [" "]
            if success:
                self.signal.emit(img)  
            cv2.waitKey(1)

    def stop(self):
        print("stop threading", self.index)
        self.terminate()
class translate_lang(QtCore.QThread):
    signal_1 = pyqtSignal(object)
    # translate_text = pyqtSignal(object)
    set_text_2 = pyqtSignal(str)
    def __init__(self, index=0 ):
        super(translate_lang, self).__init__()
        self.index = index
    def run(self):
        global sentence
        print('Starting thread...', self.index)
        while True:
            # self.translate_text.emit(' '.join(sentence))
            time.sleep(2)
    def stop(self):
        print('Stopping thread...', self.index)
        self.terminate()
#////////////////////////////////////////////////////////////////
class Get_Video(QtCore.QThread):
    signal_2 = pyqtSignal(np.ndarray)
    def __init__(self, index):
        global name_def
        print(name_def)
        self.index = index
        print("start threading", self.index)
        super(Get_Video, self).__init__()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('{}.avi'.format(name_def), fourcc, 20.0, (640, 480))
    def run(self):
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            ret, cv_img = cap.read()
            if ret:
                self.out.write(cv_img)
                self.signal_2.emit(cv_img)
        cap.release()
    def stop_get_video(self):
        print("stop threading", self.index)
        self.terminate()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())