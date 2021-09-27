from ahk import AHK
from pynput import mouse, keyboard
import pyautogui
import multiprocessing
import os
import json
import time
import tkinter
from PIL import Image, ImageDraw
import numpy as np

class Ability:
    def __init__(self, deserializeable):
        self.name = deserializeable['ability']
        self.ability_type = deserializeable['type']
        self.cooldown = deserializeable['cooldown']
        self.incurs_gcd = deserializeable['incurs_gcd']
        self.last_use = 0

    def activate(self, activation_time):
        if(activation_time - self.last_use > self.cooldown):
            self.last_use = activation_time
            return True
        else:
            return False

    def __str__(self):
        return "{} : {}".format(self.name, self.ability_type)

class AbilityReference:
    def __init__(self, name):
        self._name = name
        self.image = None

    def __str__(self):
        return self._name

class ClickableAbility(AbilityReference):
    def __init__(self, deserializeable):
        super().__init__(deserializeable['ability'])
        self._x1 = deserializeable['x']
        self._y1 = deserializeable['y']
        self._x2 = deserializeable['w']
        self._y2 = deserializeable['h']
            #      y1
            #   x1    x2
            #      y2

    def lt(self, other):
        if(isinstance(other, ClickableAbility)):
            other = other.key()
        elif(not isinstance(other, tuple)):
            raise Exception("Invalid key: {}".format(other))
        if(self._x2 < other[0]):
            return True
        elif(self._x1 <= other[0]):
            return (other[1] < self._y2)

    def eq(self, other):
        if(isinstance(other, ClickableAbility)):
            other = other.key()
        elif(not isinstance(other, tuple)):
            raise Exception("Invalid key: {}".format(other))
        center = self.center()
        return (abs(other[0]-center[0]) <= 15 and abs(other[1]-center[1]) <= 15)

    def key(self):
        return self.center()

    def center(self):
        return ((self._x1+self._x2)/2, (self._y1+self._y2)/2)

    def box(self):
        return [self._x1, self._y1,
                self._x2, self._y1,
                self._x2, self._y2,
                self._x1, self._y2,
                self._x1, self._y1]

    def label(self):
        return self._name

    def to_dict(self):
        ability = {}
        ability['ability'] = self._name
        ability['x'] = self._x1
        ability['y'] = self._y1
        ability['w'] = self._x2
        ability['h'] = self._y2
        return ability

    def __str__(self):
        return "{} : ({},{})".format(self._name, *self.center())

class KeypressAbility(AbilityReference):
    modifier_keys = [keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.alt_l, keyboard.Key.alt_gr, keyboard.Key.shift,
                     keyboard.Key.shift_r, keyboard.Key.shift_l, keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l]
    modifier_key_map = {'shift':'shift', 'shift_r':'shift', 'alt_l':'alt', 'alt_gr':'alt', 'alt':'alt', 'ctrl':'ctrl',
                        'ctrl_l':'ctrl', 'ctrl_r':'ctrl'}
    def __init__(self, deserializeable):
        super().__init__(deserializeable['ability'])
        self._key = deserializeable['key'].lower()
        if(deserializeable['modifier'] is None):
            self._modifier = None
        else:
            self._modifier = deserializeable['modifier']

    def has_modifier(self):
        return self._modifier is None

    def modifier_match(self, modifier):
        return self._modifier == modifier

    def key(self):
        if(self._modifier is None):
            return self._key
        else:
            return self._key + self._modifier
        
    def lt(self, other):
        if(isinstance(other, KeypressAbility)):
            other = other.key()
        elif(not isinstance(other, tuple)):
            raise Exception("Invalid key: {}".format(other))
        else:
            if(other[1] is None):
                other = other[0]
            else:
                other = "".join(other)
        if(self.key() < other):
            return True
        else:
            return False

    def eq(self, other):
        if(isinstance(other, KeypressAbility)):
            other = other.key()
        elif(not isinstance(other, tuple)):
            raise Exception("Invalid key: {}".format(other))
        else:
            if(other[1] is None):
                other = other[0]
            else:
                other = "".join(other)
        print(self.key(), other)
        return(self.key() == other)

    def to_dict(self):
        return {'ability':self._name, 'key':self._key, 'modifier':self._modifier}

    def __hash__(self):
        return self.key().__hash__()

    def __str__(self):
        return "{} : ({} + {})".format(self._name, self._key, self._modifier)

class TreeNode:
    def __init__(self, item, right, left):
        self.item = item
        self.right = right
        self.left = left

class AbilitySearchTable:
    def __init__(self, ability_list):
        self.map = {}
        self.build_table(ability_list)

    def build_table(self, ability_list):
        for ability in ability_list:
            self.map[ability.__hash__()] = ability
                  
    def search(self, key):
        if(key[1] is None):
            key = key[0]
        else:
            key = "".join(key)
        try:
            return self.map[key.__hash__()]
        except:
            return None

class AbilitySearchList:
    def __init__(self, ability_list):
        self.ability_list = ability_list
        
    def search(self, key):
        if(key[1] is None):
            key = key[0]
        else:
            key = "".join(key)
        for i in range(len(self.ability_list)):
            if(self.ability_list[i].key() == key):
                return self.ability_list[i]
        return None
    
class AbilitySearchTree:
    def __init__(self, ability_list):
        self.root = None
        self.size = 0
        self.build_tree(ability_list)

    def build_tree(self, ability_list):
        for i in range(len(ability_list)):
            self.insert(ability_list[i])

    def insert(self, ability):
        if(self.root is None):
            self.root = TreeNode(ability, None, None)
            self.size += 1
        else:
            curr = self.root
            while(True):
                if(ability.lt(curr.item) or ability.eq(curr.item)):
                    if(curr.left == None):
                        self.size += 1
                        curr.left = TreeNode(ability, None, None)
                        return
                    else:
                        curr = curr.left
                else:
                    if(curr.right == None):
                        curr.right = TreeNode(ability, None, None)
                        self.size += 1
                        return
                    else:
                        curr = curr.right

    def search(self, key):
        curr = self.root
        while(True):
            if(curr.item.eq(key)):
                return curr.item
            elif(curr.item.lt(key)):
                if(curr.right != None):
                    curr = curr.right
                else:
                    return None
            else:
                if(curr.left != None):
                    curr = curr.left
                else:
                    return None
