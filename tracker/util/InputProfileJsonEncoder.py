import json
from tracker.actions.KeybindAction import KeybindAction
from tracker.actions.MousebindAction import MousebindAction

class InputProfileJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, KeybindAction):
            return obj.to_dict()
        elif isinstance(obj, MousebindAction):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)
