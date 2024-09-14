from tkinter import *
from tkinter import font
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




class TestLabel(Label):
    def __init__(self, master, filename):
        img = Image.open(filename)
        seq = []
        try:
            while 1:
                seq.append(img.copy())
                img.seek(len(seq))
        except EOFError:
            pass
        try:
            self.delay = img.info['duration']
        except KeyError:
            self.delay = 100
        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]
        Label.__init__(self, master, image=self.frames[0])
        
        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))
        self.idx = 0
        self.cancel = self.after(self.delay, self.play)
        
    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)
        
    def update_image(self, filename):
        img = Image.open(filename)
        seq = []
        try:
            while 1:
                seq.append(img.copy())
                img.seek(len(seq))
        except EOFError:
            pass
        try:
            self.delay = img.info['duration']
        except KeyError:
            self.delay = 100
        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]
        
        
font_load = loadfont(".//fonts//TorontoSubwayRegular.ttf", True, False)

root = Tk()
root.attributes('-fullscreen', True)
root.title("test for tk")
print(font.families(root=root))


anim = TestLabel(root, ".//images//animated//tv_collect_pepp.webp")
anim.grid(row=0, column=5)

def stop_anim():
    print(type(anim))
    anim.after_cancel(anim.cancel)
    
    
def anim_replace():
    global anim
    if anim is not None:
        anim.after(ms=0, func=anim.destroy())
        anim = None
    new_anim = TestLabel(root, ".//images//animated//tv_collected_pepp.gif")
    new_anim.grid(row=0, column=5)
    anim = new_anim
    
    

Button(root, text="stop", command=stop_anim).grid(row=1, column=1)
Button(root, text="replace", command=anim_replace).grid(row=1, column=2)
Label(root, text="This is a test of the font family", font=font.families(root=root)[-1]).grid(row=2, column=3)

root.mainloop()
