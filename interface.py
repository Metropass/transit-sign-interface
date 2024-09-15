import tkinter as tk
import time
from typing import Callable
from PIL import Image, ImageTk
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer




FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=True, enumerable=False):
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



class SignInterface(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg="WHITE")
        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.create_items()
    
    def create_items(self):
        self.label_gif1 = tk.Label(self.main_frame, bg="WHITE", border=0)
        self.label_gif1.grid(column=0, row=0)
        self.gif1_frames = self._get_frame(".//images//animated//tv_collect_pepp.webp")
        root.after(100, self._play_gif, self.label_gif1, self.gif1_frames)
        self.label_gif1.config(image=self.gif1_frames[4])
        self.button = tk.Button(self.main_frame, text="Button", width=10, height=2)
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
        for frame in frames:
            root.after(total_delay, self._next_frame, frame, label, frames)
            total_delay += delay_frames
        root.after(total_delay, self._next_frame, frame, label, frames, True)
    
    def _next_frame(self, frame, label, frames, restart=False):
        if restart:
            root.after(1, self._play_gif, label, frames)
            return
        
        label.config(image=frame)
    
    
root = tk.Tk()
root.title("Meme")
root.geometry("1200x800")
root.resizable(width=False, height=False)

instance_of_app = SignInterface(root)
root.mainloop()
        
'''
font_load = loadfont(".//fonts//TorontoSubwayRegular.ttf", True, False)




GIF_pepp = ".//images//animated//tv_collected_pepp.gif"
WEBP_pepp = ".//images//animated//tv_collect_pepp.webp"

'''