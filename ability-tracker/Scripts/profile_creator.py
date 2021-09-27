from ahk import AHK
from pynput import mouse, keyboard
import pyautogui
import tkinter
from PIL import Image, ImageDraw, ImageTk
import os
import multiprocessing
import json
import time
import numpy as np
from ability import *


class MouseBindSelector:
    def __init__(self,q, abilities):
        self.q = q
        self.abilities = abilities
        self.active = True

    def run(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        while(self.active):
            time.sleep(1)

    def on_click(self, x, y, button, pressed):
        if(pressed):
            if(button == mouse.Button.middle):
                self.popup(x,y)
            elif(button == mouse.Button.right):
                self.active = False
                return False

    def popup(self,x,y):
        screenshot = np.array(pyautogui.screenshot(region=(x-15,y-15,30,30)))
        root = tkinter.Tk()
        root.geometry("150x50+{}+{}".format(x-145,y-45))
        root.attributes('-topmost', True)
        root.iconphoto(False,ImageTk.PhotoImage(file='ability-tracker\\data\\app icons\\icon.png'))
        root.title('Add Mouse-Clicked Ability')
        ability_selection = tkinter.ttk.Combobox(root)
        ability_selection['values'] = tuple(self.abilities)
        ability_selection.pack()
        msbnd = tkinter.Button(root, text='Add', command=lambda : self.add_mousebind(ability_selection.get(), x, y, root, screenshot))
        msbnd.pack()
        root.mainloop()

    def add_mousebind(self, abil, x, y, root, screenshot):
        self.q.put((abil, x, y, screenshot))
        root.destroy()
        


class ProfileCreator:
    def __init__(self, icons_path, profile_path, profile_types, modifier_keys):
        self.abilities = []
        for file in os.listdir(icons_path):
            self.abilities.append(file.split('.')[0])
        self.profile_path = profile_path
        self.profile_types = profile_types
        self.modifier_keys = modifier_keys

        self.clickable_region_path = 'ability-tracker\\data\\saved profile clickables\\{}{}{}.png'

        self.root = tkinter.Tk()
        self.root.geometry('420x500')
        self.root.attributes('-topmost', True)
        self.root.iconphoto(False,ImageTk.PhotoImage(file='ability-tracker\\data\\app icons\\icon.png'))
        self.root.title('Input Profile Creator')

        self.mouse_queue = multiprocessing.Queue()

        self.profile_container = tkinter.Frame(self.root)
        self.profile_container.grid(row=0, sticky=tkinter.W)
        self.mousebind_container = tkinter.Frame(self.root)
        self.mousebind_container.grid(row=1, sticky=tkinter.W)
        self.keybind_container = tkinter.Frame(self.root)
        self.keybind_container.grid(row=2, sticky=tkinter.W)

        
        #### Profile Section ####
        self.profile_label = tkinter.Label(self.profile_container, text="Profile")
        self.profile_label.grid(row=0, column=0, sticky=tkinter.EW, pady=2)

        self.profile_selection = tkinter.ttk.Combobox(self.profile_container)
        self.profile_selection['values'] = self.profile_types
        self.profile_selection.grid(row=0, column=1, sticky=tkinter.EW, pady=2)
        self.profile_selection.current(0)

        self.profile_load_button = tkinter.Button(self.profile_container,
                                                  text="Load",
                                                  command=self.load_profile)
        self.profile_load_button.grid(row=1, column=0, sticky=tkinter.EW, pady=2)
        
        self.profile_save_button = tkinter.Button(self.profile_container,
                                                  text="Save",
                                                  command=self.save_profile)
        self.profile_save_button.grid(row=1, column=1, sticky=tkinter.EW, pady=2)

        self.profile_generate_button = tkinter.Button(self.profile_container,
                                                      text="generate",
                                                      command=self.generate_profile)
        self.profile_generate_button.grid(row=1, column=2, sticky=tkinter.EW, pady=2)
        

        #### Mousebind Section ####
        self.mousebind_label = tkinter.Label(self.mousebind_container, text="Mouse Binds")
        self.mousebind_label.grid(row=0, column=0, sticky=tkinter.EW, pady=2)

        self.mousebind_start_listener = tkinter.Button(self.mousebind_container,
                                                       text="Start Mouse Listener",
                                                       command=self.start_mouse_listener)
        self.mousebind_start_listener.grid(row=0, column=1, sticky=tkinter.EW, pady=2)

        self.mouse_ability_image = ImageTk.PhotoImage(Image.open('ability-tracker\\icons\\Zaros Godsword.png'))
        self.mouse_ability_image_label = tkinter.Label(self.mousebind_container, image=self.mouse_ability_image)
        self.mouse_ability_image_label.grid(row=0, column=2, sticky=tkinter.EW, pady=2)

        self.mousebind_description = tkinter.Label(self.mousebind_container,
                                                   text="Middle mouse to add mousebind, right mouse to stop listener.")
        self.mousebind_description.grid(row=1, column=0, sticky=tkinter.EW,
                                        pady=2, columnspan=2)

        self.mousebind_list = tkinter.Listbox(self.mousebind_container)
        self.mousebind_list.grid(row=2, column=0, sticky=tkinter.EW, pady=2,
                                 columnspan=2, rowspan=5)
        self.mousebind_list.bind('<<ListboxSelect>>', self.mousebind_select)

        self.mousebind_delete = tkinter.Button(self.mousebind_container,
                                                       text="Delete",
                                                       command=self.delete_mousebind)
        self.mousebind_delete.grid(row=2, column=2, sticky=tkinter.NSEW, pady=2)

        
        #### Keybind Selection ####
        self.keybind_label = tkinter.Label(self.keybind_container, text="Key Binds")
        self.keybind_label.grid(row=0, column=0, sticky=tkinter.EW, pady=2)

        self.keybind_list = tkinter.Listbox(self.keybind_container)
        self.keybind_list.grid(row=2, column=0, sticky=tkinter.EW, pady=2,
                                 columnspan=3, rowspan=5)


        self.keybind_add = tkinter.Button(self.keybind_container,
                                                       text="Add",
                                                       command=self.add_keybind)
        self.keybind_add.grid(row=1, column=0, sticky=tkinter.EW, pady=2)

        self.keybind_key = tkinter.Entry(self.keybind_container, width=10)
        self.keybind_key.grid(row=1, column=1, sticky=tkinter.EW, pady=2)

        self.keybind_modifier_selection = tkinter.ttk.Combobox(self.keybind_container)
        self.keybind_modifier_selection['values'] = self.modifier_keys
        self.keybind_modifier_selection.grid(row=1, column=2, sticky=tkinter.EW, pady=2)

        self.keybind_ability_selection = tkinter.ttk.Combobox(self.keybind_container)
        self.keybind_ability_selection['values'] = self.abilities
        self.keybind_ability_selection.grid(row=1, column=3, sticky=tkinter.EW, pady=2)
        
        self.keybind_delete = tkinter.Button(self.keybind_container,
                                                       text="Delete",
                                                       command=self.delete_keybind)
        self.keybind_delete.grid(row=2, column=3, sticky=tkinter.NSEW, pady=2)
        

        # Load default profile
        self.load_profile()
        self.loop()
        self.root.mainloop()

    def loop(self):
        if(self.mouse_queue.qsize() > 0):
            self.add_mousebind(self.mouse_queue.get())
        self.root.after(25, self.loop)

    def load_profile(self):
        f = open(self.profile_path + self.profile_selection.get() + '.json', 'r+')
        self.profile_data = json.loads("".join(f.readlines()))
        f.close()

        for i in range(len(self.profile_data['keypress_activated'])):
                self.profile_data['keypress_activated'][i] = KeypressAbility(self.profile_data['keypress_activated'][i])
        for i in range(len(self.profile_data['mouse_activated'])):
                self.profile_data['mouse_activated'][i] = ClickableAbility(self.profile_data['mouse_activated'][i])

        self.update_mousebinds()
        self.update_keybinds()

    def save_profile(self):
        saved_profile_data = {'keypress_activated':[], 'mouse_activated':[]}
        for i in range(len(self.profile_data['keypress_activated'])):
                saved_profile_data['keypress_activated'].append(self.profile_data['keypress_activated'][i].to_dict())
        for i in range(len(self.profile_data['mouse_activated'])):
                saved_profile_data['mouse_activated'].append(self.profile_data['mouse_activated'][i].to_dict())

        f = open(self.profile_path + self.profile_selection.get() + '.json', 'w+')
        saved_profile_data = json.dumps(saved_profile_data)
        f.write(saved_profile_data)
        f.close()

        self.load_profile()

    def generate_profile(self):
        self.profile_data = {'keypress_activated':[], 'mouse_activated':[]}
        self.save_profile()

    def start_mouse_listener(self):
        mouse = MouseBindSelector(self.mouse_queue, self.abilities)
        mouse_process = multiprocessing.Process(target=mouse.run)
        mouse_process.start()

    def add_mousebind(self, binding):
        abil = ClickableAbility({'ability':binding[0], 'x':binding[1]-15, 'y': binding[2]-15,
                    'w':binding[1]+15, 'h':binding[2]+15})
        image = Image.fromarray(binding[3])
        image.save(self.clickable_region_path.format(self.profile_selection.get(),abil._name, str(abil._x1)+ '-' + str(abil._y1)))
        abil.image = ImageTk.PhotoImage(image=image)
        self.profile_data['mouse_activated'].insert(0, abil)
        self.update_mousebinds()

    def delete_mousebind(self):
        if(len(self.mousebind_list.curselection()) > 0):
            try:
                abil = self.profile_data['mouse_activated'][self.mousebind_list.curselection()[0]]
                os.remove(self.clickable_region_path.format(self.profile_selection.get(),abil._name, str(abil._x1)+ '-' + str(abil._y1)))
            except:
                ""
            del self.profile_data['mouse_activated'][self.mousebind_list.curselection()[0]]
            self.update_mousebinds()

    def delete_keybind(self):
        if(len(self.keybind_list.curselection()) > 0):
            del self.profile_data['keypress_activated'][self.keybind_list.curselection()[0]]
            self.update_keybinds()

    def add_keybind(self):
        key = self.keybind_key.get()
        modifier = self.keybind_modifier_selection.get()
        if(modifier == ''):
            modifier = None
        ability = self.keybind_ability_selection.get()
        self.profile_data['keypress_activated'].insert(0, KeypressAbility({
            'ability':ability, 'key':key, 'modifier':modifier}))
        self.update_keybinds()

    def update_mousebinds(self):
        self.mousebind_list.delete(0, self.mousebind_list.size()-1)
        for i in range(len(self.profile_data['mouse_activated'])):
            self.mousebind_list.insert(i, str(self.profile_data['mouse_activated'][i]))

    def update_keybinds(self):
        self.keybind_list.delete(0, self.keybind_list.size()-1)
        for i in range(len(self.profile_data['keypress_activated'])):
            self.keybind_list.insert(i, str(self.profile_data['keypress_activated'][i]))

    def mousebind_select(self, event):
        ability = self.profile_data['mouse_activated'][self.mousebind_list.curselection()[0]]
        try:
            if(ability.image is None):
                ability.image = tkinter.PhotoImage(file=self.clickable_region_path.format(self.profile_selection.get(),ability._name, str(ability._x1)+ '-' + str(ability._y1)))
            self.mouse_ability_image = ability.image
            self.mouse_ability_image_label.configure(image=self.mouse_ability_image)
        except:
            ability.image = tkinter.PhotoImage(file='ability-tracker\\icons\\{}.png'.format(ability._name))
            self.mouse_ability_image = ability.image
            self.mouse_ability_image_label.configure(image=self.mouse_ability_image)


profile_types = ['dw_melee', '2h_melee', 'dw_range', '2h_range', 'dw_magic', '2h_magic']
modifier_keys=['','alt','shift','ctrl']

if __name__ == '__main__':
    profile_creator = ProfileCreator('ability-tracker\\icons\\', 'ability-tracker\\data\\saved profiles\\', profile_types, modifier_keys)









        
