import tkinter as tk
from tkinter import font as font
import time
from typing import Callable
from PIL import Image, ImageTk
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from functools import partial




FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20




class SignInterface(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg="WHITE")
        self.loaded_fonts = self._loadfont(fontpath=".//fonts//TorontoSubwayRegular.ttf", private=True, enumerable=False)
        print(font.families())
        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.create_items()
    
    def create_items(self):
        
        self.swap = False
        self.label_gif1 = tk.Label(self.main_frame, bg="WHITE", border=0)
        self.label_gif1.grid(column=0, row=0)
        self.label_gif2 = None
        self.gif1_frames = self._get_frame(".//images//animated//tv_collect_pepp.webp")
        self.gif2_frames = None
        #root.after(100, self._play_gif, self.label_gif1, self.gif1_frames)
        self.main_frame.after(100, self._play_gif, self.label_gif1, self.gif1_frames)
        
        self.text_label = tk.Label(self.main_frame, text="Test Text", font=font.families(root=self.main_frame)[-1]).grid(row=0, column=3)
        self.button = tk.Button(self.main_frame, text="Button", width=10, height=2, command=partial(self._replace_gif, newpic=".//images//animated//tv_idle.webp"))
        self.button.grid(column=0, row=1)
        
    def _get_frame(self, img):
        with Image.open(img) as gif:
            index = 0
            frames = []
            while True:
                try:
                    gif.seek(index)
                    frame = ImageTk.PhotoImage(gif)
                    frames.append(frame)
                except EOFError:
                    break
                index += 1
            return frames
    
    def _play_gif(self, label, frames):
        total_delay = 10
        delay_frames = 50
        for framei in frames:
            self.main_frame.after(total_delay, self._next_frame, framei, label, frames)
            total_delay += delay_frames
        root.after(total_delay, self._next_frame, framei, label, frames, True)
    
    def _next_frame(self, frame, label, frames, restart=False):
        if restart:
            root.after(1, self._play_gif, label, frames)
            return
        label.config(image=frame)
    
    def _replace_gif(self, newpic):
        if self.swap is True:
            newpic = ".//images//animated//tv_collect_pepp.webp"
            self.swap = False
        else:
            newpic=".//images//animated//tv_idle.webp"
            self.swap = True
        if self.gif2_frames is None:
            self.label_gif2 = tk.Label(self.main_frame, bg="WHITE", border=0)
            self.label_gif2.grid(column=0, row=0)
            self.gif2_frames = self._get_frame(newpic)
            self.main_frame.after(100, self._play_gif, self.label_gif2, self.gif2_frames)
            self.label_gif1.update()
            self.label_gif1 = None
            return
        elif self.gif1_frames is None:
            self.label_gif1 = tk.Label(self.main_frame, bg="WHITE", border=0)
            self.label_gif1.grid(column=0, row=0)
            self._get_frame(newpic)
            self.main_frame.after(100, self._play_gif, self.label_gif1, self.gif1_frames)
            self.label_gif2.update()
            self.label_gif2 = None
            return
        
        
    def _loadfont(self, fontpath, private=True, enumerable=False):
        '''
        Makes fonts located in file `fontpath` available to the font system.

        `private`     if True, other processes cannot see this font, and this
                        font will be unloaded when the process dies
        `enumerable`  if True, this font will appear when enumerating fonts

        See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

        '''
        if isinstance(fontpath, bytes):
            pathbuf = create_string_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExA
        elif isinstance(fontpath, str):
            pathbuf = create_unicode_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('fontpath must be of type str or unicode')
        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
        return bool(numFontsAdded)

    
    
root = tk.Tk()
root.title("Meme")
root.geometry("1200x800")
root.resizable(width=False, height=False)

instance_of_app = SignInterface(root)
root.mainloop()
        
