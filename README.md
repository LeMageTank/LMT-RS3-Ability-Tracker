# LeMageTank's RS3 Ability Tracker
![ability-tracker](https://user-images.githubusercontent.com/91403167/214178520-2adc9488-173b-44f0-b4cd-0675bbd607a2.PNG)

This program is under active development and is currently working but incomplete. Bugs may exist, abilities, items and spells may not be present, and there may be inconsistencies in formatting. The full feature list for the upcoming version 1.0.0 can be found in the [Features](#features) section.

1. [Features](#features)
2. [Setup](#setup)
3. [Extensions](#extensions)
   - Ability Tracker
   - APM Counter
4. [Environment Setup and Building](#environment-setup-and-building)
5. [Extensions API](#extensions-api)
6. [Adding Custom Abilities and Macros](#adding-custom-abilities-and-macros)

## Features
Currently available and upcoming features:
- [x] Ability, weapon, spell, etc. tracking for action bar keybinds and mouse-presses
- [x] Automatic action bar updating on weapon changes
- [x] Step-by-step setup wizard
- [x] Web endpoint ability tracker for OBS
- [x] Actions-per-minutes counter
- [x] Extension API
- [ ] EOF and weapon special tracking
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
This application comes with two 'extensions' by default: the [ability tracker](#ability-tracker) and an [actions-per-minute counter](#apm-counter). Extensions in this context are similar to plugins for runelite; an [extensions API](#Extensions-API) exposes the ui, user input/actions, and game data for use by the extensions. In the future this program may be updated with more extensions.

- ### Ability Tracker
The Ability Tracker extension shows the abilities, items, equipment, and etc. that the player uses in a timeline format:
![Tracker](https://user-images.githubusercontent.com/91403167/214473693-c2089ade-c392-40df-8050-b65423430af9.PNG)

This extension has two modes: an on-screen bar that displays an adjustable number of actions, and a 'web' endpoint that can be imported into OBS for use on-screen without it being displayed on-screen.

The on-screen ability tracker is enabled by default. To use the web endpoint for displaying the tracker in OBS follow these steps:
1. Add a Browser source in OBS

![image](https://user-images.githubusercontent.com/91403167/214474409-8a49e2cf-f8be-49fe-80c5-64799ec37153.png)

2. Check the `Local File` box

![image](https://user-images.githubusercontent.com/91403167/214474644-cef2b78a-61b2-4c56-be1e-f125d79ef3e9.png)

3. Add the file `/data/extension data/action-tracker/ability-tracker-page.html`

![image](https://user-images.githubusercontent.com/91403167/214474572-4b59bf65-e1cf-4773-8561-5d0cdcd4049e.png)

The ability tracker should now be visible in the scene, adjust the size and resolution as necessary.

![image](https://user-images.githubusercontent.com/91403167/214474856-ad24838b-9f09-4792-ac46-366b868db707.png)


The ability tracker has a few configuration options within the `config.json` file:
- **action-tracker-enabled**: Enable or disable the tracker (boolean)
- **tracker-background-color**: The background color of the ability tracker, leave empty for transparent background (hex string)
- **actiontracker-icons**: The number of actions displayed on the tracker (int)
- **actiontracker-always-on-top**: Sets if the ability tracker always shows on top of other programs (boolean)
- **action-tracker-window-position**: The position of the ability tracker on-screen, updates automaticall on exit (int [x, y])
---
- ### APM Counter

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
