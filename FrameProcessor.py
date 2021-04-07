##### Comments:
'''
Символ G в комментариях - старый код
Символ GUI в комментариях - добавить в gui
Символ + в комментариях - регулировка точности
'''
#-#-#


##### Imports:

### Video parsing:
import cv2 as cv
import numpy as np


### General:
# Time:
import time
#from time import time
from datetime import timedelta

#-#-#


##### Variables + Initialisations:

def Initialize():
    ### Global variables list:
    global start_time, timer, \
    ref_size, ref_x, ref_y, \
    calc_zone, \
    numbBox, numbCons, numbAll, boxSize, \
    prodOld, prodCurr, \
    isWork, \
    inFrame, \
    sens_lower, sens_upper, \
    noise_lower, noise_upper, \
    pixels_h, ref_hsv, \
    bound_lower, bound_upper

    ### Start time counting:
    start_time = time.time() #Момент времени когда програма была запущена
    #timer = 0 #Инициализация таймера (с нуля) GUI old
    timer = 0 #Инициализация таймера (с нуля) GUI new

    ###Положение опорного кадра цвета фона (место где нет продукта и только лента конвейера):
    #ref_size = 50 #Size (by x and y) G
    ref_size = 50 #Size (by x and y) + 

    #ref_x = 160 #Start point by x G
    ref_x = 215 #Start point by x + 

    #ref_y = 10 #Start point by y G
    ref_y = 5 #Start point by y +


    ### Зона подсчета пикселей:
    calc_zone = ((0,225),(220,255)) # +

    pixels_h = 0

    ref_hsv = 0


    ### Counting:
    #boxCounter = 0 #количество объектов в коробке G
    numbBox = 0 #количество продукции в коробке GUI

    #typeCounter = 0 #количество объектов одного типа G
    numbCons = 0 #количество продукции в текущей партии (один тип продукта) GUI

    #counter = 0 #количество объектов за смену G
    numbAll = 0 #количество всей продукции с момента включения GUI

    boxSize = 3 #вместимость коробки GUI

    #oldType = "sosage" #предыдущий тип продукта G
    prodOld = " " #предыдущий тип продукта GUI

    #newType = "sosage" #настоящий тип продукта G
    prodCurr = " " #текущий тип продукта GUI

    #stop = 0 #0 - конвейер работает, 1 - конвейер остановлен G
    isWork = False #True - конвейер работает, False - конвейер не работает GUI


    ### Object finding:
    inFrame = False #True - объект в области обнаружен, False - объект в области не обнаружен GUI

    #level = 10 #порог наличия объекта G
    sens_lower = 300 #нижний порог наличия объекта (min = noise_upper+1) +
    sens_upper = 6600 #верхний порог наличия объекта (max = 6600) +

    noise_lower = 1 #нижний порог наличия шумов (min = 1) +
    noise_upper = 299 #верхний порог наличия шумов (max = sens_lower-1) +

    bound_lower = []
    bound_upper = []

    ### Not in use:
    #workTime = 0 #время работы конвейера GUI
    #stopTime = 0 #время останова конвейера GUI


    ### From GUI file:
    #IDlist = [] #список типов продукции old
    prodList = [] #список типов продукции new
    #next = False # удалить
    
#-#-#


##### Functions:

