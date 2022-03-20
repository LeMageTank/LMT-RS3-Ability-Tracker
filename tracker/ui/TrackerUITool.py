import tkinter
import importlib
import os
import traceback
from PIL import Image, ImageDraw, ImageTk


class TrackerUITool:
    def __init__(self, configuration, control_queue, tool_config):
        self._configuration = configuration
        self._control_queue = control_queue
        self._root = tkinter.Tk()
        self._update_interval = configuration['actiontracker-update-interval']
        self._width = 1
        self._height = 1
        self._tool_ui = self.load_tool(tool_config)
        self._root.title('Ability Tracker: ' + tool_config['file-name'])
        self._root.attributes('-topmost', configuration['actiontracker-always-on-top'])
        self._root.iconphoto(False,ImageTk.PhotoImage(file=configuration['application-icon-file']))
        self._root.bind('<B1-Motion>', self.move_window)
        self._root.configure(background='black')
        self._root.geometry("{}x{}".format(self._width, self._height))
        self._root.protocol('WM_DELETE_WINDOW', self.close)
        
        self._icon_map = self.load_icons(configuration['action-icon-directory']) if tool_config['requires-icons'] else None
        self.update()

    def close(self):
        self._root.destroy()
        
    def move_window(self, event):
        x,y = self._root.winfo_pointerxy()
        self._root.geometry("{}x{}+{}+{}".format(self._width, self._height, x, y))

    def load_tool(self, tool_config):
        tool_import_spec = importlib.util.spec_from_file_location(tool_config['file-name'], self._configuration['tools-path'] + tool_config['file-name'] + '.py')
        tool_module = importlib.util.module_from_spec(tool_import_spec)
        tool_import_spec.loader.exec_module(tool_module)
        tool_ui_class = getattr(tool_module, tool_config['tracker-tool-ui'])
        tool_ui = tool_ui_class(self._configuration, self._root)
        tool_ui.widget.grid(column=0, row=0, sticky=tkinter.W)
        self._width, self._height = tool_ui.shape
        return tool_ui

    def load_icons(self, path):
        icon_map = {}
        for file in os.listdir(path):
            icon = tkinter.PhotoImage(file=(path + file))
            icon_map[file.split('.')[0]] = icon
        return icon_map

    def update(self):
        while self._control_queue.qsize() > 0:
            item = self._control_queue.get()
            self._tool_ui.add_item(item)
        self._tool_ui.draw(self._icon_map)
        self._root.after(self._update_interval, self.update)

    def start(self):
        self._root.mainloop()
