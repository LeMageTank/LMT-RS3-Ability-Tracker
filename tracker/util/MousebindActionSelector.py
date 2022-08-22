from pynput import mouse
from PIL import ImageTk
import multiprocessing
import tkinter
import time
import os

def run_mousebind_action_selector(mousebind_output_queue, control_input_queue, configuration):
    mouse_bind_action_selector = MouseBindActionSelector(mousebind_output_queue, control_input_queue, configuration)
    mouse_bind_action_selector.run()

class MouseBindActionSelector:
    def __init__(self, output_queue, input_queue, configuration):
        self._configuration = configuration
        self._output_queue = output_queue
        self._input_queue = input_queue
        self._action_list = self.load_action_list()
        self._action_shape = configuration['actiontracker-icon-shape']
        self._active = True

    def run(self):
        self._mouse_listener = mouse.Listener(on_click=self.on_click)
        self._mouse_listener.start()
        while(self._active):
            time.sleep(1)

    def load_action_list(self):
        actions = []
        for file in os.listdir(self._configuration['action-icon-directory']):
            actions.append(file.split('.')[0])
        return actions

    def on_click(self, x, y, button, pressed):
        if self._active is False:
            return False
        if self._input_queue.qsize() > 0:
            message = self._input_queue.get()
            if message == 'exit':
                self._active = False
                return False
        if pressed:
            if button == mouse.Button.right:
                self.popup(x,y)

    def popup(self,x,y):
        root = tkinter.Tk()
        root.geometry("150x70+{}+{}".format(x-145,y-45))
        root.attributes('-topmost', True)
        root.iconphoto(False, ImageTk.PhotoImage(file=self._configuration['application-icon-file']))
        root.title('Add Mousebind Action')
        action_selection = tkinter.ttk.Combobox(root)
        action_selection['values'] = self._action_list
        action_selection.pack()
        mousebind_add_button = tkinter.Button(root, text='Add', command=lambda : self.add_mousebind_to_queue(action_selection.get(), x, y, root))
        mousebind_stop_button = tkinter.Button(root, text='Stop Mouse Listener', command=lambda : self.mousebind_selector_exit(root))
        mousebind_add_button.pack()
        mousebind_stop_button.pack()
        root.mainloop()

    def mousebind_selector_exit(self, root):
        self._active = False
        root.destroy()
        
        
    def add_mousebind_to_queue(self, action, x, y, root):
        self._output_queue.put((action, x, y))
        root.destroy()
