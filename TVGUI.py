"""
Filename: TVGUI.py
Author: Taliesin Reese
Verion: 1.0
Date: 11/11/2023
Purpose: Regularly-scheduled programming
"""
import tkinter
from pygame import mixer
from PIL import Image, ImageTk
import cv2
import time
def guiLayout(win: tkinter.Tk)->None:
    """
        Lay out the widgets of the window belonging to the TV passed in.
    """
    win.geometry("500x250")
    win.title("TV Simulator 2023")
    win.resizable(False, True)
    #images
    win.bgimg = ImageTk.PhotoImage(Image.open("BG.png"))
    win.powup = ImageTk.PhotoImage(Image.open("powBtnDef.png"))
    win.powhov = ImageTk.PhotoImage(Image.open("powBtnHov.png"))
    win.powpress = ImageTk.PhotoImage(Image.open("powBtnPrs.png"))
    win.muteup = ImageTk.PhotoImage(Image.open("muteBtnDef.png"))
    win.mutehov = ImageTk.PhotoImage(Image.open("muteBtnHov.png"))
    win.mutepress = ImageTk.PhotoImage(Image.open("muteBtnPrs.png"))
    win.volupup = ImageTk.PhotoImage(Image.open("volUpBtnDef.png"))
    win.voluphov = ImageTk.PhotoImage(Image.open("volUpBtnHov.png"))
    win.voluppress = ImageTk.PhotoImage(Image.open("volUpBtnPrs.png"))
    win.voldownup = ImageTk.PhotoImage(Image.open("volDownBtnDef.png"))
    win.voldownhov = ImageTk.PhotoImage(Image.open("volDownBtnHov.png"))
    win.voldownpress = ImageTk.PhotoImage(Image.open("volDownBtnPrs.png"))
    win.chnupup = ImageTk.PhotoImage(Image.open("chnUpBtnDef.png"))
    win.chnuphov = ImageTk.PhotoImage(Image.open("chnUpBtnHov.png"))
    win.chnuppress = ImageTk.PhotoImage(Image.open("chnUpBtnPrs.png"))
    win.chndownup = ImageTk.PhotoImage(Image.open("chnDownBtnDef.png"))
    win.chndownhov = ImageTk.PhotoImage(Image.open("chnDownBtnHov.png"))
    win.chndownpress = ImageTk.PhotoImage(Image.open("chnDownBtnPrs.png"))
    #BG
    win.canvas = tkinter.Canvas(win, width = 500, height = 250)
    win.canvas.place(x = 0, y = 0)
    win.bg = win.canvas.create_image((250, 125), image = win.bgimg)
    #status label
    win.statuslbl = tkinter.Label(win, text = "Power:False Mute:False Channel:0 Volume:0")
    win.statuslbl.place(x = 250, y = 20)
    #player
    win.player0 = cv2.VideoCapture(r"Video (0).mp4")
    win.video0 = win.canvas.create_image((129,97), image = win.bgimg)
    win.video0duration = 0.0
    win.video0frame = ImageTk.PhotoImage(Image.open("BG.png"))
    win.prevframe0 = time.time()
    
    win.player1 = cv2.VideoCapture(r"Video (1).mp4")
    win.video1 = win.canvas.create_image((129,97), image = win.bgimg)
    win.video1duration = 0.0
    win.video1frame = ImageTk.PhotoImage(Image.open("BG.png"))
    win.prevframe1 = time.time()

    win.player2 = cv2.VideoCapture(r"Video (2).mp4")
    win.video2 = win.canvas.create_image((129,97), image = win.bgimg)
    win.video2duration = 0.0
    win.video2frame = ImageTk.PhotoImage(Image.open("BG.png"))
    win.prevframe2 = time.time()

    win.player3 = cv2.VideoCapture(r"Video (3).mp4")
    win.video3 = win.canvas.create_image((129,97), image = win.bgimg)
    win.video3duration = 0.0
    win.video3frame = ImageTk.PhotoImage(Image.open("BG.png"))
    win.prevframe3 = time.time()

    #remote label
    win.remotelabel = tkinter.Label(win, background = "#7f7f7f", foreground = "#ffffff", text = "VOL        CHN")
    win.remotelabel.place(x = 386, y = 141)
    #buttons
    ##power button
    win.powbtn = tkinter.Label(win, background = "#7f7f7f", image = win.powup)
    win.powbtn.place(x = 381, y = 100)
    ##Mute button
    win.mutebtn = tkinter.Label(win, background = "#7f7f7f", image = win.muteup)
    win.mutebtn.place(x = 433, y = 100)
    ##volume up
    win.volupbtn = tkinter.Label(win, background = "#7f7f7f", image = win.volupup)
    win.volupbtn.place(x = 381, y = 161)
    ##volume down
    win.voldownbtn = tkinter.Label(win, background = "#7f7f7f", image = win.voldownup)
    win.voldownbtn.place(x = 381, y = 202)
    ##channel up
    win.chnupbtn = tkinter.Label(win, background = "#7f7f7f", image = win.chnupup)
    win.chnupbtn.place(x = 433, y = 161)
    ##channel down
    win.chndownbtn = tkinter.Label(win, background = "#7f7f7f", image = win.chndownup)
    win.chndownbtn.place(x = 433, y = 202)
    #Excellent. Please proceed quickly to the chamberlock, as measuring the effects of prolonged exposure to the button is not part of this test.
def updatePlayer(channel: int, prevframe: float, timeupdatefunc: callable, win: tkinter.Tk, player: cv2.VideoCapture, video: int, setframefunc: callable, duration: float, setdurationfunc: callable, sound: mixer.Sound):
    """Update video on the window passed in. Now, please tell me why all these imports aren't just in a new class, Tali. Oh? you can't? Nice.
    :param channel: the current channel of the tv object
    :param prevframe: the time since this video was updated
    :param timeupdatefunc: function to update previous time
    :param win: tkinter window
    :param player: cv2 video capture of file
    :param video: id for video on canvas, in form of integer
    :param setframefunc: function to store frame
    :param duration: elapsed duration of video being passed in
    :param setdurationfunc: function to store video duration
    """
    #get the time now
    currenttime = time.time()
    try:
        #subtract last loop time to get elapsed time
        passtime = currenttime-prevframe
        #print("time passed: ",currenttime-win.lastframetime)
    except AttributeError as e:
        passtime = 0
    timeupdatefunc()
    fps = player.get(cv2.CAP_PROP_FPS)
    newframe = setdurationfunc(duration + passtime)*fps
    player.set(cv2.CAP_PROP_POS_FRAMES,newframe)
    if (setdurationfunc.__name__==f"duration{channel}update"):
        returnval, win.rawimage = player.read()
        if returnval == True:
            image = cv2.cvtColor(win.rawimage, cv2.COLOR_BGR2RGB)
            arraypic = Image.fromarray(image)
            arraypic = arraypic.resize((148,96),Image.ANTIALIAS)
            pic = ImageTk.PhotoImage(arraypic)
            setframefunc(pic)
            win.canvas.itemconfig(video, image = pic)
        else:
            player.set(cv2.CAP_PROP_POS_MSEC, 0)
            setdurationfunc(0)
            sound.play()
    #time.sleep(1)