def FrameProcess(frame, isRet):
    ### Global variables list:
    global start_time, timer, \
    ref_size, ref_x, ref_y, \
    calc_zone, \
    numbBox, numbCons, numbAll, boxSize, \
    prodOld, prodCurr, \
    isWork, \
    inFrame, \
    sens_lower, sens_upper, \
    noise_lower, noise_upper, \
    pixels_h, ref_hsv, \
    bound_lower, bound_upper


    ### Function:
    #while(cap.isOpened()): old

    ### Time counting:
    timer = (time.time()-start_time)// 1 #Время с момента запуска программы (// - целое от деления)
    #print(timedelta(seconds=int(timer)))
    #timerDHS = str(timedelta(seconds = int(timer)))) new +++


    ### Video source processing:
    if isRet == True:
        #_, frame = cap.read()  #Main Frame (video source in colour), Take each frame old
        
        #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #Convert BGR to HSV (whole Frame zone) G
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #Convert BGR to HSV (whole Frame zone)

        #(источник https://docs.opencv.org/4.2.0/df/d9d/tutorial_py_colorspaces.html)
        #bgr_ref = np.median(frame[ref_x:ref_x+ref_size,ref_y:ref_y+ref_size],axis=[0,1]) #Medium colour (RGB) in ref zone G
        ref_bgr = np.median(frame[ref_x:ref_x+ref_size,ref_y:ref_y+ref_size],axis=[0,1]) #Medium colour (RGB) in ref zone

        #bgr_ref = np.uint8([[bgr_ref]]) #Convert type to unsigned int G
        ref_bgr = np.uint8([[ref_bgr]]) #Convert type to unsigned int

        #hsv_ref = cv.cvtColor(bgr_ref,cv.COLOR_BGR2HSV) #Convert BGR to HSV (only ref zone) G
        ref_hsv = cv.cvtColor(ref_bgr,cv.COLOR_BGR2HSV) #Convert BGR to HSV (only ref zone)

        #hsv_ref = hsv_ref[0,0] # Extract HSV from massive (only ref zone) G
        ref_hsv = ref_hsv[0,0] # Extract HSV from massive (only ref zone) +
                #Reference colour ~ (100, 20, 190 +_10), Default HSV = (0-255, 0-255, 0-255) +
        '''
        print (ref_hsv) # For debugging
        '''

        # Define range of ref color in HSV:

        '''
        #вот так по-идее правильно:
        #lower_bound = np.transpose(cv.subtract(hsv_ref, np.uint8([10,100,100])))[0] G
        #lower_bound = np.transpose(cv.subtract(ref_hsv, np.uint8([10,100,100])))[0]
        #upper_bound = np.transpose(cv.add(hsv_ref, np.uint8([10,255,255])))[0] G
        #upper_bound = np.transpose(cv.add(ref_hsv, np.uint8([10,255,255])))[0]
        
        #но вот так работает:
        '''
        
        #lower_bound = np.uint8([hsv_ref[0]-10,50,50]) G
        bound_lower = np.uint8([ref_hsv[0]-10,50,50]) #Lower bound of reference colour +
        #bound_lower_s = ref_hsv-[10,20,30] #Lower bound of reference colour +
        
        print (bound_lower) #For debugging
        

        #upper_bound = np.uint8([hsv_ref[0]+10,255,255]) G
        bound_upper = np.uint8([ref_hsv[0]+10,255,255]) #Upper bound of reference colour +
        #bound_upper_s = ref_hsv+[10,20,30] #Lower bound of reference colour +
        
        print (bound_upper) #For debugging
        

        # Threshold the HSV image to get only reference colours:
        #mask = cv.inRange(hsv, lower_bound, upper_bound) G
        mask = cv.inRange(frame_hsv, bound_lower, bound_upper) #Mask frame (only products, black and white)

        # Counting zone processing:
        sample = mask[calc_zone[0][1]:calc_zone[1][1], calc_zone[0][0]:calc_zone[1][0]] #Mask in counting zone
        #pixels = sum(sum(sample))//255 #Среднее значение цвета в каждом пикселе G
        #pixels_m = sum(sum(sample))//255 #???Среднее значение цвета пикселей в области счёта
        #pixels = sum(sum(sample))#//255 #???Сумма всех пикселей в области счёта 

        '''
        # For debugging:
        sum0 = 0
        sum255 = 0
        for i in range (len(sample) ): 
            for j in range (len(sample[i]) ): 
                if (sample[i][j] == 0):
                    sum0 += 1
                if (sample[i][j] == 255):
                    sum255 += 1 
        print (sum0)
        print (sum255)
        print (sum0 + sum255)
        '''
        
        # Number of pixels (pixels_h) which = 255 in counting zone on Mask frame (white colour):
        pixels_h = 0 
        for row in sample: 
           pixels_h += sum(row)
        pixels_h /= 255   # +


        ### Product checking:
        #if (pixels > level): G
        if (pixels_h >= sens_lower and pixels_h <= sens_upper):
            inFrame = True # +++
            '''
            print("inFrame")
            '''
            #sleep(1000)
        elif (pixels_h >= noise_lower and pixels_h <= noise_upper):
            '''    
            print("Noise")
            '''
        else:
            if inFrame:
                '''
                print("Added +1")
                '''
                #boxCounter += 1 G
                numbBox += 1
                    
                #if (boxCounter > boxSize): G
                #boxCounter = 1 G
                if (numbBox >= boxSize):
                    #typeCounter += 1 G
                    numbCons += 1
                    numbBox = 0

                #counter += 1 G
                numbAll += 1
                      
                inFrame = False

        #if (newType != oldType): G
            #typeCounter = 0 G
        if (prodCurr != prodOld):
            numbCons = 0


        ### Screens output:
        # Bitwise-AND mask and original image ???
        res = cv.bitwise_and(frame,frame, mask= mask) #Result frame (mask in colour)
        DrawCustom(frame, numbBox, numbCons, numbAll, timer) #Text output


        '''
        # For debugging:
        #cv.imshow('ref',frame[ref_x:ref_x+ref_size,ref_y:ref_y+ref_size]) #Screen: Reference zone frame
        #cv.imshow('frame',frame) #Screen: Main Frame
        #cv.imshow('mask',mask) #Screen: Mask frame
        #cv.imshow('res',res) #Screen: Result frame

        #print(sample.shape) #<Name> frame: Resolution
        #print(sample.size) #<Name> frame: Number of pixels (Если RGB, то ещё делим на 3, т. к. 3 канала)

        #print (pixels_h) #Number of 
        #print()
        
        #if cv.waitKey(20) == ord('q'): # При нажатии клавиши Q - завершать цикл While
        #    break
        '''

        
        return frame

    else:
        cv.destroyAllWindows()
        #return 0

