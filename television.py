"""
Filename: television.py
Author: Talieisn Reese
Version: 2.1
Date: 12/8/2023
Purpose: Now in glorious Visuals
"""
import tkinter
from pygame import mixer
import time
import TVGUI
from PIL import ImageTk, Image

class Television:
  """
  A class that represents a television. Far less interesting than the real thing.
  """
  MIN_VOLUME = 0
  MAX_VOLUME = 2
  MIN_CHANNEL = 0
  MAX_CHANNEL = 3
  mixer.init()
  def __init__(self):
    """ If you want a Television, you must first BEND REALITY TO YOUR WHIMS AND CREATE IT EX NIHILO
    :return: Television Object"""
    self.__status = False
    self.__muted = False
    self.__volume = Television.MIN_VOLUME
    self.__channel = Television.MIN_CHANNEL
    #create the GUI
    self.window = tkinter.Tk()
    TVGUI.guiLayout(self.window)
    self.funcAssign()
    #set up the audios
    self.sound0 = mixer.Sound("Audio (0).wav")
    self.sound1 = mixer.Sound("Audio (1).wav")
    self.sound2 = mixer.Sound("Audio (2).wav")
    self.sound3 = mixer.Sound("Audio (3).wav")
    self.activesound = self.sound0
    self.soundUpdate()
    self.sound0.play()
    self.sound1.play()
    self.sound2.play()
    self.sound3.play()
    #set up the videos
    self.activevid = self.window.video0
    self.vidUpdate()

  def power(self)->None:
    """Turn the TV off or on."""
    if self.__status:
      self.__status = False
    else:
      self.__status = True
    self.vidUpdate()
    self.soundUpdate()
    #just a little housekeeping here.
    self.window.powbtn.config(image = self.window.powup)
  def mute(self)->None:
    """Stop the volume. Only works if TV is ON"""
    if self.__status == True:
      if self.__muted:
        self.__muted = False
      else:
        self.__muted = True
      self.soundUpdate()
    #don't mind me, just resetting the button image
    self.window.mutebtn.config(image = self.window.muteup)
  def channel_up(self)->None:
    """Iterate channel up by one. If channel is at maximum, loop back to minimum. Only works if TV is ON"""
    if self.__status == True:
      if self.__channel == Television.MAX_CHANNEL:
        self.__channel = Television.MIN_CHANNEL
      else:
        self.__channel += 1
      self.vidUpdate()
      self.soundUpdate()
    #this'll just take a minute.
    self.window.chnupbtn.config(image = self.window.chnupup)
  def channel_down(self)->None:
    """Iterate channel down by one. If channel is at minimum, loop back to maximum. Only works if TV is ON"""
    if self.__status == True:
      if self.__channel == Television.MIN_CHANNEL:
        self.__channel = Television.MAX_CHANNEL
      else:
        self.__channel -= 1
      self.vidUpdate()
      self.soundUpdate()
    #Here, let me fix that up for you.
    self.window.chndownbtn.config(image = self.window.chndownup)
  def volume_up(self)->None:
    """Iterate volume up by one. If volume is at maximum, don't iterate any longer. Automatically un-mutes the TV. Only works if TV is ON"""
    if self.__status == True:
      if self.__volume < Television.MAX_VOLUME:
        self.__volume += 1
        self.__muted = False
      self.soundUpdate()
      self.vidUpdate()
    #Oh, here's another one.
    self.window.volupbtn.config(image = self.window.volupup)
  def volume_down(self)->None:
    """Iterate volume down by one. If volume is at minimum, don't iterate any longer. Automatically un-mutes the TV. Only works if TV is ON"""
    if self.__status == True:
      if self.__volume > Television.MIN_VOLUME:
        self.__volume -= 1
        self.__muted = False
      self.soundUpdate()
      self.soundUpdate()
    #I feel like the maid, like, "I just cleaned this mess up! Can it stay clean? Fo-for 10 MINUTES?"
    self.window.voldownbtn.config(image = self.window.voldownup)

  def __str__(self)->None:
    """Display stats of the TV.
    :return: a string representation of the TV object"""
    if self.__muted == False:
      return f"Power = {self.__status}, Channel = {self.__channel}, Volume = {self.__volume}"
    else:
      return f"Power = {self.__status}, Channel = {self.__channel}, Volume = {0}"

  def soundUpdate(self):
    """Apply changes to the program sounds"""
    self.activesound = getattr(self,f"sound{self.__channel}")
    self.sound0.set_volume(0.0)
    self.sound1.set_volume(0.0)
    self.sound2.set_volume(0.0)
    self.sound3.set_volume(0.0)
    if self.__muted == False and self.__status == True:
      self.activesound.set_volume(self.__volume/2)
  def vidUpdate(self):
    """Apply changes to the displayed video"""
    self.activevid = getattr(self.window, f"video{self.__channel}")
    self.window.canvas.itemconfig(self.window.video0, state = 'hidden')
    self.window.canvas.itemconfig(self.window.video1, state = 'hidden')
    self.window.canvas.itemconfig(self.window.video2, state = 'hidden')
    self.window.canvas.itemconfig(self.window.video3, state = 'hidden')
    if self.__status == True:
      self.window.canvas.itemconfigure(self.activevid, state = 'normal')

  def update(self):
    """Special addons to the update loop"""
    TVGUI.updatePlayer(self.__channel, self.window.prevframe0, self.updatetime0, self.window, self.window.player0, self.window.video0, self.frame0update, self.window.video0duration, self.duration0update, self.sound0)
    TVGUI.updatePlayer(self.__channel, self.window.prevframe1, self.updatetime1, self.window, self.window.player1, self.window.video1, self.frame1update, self.window.video1duration, self.duration1update, self.sound1)
    TVGUI.updatePlayer(self.__channel, self.window.prevframe2, self.updatetime2, self.window, self.window.player2, self.window.video2, self.frame2update, self.window.video2duration, self.duration2update, self.sound2)
    TVGUI.updatePlayer(self.__channel, self.window.prevframe3, self.updatetime3, self.window, self.window.player3, self.window.video3, self.frame3update, self.window.video3duration, self.duration3update, self.sound3)
    self.window.update()

  def frame0update(self, frame: ImageTk.PhotoImage):
    """Updates video0frame for later use of the included frame
    :param frame: frame to store in class variable"""
    self.window.video0frame = frame
  def frame1update(self, frame: ImageTk.PhotoImage):
    """Updates video1frame for later use of the included frame
    :param frame: frame to store in class variable"""
    self.window.video1frame = frame
  def frame2update(self, frame: ImageTk.PhotoImage):
    """Updates video2frame for later use of the included frame
    :param frame: frame to store in class variable"""
    self.window.video2frame = frame
  def frame3update(self, frame: ImageTk.PhotoImage):
    """Updates video3frame for later use of the included frame
    :param frame: frame to store in class variable"""
    self.window.video3frame = frame

  def updatetime0(self):
    """Updates the times for video0"""
    self.window.prevframe0 = time.time()
  def updatetime1(self):
    """Updates the times for video1"""
    self.window.prevframe1 = time.time()
  def updatetime2(self):
    """Updates the times for video2"""
    self.window.prevframe2 = time.time()
  def updatetime3(self):
    """Updates the times for video3"""
    self.window.prevframe3 = time.time()
    
  def duration0update(self, duration: float)-> float:
    """Updates video0duration for later use in calculation of FPS
    :param duration: duration to store in class variable
    :return: the frame you just set"""
    self.window.video0duration = duration
    return self.window.video0duration
  def duration1update(self, duration: float)-> float:
    """Updates video1duration for later use in calculation of FPS
    :param duration: duration to store in class variable
    :return: the frame you just set"""
    self.window.video1duration = duration
    return self.window.video1duration
  def duration2update(self, duration: float)-> float:
    """Updates video2duration for later use in calculation of FPS
    :param duration: duration to store in class variable
    :return: the frame you just set"""
    self.window.video2duration = duration
    return self.window.video2duration
  def duration3update(self, duration: float)-> float:
    """Updates video3duration for later use in calculation of FPS
    :param duration: duration to store in class variable
    :return: the frame you just set"""
    self.window.video3duration = duration
    return self.window.video3duration

  def funcAssign(self)->None:
    """Assign functions to the buttons and other required Event calls"""
    #power
    self.window.powbtn.bind("<Enter>", lambda x : self.window.powbtn.config(image = self.window.powhov))
    self.window.powbtn.bind("<Leave>", lambda x : self.window.powbtn.config(image = self.window.powup))
    self.window.powbtn.bind("<Button-1>", lambda x : self.window.powbtn.config(image = self.window.powpress))
    self.window.powbtn.bind("<ButtonRelease-1>", lambda x : self.power())
    #mute
    self.window.mutebtn.bind("<Enter>", lambda x : self.window.mutebtn.config(image = self.window.mutehov))
    self.window.mutebtn.bind("<Leave>", lambda x : self.window.mutebtn.config(image = self.window.muteup))
    self.window.mutebtn.bind("<Button-1>", lambda x : self.window.mutebtn.config(image = self.window.mutepress))
    self.window.mutebtn.bind("<ButtonRelease-1>", lambda x : self.mute())
    #volume toggle
    self.window.volupbtn.bind("<Enter>", lambda x : self.window.volupbtn.config(image = self.window.voluphov))
    self.window.volupbtn.bind("<Leave>", lambda x : self.window.volupbtn.config(image = self.window.volupup))
    self.window.volupbtn.bind("<Button-1>", lambda x : self.window.volupbtn.config(image = self.window.voluppress))
    self.window.volupbtn.bind("<ButtonRelease-1>", lambda x : self.volume_up())
    self.window.voldownbtn.bind("<Enter>", lambda x : self.window.voldownbtn.config(image = self.window.voldownhov))
    self.window.voldownbtn.bind("<Leave>", lambda x : self.window.voldownbtn.config(image = self.window.voldownup))
    self.window.voldownbtn.bind("<Button-1>", lambda x : self.window.voldownbtn.config(image = self.window.voldownpress))
    self.window.voldownbtn.bind("<ButtonRelease-1>", lambda x : self.volume_down())
    #channel toggle
    self.window.chnupbtn.bind("<Enter>", lambda x : self.window.chnupbtn.config(image = self.window.chnuphov))
    self.window.chnupbtn.bind("<Leave>", lambda x : self.window.chnupbtn.config(image = self.window.chnupup))
    self.window.chnupbtn.bind("<Button-1>", lambda x : self.window.chnupbtn.config(image = self.window.chnuppress))
    self.window.chnupbtn.bind("<ButtonRelease-1>", lambda x : self.channel_up())
    self.window.chndownbtn.bind("<Enter>", lambda x : self.window.chndownbtn.config(image = self.window.chndownhov))
    self.window.chndownbtn.bind("<Leave>", lambda x : self.window.chndownbtn.config(image = self.window.chndownup))
    self.window.chndownbtn.bind("<Button-1>", lambda x : self.window.chndownbtn.config(image = self.window.chndownpress))
    self.window.chndownbtn.bind("<ButtonRelease-1>", lambda x : self.channel_down())
    #also, make sure video is playing
    """self.window.video0.bind("<<AdOver>>", self.window.player0.play())
    self.window.video1.bind("<<AdOver>>", self.window.player1.play())
    self.window.video2.bind("<<AdOver>>", self.window.player2.play())
    self.window.video3.bind("<<AdOver>>", self.window.player3.play())"""
    #also, close program and all threads when window terminated
    self.window.protocol('WM_DELETE_WINDOW', exit)
