from pynput import mouse, keyboard
import pyautogui
import tkinter
from PIL import Image, ImageDraw, ImageTk
import os
import multiprocessing
import json
import time
import numpy as np
from tracker.action import *


class MouseBindSelector:
    def __init__(self, queue, configuration, action_list):
        self.configuration = configuration
        self.queue = queue
        self.action_list = tuple(action_list)
        self.action_shape = self.configuration['actiontracker-icon-shape']
        self.active = True

    def run(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        while(self.active):
            time.sleep(1)

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.middle:
                self.popup(x,y)
            elif button == mouse.Button.right:
                self.active = False
                return False

    def popup(self,x,y):
        screenshot = np.array(pyautogui.screenshot(region=(x-self.action_shape[0]/2,y-self.action_shape[1]/2,
                                                           self.action_shape[0],self.action_shape[1])))
        root = tkinter.Tk()
        root.geometry("150x50+{}+{}".format(x-145,y-45))
        root.attributes('-topmost', True)
        root.iconphoto(False,ImageTk.PhotoImage(file=self.configuration['application-icon-file']))
        root.title('Add Mousebind Action')
        action_selection = tkinter.ttk.Combobox(root)
        action_selection['values'] = self.action_list
        action_selection.pack()
        mousebind_add_button = tkinter.Button(root, text='Add', command=lambda : self.add_mousebind(action_selection.get(), x, y, root, screenshot))
        mousebind_add_button.pack()
        root.mainloop()

    def add_mousebind(self, action, x, y, root, screenshot):
        self.queue.put((action, x, y, screenshot))
        root.destroy()

class MouseAdrenSelector:
    def __init__(self, queue, configuration):
        self.configuration = configuration
        self.queue = queue
        self.active = True
        self.coords = []

    def run(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        while(self.active):
            time.sleep(1)

    def on_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.right:
            self.coords.append((x,y))
            if len(self.coords) == 2:
                self.queue.put((self.coords[0][0], self.coords[0][1], self.coords[1][0]-self.coords[0][0], 1))
                self.active = False
                return False


class ProfileCreator:
    def __init__(self, configuration):
        self.configuration = configuration
        self.actions = []
        for file in os.listdir(self.configuration['action-icon-directory']):
            self.actions.append(file.split('.')[0])
        self.profile_types = self.configuration['profile-types']
        self.modifier_keys = self.configuration['modifier-keys']

        self.clickable_region_path = self.configuration['clickable-region-file-template']

        self.root = tkinter.Tk()
        self.root.geometry('420x700')
        self.root.attributes('-topmost', True)
        self.root.iconphoto(False,ImageTk.PhotoImage(file=self.configuration['application-icon-file']))
        self.root.title('Input Profile Creator')

        self.mouse_queue = multiprocessing.Queue()
        self.adren_queue = multiprocessing.Queue()

        self.build_profile_selector()
        self.build_mousebind_creator()
        self.build_keybind_creator()
        self.build_misc_tools()
        
        self.load_profile()
        
    def run(self):
        self.loop()
        self.root.mainloop()

    def build_profile_selector(self):
        self.profile_container = tkinter.Frame(self.root)
        self.profile_container.grid(row=0, sticky=tkinter.EW)
        
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

    def build_mousebind_creator(self):
        self.mousebind_container = tkinter.Frame(self.root)
        self.mousebind_container.grid(row=1, sticky=tkinter.EW)
        self.mousebind_label = tkinter.Label(self.mousebind_container, text="Mousebinds")
        self.mousebind_label.grid(row=0, column=0, sticky=tkinter.EW, pady=2)
        self.mousebind_start_listener = tkinter.Button(self.mousebind_container,
                                                       text="Start Mouse Listener",
                                                       command=self.start_mouse_listener)
        self.mousebind_start_listener.grid(row=0, column=1, sticky=tkinter.EW, pady=2)
        self.mouse_action_image = ImageTk.PhotoImage(Image.open(self.configuration['profile-creator-default-icon-file']))
        self.mouse_action_image_label = tkinter.Label(self.mousebind_container, image=self.mouse_action_image)
        self.mouse_action_image_label.grid(row=0, column=2, sticky=tkinter.EW, pady=2)
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

    def build_keybind_creator(self):
        self.keybind_container = tkinter.Frame(self.root)
        self.keybind_container.grid(row=2, sticky=tkinter.EW)
        self.keybind_label = tkinter.Label(self.keybind_container, text="Keybinds")
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
        self.keybind_action_selection = tkinter.ttk.Combobox(self.keybind_container)
        self.keybind_action_selection['values'] = self.actions
        self.keybind_action_selection.grid(row=1, column=3, sticky=tkinter.EW, pady=2)
        self.keybind_delete = tkinter.Button(self.keybind_container,
                                                       text="Delete",
                                                       command=self.delete_keybind)
        self.keybind_delete.grid(row=2, column=3, sticky=tkinter.NSEW, pady=2)

    def build_misc_tools(self):
        self.misc_container = tkinter.Frame(self.root)
        self.misc_container.grid(row=3, sticky=tkinter.EW)

        self.adrenaline_label = tkinter.Label(self.misc_container, text="Adrenaline Reader")
        self.adrenaline_label.grid(row=0, column=0, sticky=tkinter.EW, pady=2)

        self.adrenaline_listener_button = tkinter.Button(self.misc_container,
                                                         text="Start Mouse Listener",
                                                         command=self.start_adrenaline_listener)
        self.adrenaline_listener_button.grid(row=0, column=1, sticky=tkinter.EW, pady=2)
        self.adrenaline_description = tkinter.Label(self.misc_container,
                                                   text="Right click both ends of the adrenaline bar to mark its position.")
        self.adrenaline_description.grid(row=1, column=0, sticky=tkinter.EW, pady=2,
                                          rowspan=2,columnspan=3)
        self.adrenaline_display = tkinter.Label(self.misc_container, text="")
        self.adrenaline_display.grid(row=3, column=0, sticky=tkinter.EW, pady=2)

    def loop(self):
        if self.mouse_queue.qsize() > 0:
            self.add_mousebind(self.mouse_queue.get())
        if self.adren_queue.qsize() > 0:
            self.update_adrenaline_bar(self.adren_queue.get())
        self.root.after(25, self.loop)

    def load_profile(self):
        with open(self.configuration['saved-profiles-directory'] + self.profile_selection.get() + '.json', 'r+') as file:
            self.profile_data = json.loads("".join(file.readlines()))
            for i in range(len(self.profile_data['keybinds'])):
                    self.profile_data['keybinds'][i] = KeybindAction(self.profile_data['keybinds'][i])
            for i in range(len(self.profile_data['mousebinds'])):
                    self.profile_data['mousebinds'][i] = MousebindAction(self.profile_data['mousebinds'][i])

        self.update_mousebinds()
        self.update_keybinds()

    def save_profile(self):
        saved_profile_data = {'keybinds':[], 'mousebinds':[], 'adrenaline-bar':[]}
        saved_profile_data['adrenaline-bar'] = self.profile_data['adrenaline-bar']
        for i in range(len(self.profile_data['keybinds'])):
                saved_profile_data['keybinds'].append(self.profile_data['keybinds'][i].to_dict())
        for i in range(len(self.profile_data['mousebinds'])):
                saved_profile_data['mousebinds'].append(self.profile_data['mousebinds'][i].to_dict())

        with open(self.configuration['saved-profiles-directory'] + self.profile_selection.get() + '.json', 'w+') as file:
            saved_profile_data = json.dumps(saved_profile_data)
            file.write(saved_profile_data)

        self.load_profile()

    def generate_profile(self):
        self.profile_data = {'keybinds':[], 'mousebinds':[], 'adrenaline-bar':[]}
        self.save_profile()

    def start_mouse_listener(self):
        mouse = MouseBindSelector(self.mouse_queue, self.configuration, self.actions)
        mouse_process = multiprocessing.Process(target=mouse.run)
        mouse_process.start()

    def start_adrenaline_listener(self):
        mouse = MouseAdrenSelector(self.adren_queue, self.configuration)
        mouse_process = multiprocessing.Process(target=mouse.run)
        mouse_process.start()

    def add_mousebind(self, binding):
        action = MousebindAction({'action':binding[0], 'x1':binding[1]-15, 'y1': binding[2]-15,
                    'x2':binding[1]+15, 'y2':binding[2]+15})
        image = Image.fromarray(binding[3])
        image.save(self.clickable_region_path.format(self.profile_selection.get(),action.action, str(action.x1)+ '-' + str(action.y1)))
        action.image = ImageTk.PhotoImage(image=image)
        self.profile_data['mousebinds'].insert(0, action)
        self.update_mousebinds()

    def delete_mousebind(self):
        if len(self.mousebind_list.curselection()) > 0:
            try:
                action = self.profile_data['mousebinds'][self.mousebind_list.curselection()[0]]
                os.remove(self.clickable_region_path.format(self.profile_selection.get(),action.action, str(action.x1)+ '-' + str(action.y1)))
            except:
                pass
            del self.profile_data['mousebinds'][self.mousebind_list.curselection()[0]]
            self.update_mousebinds()

    def delete_keybind(self):
        if len(self.keybind_list.curselection()) > 0:
            del self.profile_data['keybinds'][self.keybind_list.curselection()[0]]
            self.update_keybinds()

    def add_keybind(self):
        key = self.keybind_key.get()
        modifier = self.keybind_modifier_selection.get()
        if modifier == '':
            modifier = None
        action = self.keybind_action_selection.get()
        self.profile_data['keybinds'].insert(0, KeybindAction({
            'action':action, 'key':key, 'modifier':modifier}))
        self.update_keybinds()

    def update_adrenaline_bar(self, region):
        self.profile_data['adrenaline-bar'] = region
        self.adrenaline_display.text = "Location recorded"

    def update_mousebinds(self):
        self.mousebind_list.delete(0, self.mousebind_list.size()-1)
        for i in range(len(self.profile_data['mousebinds'])):
            self.mousebind_list.insert(i, str(self.profile_data['mousebinds'][i]))

    def update_keybinds(self):
        self.keybind_list.delete(0, self.keybind_list.size()-1)
        for i in range(len(self.profile_data['keybinds'])):
            self.keybind_list.insert(i, str(self.profile_data['keybinds'][i]))

    def mousebind_select(self, event):
        action = self.profile_data['mousebinds'][self.mousebind_list.curselection()[0]]
        try:
            if(action.image is None):
                action.image = tkinter.PhotoImage(file=self.configuration['clickable-region-file-template'].format(self.profile_selection.get(),action.action,
                                                                                                                    str(action.x1)+ '-' + str(action.y1)))
            self.mouse_action_image = action.image
            self.mouse_action_image_label.configure(image=self.mouse_action_image)
        except:
            action.image = tkinter.PhotoImage(file=self.configuration['action-icon-file-template'].format(action.action))
            self.mouse_action_image = action.image
            self.mouse_action_image_label.configure(image=self.mouse_action_image)

def run_profilecreator(configuration):
    profile_creator = ProfileCreator(configuration)
    profile_creator.run()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    configuration = None
    with open('config.json', 'r+') as config_file:
        configuration = json.loads("".join(config_file.readlines()))
    profile_creator = ProfileCreator(configuration)
    profile_creator.run()









        
