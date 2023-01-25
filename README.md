# LeMageTank's RS3 Ability Tracker
![ability-tracker](https://user-images.githubusercontent.com/91403167/214178520-2adc9488-173b-44f0-b4cd-0675bbd607a2.PNG)

1. [Features](#Features)
2. [Setup](#Setup)
3. [Extensions](#Extensions)
   - Ability Tracker
   - APM Counter
4. [Environment Setup and Building](#Environment-Setup-and-Building)
5. [Extensions API](#Extensions-API)
6. [Adding Custom Abilities and Macros](#Adding_Custom_Abilities_and_Macros)

## Features
Currently available and upcoming features:
- [x] Ability, weapon, spell, etc. tracking for action bar keybinds and mouse-presses
- [x] Automatic action bar updating on weapon changes
- [x] Step-by-step setup wizard
- [x] Web endpoint ability tracker for OBS
- [x] Actions-per-minutes counter
- [x] Extension API
- [ ] EOF and weapon special tracking
- [ ] Multi-output macro support
- [ ] Inventory & Prayerbook mousebinds
- [ ] Keybind Action Bar Switching

## Setup
**Setup Steps:**

### 1. Action Bar Presets
![image](https://user-images.githubusercontent.com/91403167/214440387-07c1c02c-0eff-4d3f-83f3-a85ceff6f67b.png)

Drag and drop abilities, weapons, prayers, items, etc. to the numbered action bar presets to match your in-game presets.  

---
### 2. On-Screen Action Bar Selection

![image](https://user-images.githubusercontent.com/91403167/214440870-871da2dd-5b28-43e0-b5af-25c14029ada1.png)

Select the action bars that you have on-screen in-game.  

---
### 3. Action Bar Keybinds

![image](https://user-images.githubusercontent.com/91403167/214441027-941654fc-a3c7-44c9-a641-ccff534bd99d.png)

Enter the keybinds for your action bars. Select the modifier for the keybind using the drop-down menu on the right, and enter the main key on the left. For non-alphanumeric keys, including f keys, enter the keycode ('f1' for f1, 'f2' for f2, 'del' for delete, etc.).  

---
### 4. Action Bar Mousebinds

![image](https://user-images.githubusercontent.com/91403167/214441667-9d9b0c17-dc96-4675-a490-eed7af352bee.png)

Move the setup dialogue box to the monitor where your game is shown. Clicking 'begin' will take a screen shot and display it in fullscreen.

![image](https://user-images.githubusercontent.com/91403167/214442041-0405be7b-626c-4915-9f21-428b3b1689a0.png)

An action bar corresponding to each active action bar you selected on the action bar selection page will be shown. Each action bar and the continue dialogue can be moved by clicking and dragging (drag the action bars by their opaque areas, transparent areas can be clicked-through). Drag the action bars to as closely as possible align with your in-game action bars. Right click action bars to change their layout.

![image](https://user-images.githubusercontent.com/91403167/214442555-2fed092d-78c7-459a-b64c-bc2b5482285b.png)

Click continue when you've aligned each action bar.  

---
### 5. Weapon Switch Action Bars

![image](https://user-images.githubusercontent.com/91403167/214442738-3702cc07-fddd-4387-b940-1c649fd1a64b.png)

For each weapon class you have set to load action bar presets when swapping weapons, select the weapon style, check the action bars that have bound presets, and then select the preset to load from the drop-down menu.

---
### 6. Default Action Bars

![image](https://user-images.githubusercontent.com/91403167/214443299-559ba2e3-1a10-4f50-95dc-a62edb0dcdab.png)

Select which action bars the ability tracker should load by default on start-up.

## Extensions
TODO

## Environment Setup and Building
TODO

## Extensions API
TODO

## Adding Custom Abilities and Macros

### Adding Custom Abilities
If there's an ability or action missing from the tracker's built in list, or there's a custom action you'd like the tracker to display, you can add it with these simple steps:
1. Add a 30 x 30 pixel PNG image to the /icons directory with the file name being the action's name.
2. Add an entry to the /data/abilityinfo.json file for the action with this schema:

```json
{
		"action": "{ action name }",
		"type": "{ action type }",
		"cooldown": 0.0,
		"incurs_gcd": true,
		"adrenaline-delta": 0,
		"ability-type": "{ action type }",
		"hits":[],
		"tag": "{ tag }"
} 
```

   ***action:*** The name of the action, this must match the file name (excluding the file extension).
   
   ***type:*** This is how actions are grouped within each of the action bar preset creation tabs during setup. This can be anything including '*null*', but the existing tags are:
   "ancient curse", "ammo", "shield", "ring", "potion", "food", "pocket", "spell", "basic", "threshold", "ultimate", "special", "weapon", and "misc".
   
   ***cooldown:*** How long is this action's cooldown if it has one?

   ***incurs_gcd:*** Does this action incur the in-game global cooldown?
   
   ***adrenaline-delta:*** This is unused for now, will be the base adrenaline change (e.g.: -15 for threshold abilities) when using this ability.

   ***ability-type:*** This is unused for now, will be one of: "channeled", "non-damage", "standard", "bleed", or "movement".
   
   ***hits:*** This is unused for now, will be a list of this abilties hits where each hit is a JSON map with *tick* that the hit lands and *damage* range of min and max hit (``` {"tick": 0, "damage": [40, 200]} ```).

   ***tag:*** This is which tab the action will be placed during the action bar preset creation.

---

### Adding Macros
Macros aren't officially allowed or supported in RuneScape, but many PvMers use them anyway, so this will tell you how to add them. Additionally, if in-game macros are ever added, this is how you can set them up. Macros that are mapped to multiple in-game actions should work by default, but if you use a keybind macro that isn't working with the tracker for some reason then you can use this process to add it:

1. Create a keybind through the normal setup process for one of the outputs. For example, if your keybind for `shift + 1` equips both `Dark shard of Leng` and `Dark sliver of Leng` through an external macro, then set `shift + 1` to equip the `Dark shard of Leng`.
2. Open the **/data/input_profile.json** file to view your keybinds and mousebinds.
3. Find the preset containing the `Dark shard of Leng` in the **action-bar-presets** list.

It will look like this:
```
{
"action-bar-presets": [
   ...
   "name": "Weapons",
            "slots": [
                [
                "Dark shard of Leng"
                  ],
   ...
]
...
}
```
4. Add the other actions that you want to trigger to the list for that preset slot:
```
{
"action-bar-presets": [
   ...
   "name": "Weapons",
            "slots": [
                [
                "Dark shard of Leng", "Dark sliver of Leng"
                  ],
   ...
]
...
}
```