def DrawTextInRect(frame, pos, text): # Вывод готового текста в рамке
    if pos==1: #In Box
        r_pos=(0, 20)
        r_size=(220,40)
    elif pos==2: #In Consignment
        r_pos=(0, 40)
        r_size=(220,60)
    elif pos==3: #Total
        r_pos=(0, 60)
        r_size=(220,80)
    elif pos==4: #Time since start (Runtime)
        r_pos=(0, 80)
        r_size=(220,100)
    else: #Default
        r_pos=(0, 0)
        r_size=(220,20)

    #Вывод рамки вокруг текста:
    cv.rectangle(frame, r_pos, r_size, (255,0,0), -1)

    #Вывод текста:
    cv.putText(frame, text, (r_pos[0],r_pos[1]+12),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (255,255,255))


def DrawCustom(frame, numbBox, numbCons, numbAll, timer): # Задание текста для вывода
    #DrawTextInRect(frame, 0, str(cap.get(cv.CAP_PROP_POS_FRAMES)))
    #DrawTextInRect(mask, 1, str(frame.shape))
    #DrawTextInRect(mask, 1, str(pixels))
    
    #DrawTextInRect(frame, 0, "Products in Box: " + str(boxCounter)) G
    DrawTextInRect(frame, 0, "Products in Box: " + str(numbBox))

    #DrawTextInRect(frame, 1, "Products of This Type: " + str(typeCounter)) G
    DrawTextInRect(frame, 1, "Products in Consignment: " + str(numbCons))
    
    #DrawTextInRect(frame, 2, "Products per Shift: " + str(counter)) G
    DrawTextInRect(frame, 2, "Total products: " + str(numbAll))
    
    #DrawTextInRect(frame, 3, "Work Time: " + str(workTime)) G
    DrawTextInRect(frame, 3, "Runtime: " + str(timer))

    #DrawTextInRect(frame, 4, "Stop Time: " + str(stopTime)) #Добавить позднее
    
    cv.rectangle(frame,calc_zone[0],calc_zone[1],(255,0,0),2) #Рамка области подсчета


def GetVariable():
    ### Global variables list:
    global start_time, timer, \
    ref_size, ref_x, ref_y, \
    calc_zone, \
    numbBox, numbCons, numbAll, boxSize, \
    prodOld, prodCurr, \
    isWork, \
    inFrame, \
    sens_lower, sens_upper, \
    noise_lower, noise_upper, \
    pixels_h, ref_hsv, \
    bound_lower, bound_upper


    guiVars = [numbBox, numbCons, numbAll, #0, 1, 2
               timer, #3
               pixels_h, ref_hsv, #4, 5
               sens_lower, sens_upper, # 6, 7
               noise_lower, noise_upper,# 8, 9
               calc_zone, # 10
               ref_x, ref_y, ref_size,# 11, 12, 13
               bound_lower, bound_upper # 14, 15
               ]
    return guiVars

#-#-#


##### Main:

#cap = cv.VideoCapture('cutted.avi') #Video source (нужно ли это???)

#cv.destroyAllWindows() #Закрыть все окна (нужно ли это???)

#-#-#
