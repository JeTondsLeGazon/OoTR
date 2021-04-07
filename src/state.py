"""
State class to define items pool possessed by the player and to use with the 
logic script.
"""

# items pool for logic and reinforcement learning states, in the form of:
# (item name, maximum state number (from zero to ...), initial state)
items_pool = [
    ('Boomerang', 1, 0),
    ('Lens of Truth', 1, 0),
    ('Megaton Hammer', 1, 0),
    ('Bottle', 1, 0),
    ('Big Poe', 1, 0),
    ('Rutos Letter', 2, 0),
    ('child trade sequence', 3, 0),
    ('adult trade sequence', 4, 0),
    ('Kokiri Sword', 1, 0),
    ('Deku Shield', 1, 1),
    ('Hylian Shield', 1, 0),
    ('Mirror Shield', 1, 0),
    ('Goron Tunic', 1, 0),
    ('Zora Tunic', 1, 0),
    ('Iron Boots', 1, 0),
    ('Hover Boots', 1, 0),
    ('Fire Arrows', 1, 0),
    ('Light Arrows', 1, 0),
    ('Gold Skulltula Token', 50, 0),
    ('Dins Fire', 1, 0),
    ('Magic Bean', 1, 0),
    ('Progressive Hookshot', 2, 0),
    ('Progressive Strength Upgrade', 3, 0),
    ('Bomb Bag', 1, 0),
    ('Bow', 1, 0),
    ('Slingshot', 1 ,0),
    ('Progressive Wallet', 2, 0),
    ('Progressive Scale', 2, 0),
    ('Magic Meter', 1, 0),
    ('Boss Key (Forest Temple)', 1, 0),
    ('Boss Key (Fire Temple)', 1, 0),
    ('Boss Key (Water Temple)', 1, 0),
    ('Boss Key (Spirit Temple)', 1, 0),
    ('Boss Key (Shadow Temple)', 1, 0),
    ('Small Key (Forest Temple)', 5, 0),
    ('Small Key (Fire Temple)', 8, 0),
    ('Small Key (Water Temple)', 6, 0),
    ('Small Key (Spirit Temple)', 5, 0),
    ('Small Key (Shadow Temple)', 5, 0),
    ('Small Key (Gerudo Training Grounds)', 9, 0),
    ('Minuet of Forest', 1, 0),
    ('Bolero of Fire', 1, 0),
    ('Serenade of Water', 1, 0),
    ('Requiem of Spirit', 1, 0),
    ('Nocturne of Shadow', 1, 0),
    ('Prelude of Light', 1, 0),
    ('Zeldas Lullaby', 1 ,0),
    ('Eponas Song', 1, 0),
    ('Sarias Song', 1, 0),
    ('Suns Song', 1, 0),
    ('Song of Time', 1, 0),
    ('Song of Storms', 1, 0),
    ('isadult', 1, 0),
    ('Forest Medallion', 1, 0),
    ('Fire Medallion', 1, 0),
    ('Water Medallion', 1, 0),
    ('Shadow Medallion', 1, 0),
    ('Spirit Medallion', 1, 0),
    ('Light Medallion', 1, 0),
    ('Kokiri Emerald', 1, 0),
    ('Goron Ruby', 1, 0),
    ('Zora Sapphire', 1, 0)]



class State():
    
    def __init__(self, base_items=items_pool):
        self.items = base_items
        self.where = None
        self.child_spawn = None
        self.adult_spawn = None
        
    @property   
    def items(self):
        return self._items
    
    @items.setter
    def items(self, items_pool):
        self._items = {k: {'max': m, 'current': i} for k, m , i in items_pool}
    
    def item_update(self, item_name):
        if self._items[item_name]['current'] < self._items[item_name]['max']:
            self._items[item_name]['current'] += 1
            
    def change_age(self):
        self._items['isadult']['current'] = int(not bool(self._items['isadult']['current']))
        
    def set_age(self, age):
        self._items['isadult']['current'] = age

    def set_initial_ms(self, locations):
        self.item_update(locations['Links Pocket'])
        
    def set_where(self, loc):
        self.where = loc
        
    def set_adult_spawn(self, loc):
        self.adult_spawn = loc
    
    def set_child_spawn(self, loc):
        self.child_spawn = loc
        
    def can_beat_ganon(self):
        return self.current_med() == 6
    
    def current_med(self):
        Medallions = [m + ' Medallion' for m in 
                  ['Forest', 'Fire', 'Water', 'Shadow', 'Spirit', 'Light']]
        return sum([self.items[m]['current'] for m in Medallions])
    
    def current_med_name(self):
        Medallions = [m + ' Medallion' for m in 
                  ['Forest', 'Fire', 'Water', 'Shadow', 'Spirit', 'Light']]
        return [(m, self.items[m]['current']) for m in Medallions]
    
    def is_where(self):
        return self.where