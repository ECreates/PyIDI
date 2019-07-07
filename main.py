import pygame as pg
import sys
import time

pg.init()
pg.font.init()

default_size = width, height = 1280, 720
fill_color = 255, 255, 255

class ButtonHeader:
    """
    Class for button ribbon at top of window.
    """
    def __init__(self):
        self.headrect = pg.Rect()

    def update_buttons(self, button, action="disable"):
        if action == "disable":
            pass

class Button:
    def __init__(self, size, text, action):
        self.button_rect = None

    def modify_size(self, new_size):
        pass

class Measure:
    pitch_data = [["c4", 112],["d4", 100],["e4", 88],["f4", 76],["g4", 64],
                ["a4", 52],["b4", 40],["c5", 28],["d5", 16],["e5", 4],
                ["f5", -8],["g5", -20],["a5", -32]]
                # TODO: Change from hard coded values

    current_offset = 0

    def __init__(self, image="staff.png"):
        self.img = pg.image.load(image)  # ALWAYS 400x100
        # FIX RECTS
        self.offset = Measure.current_offset
        Measure.current_offset += 1
        self.position = (default_size[0]//16 + 400 * self.offset,
                        default_size[1]//2.5)
        print(self.position)
        # rect_w, rect_h = self.img.get_size() # Will always be 400x100
        self.rect = pg.Rect(self.position[0], self.position[1] - 50, 400, 200)
        
        rail_x = self.position[0]
        div = 1
        self.note_rails = [NoteRail(self, data, rail_x, div)
                         for data in Measure.pitch_data]
        self.events = []
    
    def change_div(self):
        pass

class NoteRail:

    def __init__(self, parent, pitch_data, x, division):
        self.parent_measure = parent
        self.pitch_name = pitch_data[0]
        self.x = x
        self.y = parent.position[1] + pitch_data[1]
        if self.pitch_name == "f5":
            print(self.y)
        self.rect = pg.Rect(x, self.y, 400, 12)
        self.max_division = division
        self.notes = [None]

    def place_note(self, mouse_x, clicked):
        if clicked and self.notes[0] == None: # TODO: Add specific note positions
            print(self.pitch_name)
            note = Note(self.x + self.x//2, self.y)
            self.notes[0] = note
            note_blits.append(note)
        else:
            temp_note = Note(self.x + self.x//2, self.y, temp=True)
            temp_blits.append(temp_note)

class Note:
    def __init__(self, x, y, temp=False):
        if temp:
            self.img = pg.image.load("whole_note_temp.png")  # ALWAYS 25wx20h
        else:
            self.img = pg.image.load("whole_note.png")
        self.position = (x, y)

measures = [Measure("staff_first.png")]
buttons = []
note_blits = []
temp_blits = []

def modify_window(size, fill):
    window = pg.display.set_mode(size)

    title = pg.font.Font("slkscre.ttf", size[1]//24).render("MIDI Master",
                                                            True, (1,1,1))
    title_pos = (size[0]/2 - title.get_rect().size[0]//2, size[1]//32)

    for measure in measures:
        new_pos = (size[0]//16 + 400 * measure.offset, size[1]//2.5)
        measure.position = new_pos
        measure.rect = pg.Rect(new_pos[0], new_pos[1], 400, 100)

    return window, title, title_pos


window, title, title_pos = modify_window(default_size, fill_color)

pg.display.set_caption("MIDI Master")
icon = pg.image.load("icon.png")
pg.display.set_icon(icon)

def check_mouse(clicked=False):
    mouse_x, mouse_y = pg.mouse.get_pos()
    for button in buttons:
        break
    for measure in measures:
        if measure.rect.collidepoint(mouse_x, mouse_y):
            for rail in measure.note_rails:
                if rail.rect.collidepoint(mouse_x, mouse_y):
                    rail.place_note(mouse_x, clicked)

fps_counted = False
start_time = None
completed_frames = 0
count_fps = False

while True:
    if count_fps:
        if not fps_counted:
            fps_counted = True
            start_time = time.perf_counter()
            completed_frames = 0
        else:
            completed_frames += 1
        
        if time.perf_counter() - start_time >= 1:
            fps_counted = False
            print("FPS: ", completed_frames)

    mouse_checked = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            check_mouse(clicked=True)
            mouse_checked = True

    if not mouse_checked:
        check_mouse()

    window.fill(fill_color)
    window.blit(title, title_pos)
    for measure in measures:
        window.blit(measure.img, measure.position)
    for note in note_blits:
        window.blit(note.img, note.position)
    for temp in temp_blits:
        window.blit(temp.img, temp.position)
        temp_blits.clear()
    pg.display.flip()
