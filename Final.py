import keyboard
import pymem
import pymem.process
import time
import threading
from threading import Thread
import tkinter as tk  # for python 3
import pygubu
from tkinter import Tk, Button, Frame, Entry, END



pm = pymem.Pymem("csgo.exe")

# Offsets 01/17/18
dwLocalPlayer = (0xAA9AB4)
dwForceAttack = (0x2EC47F8)
m_iCrosshairId = (0xB2A4)
m_fFlags = (0x100)
dwForceJump = (0x4F1970C)
m_iGlowIndex = (0xA310)
dwEntityList = (0x4A8473C)
m_iTeamNum = (0xF0)
dwGlowObjectManager = (0x4F9F800)
dwEntityList = (0x4A8246C)
dwGlowObjectManager = (0x4FB14E8)
m_iGlowIndex = (0xA310)
m_iTeamNum = (0xF0)


#Colors min 0 max 1 supports decimals
t_red = float(1)
t_green = float(0)
t_blue = float(0)
t_alpha = float(1)
ct_red = float(0)
ct_green = float(0)
ct_blue = float(1)
ct_alpha = float(1)


aim_key = "p" # Aim key, while pressed, triggerbot is activated.]
hop_key = "o"
toggle_key = "l"

globvar = 0




client = pymem.process.module_from_name(pm.process_id, "client.dll")


class Application:
    def __init__(self, master):
            
        self.master = master
        self.builder = builder = pygubu.Builder() # Create builder
        builder.add_from_file('menu.ui') # Load ui file.


        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('menu.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Jabrony by Boxy Monkey', master)

        builder.connect_callbacks(self)

    def make_widgets(self):
        self.parent.title("Simple Prog")

    def on_glow_clicked(self):
        global globvar    # Needed to modify global copy of globvar
        print("on_glow_clicked")
        checked = self.builder.get_variable('checked') # Get variable
        print(checked.get())
        globvar = checked.get()
        toggled = True
        print(globvar)




def walls():
    global globvar
    toggled = False

    while True:
        try:
            if globvar == 1:
                if toggled == True:
                    pass
                else:
                    toggled = True
                    print("Walls has been toggled on.")
                    time.sleep(1)
            else:
                if toggled == False:
                    pass
                else:
                    toggled = False
                    print("Walls has been toggled off.")
                    time.sleep(1)
        except RuntimeError: # Keyboard throws RuntimeError on key press.
            pass

        if toggled:
            try:
                for i in range(0, 32): 
                    glow_player_glow_index = pm.read_int(get_glow_current_player(i) + m_iGlowIndex)
                    entity_team_id = pm.read_int(get_glow_current_player(i) + m_iTeamNum)

                    if entity_team_id is 2: # Terrorist
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x4)), t_red)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x8)), t_green)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0xC)), t_blue)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x10)), t_alpha)
                        pm.write_int((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x24)), 1)

                    if entity_team_id is 3: # Counter-Terrorist
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x4)), ct_red) 
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x8)), ct_green)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0xC)), ct_blue)
                        pm.write_float((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x10)), ct_alpha)
                        pm.write_int((get_glow_pointer() + ((glow_player_glow_index * 0x38) + 0x24)), 1)

            except pymem.exception.MemoryReadError: # Attempted to read invalid entity.
                pass

def get_glow_current_player(index):
    return pm.read_int(client + dwEntityList + index * 0x10)

def get_glow_pointer():
    return pm.read_int(client + dwGlowObjectManager)




if __name__ == '__main__':
    Thread(target = walls).start()
    root = tk.Tk()
    root.title("Jabrony")
    app = Application(root)
    root.mainloop()
