class Action:
    def __init__(self, action_dict):
        self.id = action_dict['action']
        self.action_type = action_dict['type']
        self.cooldown = action_dict['cooldown']
        self.incurs_gcd = action_dict['incurs_gcd']
        self.adrenaline_delta = action_dict['adrenaline-delta']
        self.ability_type = action_dict['ability-type']
        self.damage_hits = action_dict['hits']
        self.last_use = 0
        self.tag = action_dict['tag']

    def cooldown_remaining(self, current_time):
        return - min(current_time - self.last_use - self.cooldown, 0)

    def can_activate(self, activation_time):
        return activation_time - self.last_use > self.cooldown

    def activate(self, activation_time):
        if activation_time - self.last_use > self.cooldown:
            self.last_use = activation_time
            return True
        else:
            return False

    def get_damage_hits(self):
        return self.damage_hits.copy()

    def __str__(self):
        return "{} : {}".format(self.id, self.action_type)
