"""
Pathfinder to estimate time between two zones, depending on state.
"""
# TODO: use more region for access (DMC, DMT, Graveyard pad)
# TODO: castle grounds may be both adult and child !!!

from src.logic import requirements_in_logic
from mylog import logger

locations_table = [
    ('HF', 'Market', 45, []),
    ('HF', 'GV HF Side', 60, []),
    ('HF', 'LH', 75, []),
    ('HF', 'LLR', 45, []),
    ('HF', 'KF', 60, []),
    ('HF', 'Kak', 60, []),
    ('HF', 'ZR', 75, [[('isadult', 1)],
                      [('isadult', 0), ('Bomb Bag', 1)],
                      [('isadult', 0), ('is_where|ZR', 1)]]),
    ('GV HF Side', 'GV GF Side', 15, [[('isadult', 1), ('Eponas Song', 1)],
                                      [('isadult', 1), ('Progressive Hookshot', 2)],
                                      [('isadult', 0), ('is_where|GV HF Side', 1)]]),
    ('GV GF Side', 'GF', 15, []),
    ('GF', 'Wasteland', 60, [('isadult', 1)]),
    ('GF', 'GTG', 15, [('isadult', 1)]),
    ('Colossus', 'Wasteland', 60, []),
    ('Spirit Temple', 'Colossus', 20, []),
    ('GV HF Side', 'LH', 45, [('is_where|GV HF Side', 1)]),
    ('GV GF Side', 'LH', 45, [('is_where|GV GF Side', 1)]),
    ('Water Temple', 'LH', 30, []),
    ('ZD', 'LH', 30, [('isadult', 0), ('Progressive Scale', [1])]),
    ('KF', 'Deku Tree', 30, []),
    ('KF', 'LW', 30, []),
    ('LW', 'SFM', 25, []),
    ('Forest Temple', 'SFM', 30, []),
    ('LW', 'ZR', 25, [[('Progressive Scale', [1])],
                      [('isadult', 1), ('Iron Boots', 1)]]),
    ('LW', 'GC', 25, [[('Bomb Bag', 1)],
                      [('isadult', 1), ('Bow', 1), ('is_where|GC', 1)],
                      [('Dins Fire', 1), ('Magic Meter', 1)],
                      [('Progressive Strength Upgrade', [1]), ('is_where|GC', 1)],
                      [('isadult', 1), ('Megaton Hammer', 1)]]),
    ('ZD', 'ZR', 45, [[('isadult', 0)],
                      [('Zeldas Lullaby', 1)],
                      [('isadult', 1), ('Hover Boots', 1)],
                      [('is_where|ZD', 1)]]),
    ('ZD', 'ZF', 30, [[('Rutos Letter', 2)],
                      [('isadult', 1)]]),
    ('Ice Cavern', 'ZF', 30, [('isadult', 1)]),
    ('Jabu Jabus Belly', 'ZF', 15, [('isadult', 0)]),
    ('Graveyard', 'Kak', 20, []),
    ('Graveyard', 'anywhere', 10, [('Nocturne of Shadow', 1)]),
    ('Shadow Temple', 'anywhere', 10, [('Nocturne of Shadow', 1),
                                       ('Magic Meter', 1),
                                       ('Dins Fire', 1)]),
    ('DMT', 'Kak', 20, []),
    ('DMT', 'Dodongos Cavern', 20, []),
    ('DMT', 'GC', 20, []),
    ('DMC Upper', 'GC', 20, [[('isadult', 1), ('Bomb Bag', 1), ('is_where|GC', 1)],
                       [('isadult', 1), ('Bow', 1), ('is_where|GC', 1)],
                       [('isadult', 1), ('Progressive Strength Upgrade', [1]), ('is_where|GC', 1)],
                       [('is_where|DMC Upper', 1)],
                       [('isadult', 1), ('Dins Fire', 1), ('Magic Meter', 1), ('is_where|GC', 1)]]),
    ('DMC Lower', 'DMC Upper', 15, [[('isadult', 1), ('Hover Boots', 1)],
                                    [('isadult', 1), ('Progressive Hookshot', [1])],
                                    [('isadult', 1), ('Magic Bean', 1), ('is_where|DMC Lower', 1)]]),
    ('DMT', 'DMC Upper', 20, [[('Bomb Bag', 1)],
                              [('Megaton Hammer', 1), ('isadult', 1)]]),
    ('DMC Lower', 'Fire Temple', 20, [('isadult', 1)]),
    ('Market', 'Hyrule Castle', 30, [('isadult', 0)]),
    ('Market', 'Outside Ganons Castle', 30, [('isadult', 1)]),
    ('Ganons Castle', 'Outside Ganons Castle', 30, [('isadult', 1)]),
    ('Market', 'Temple of Time', 30, []),
    ('Kak', 'Bottom of the Well', 10, [])
    ]

locations_to_zones = {
    'KF':       ["KF Kokiri Sword Chest", 
                 "KF Midos Top Left Chest", 
                 "KF Midos Top Right Chest",
                 "KF Midos Bottom Right Chest",
                 "KF Midos Bottom Left Chest",
                 "KF Storms Grotto Chest"],
    'LW':       ["LW Skull Kid",
                 "LW Ocarina Memory Game",
                 "LW Target in Woods",
                 "LW Deku Scrub Near Bridge",
                 "LW Near Shortcuts Grotto Chest",
                 "Deku Theater Skull Mask",
                 "LW Deku Scrub Grotto Front"],
    'SFM':      ["Song from Saria",
                 "Sheik in Forest",
                 "SFM Wolfos Grotto Chest"],
    'Forest Temple':    ["Phantom Ganon",
                         "Forest Temple First Room Chest",
                         "Forest Temple First Stalfos Chest",
                         "Forest Temple Raised Island Courtyard Chest",
                         "Forest Temple Well Chest",
                         "Forest Temple Map Chest",
                         "Forest Temple Falling Ceiling Room Chest",
                         "Forest Temple Eye Switch Chest",
                         "Forest Temple Boss Key Chest",
                         "Forest Temple Floormaster Chest",
                         "Forest Temple Bow Chest",
                         "Forest Temple Red Poe Chest",
                         "Forest Temple Blue Poe Chest",
                         "Forest Temple Basement Chest",
                         "Forest Temple Phantom Ganon Heart"],
    'HF':           ["HF Open Grotto Chest",
                     "HF Southeast Grotto Chest",
                     "HF Deku Scrub Grotto",
                     "HF Near Market Grotto Chest",
                     "HF Tektite Grotto Freestanding PoH",
                     "Song from Ocarina of Time"],
    'GV GF Side':   ["GV Waterfall Freestanding PoH",  #appears twice
                     "GV Chest"],
    'GV HF Side':   ["GV Waterfall Freestanding PoH",
                     "GV Crate Freestanding PoH"],
    'GF':           ["GF Chest",
                     "GF HBA 1000 Points",
                     "GF HBA 1500 Points"],
    'GTG':          ["Gerudo Training Grounds Lobby Left Chest",
                     "Gerudo Training Grounds Lobby Right Chest",
                     "Gerudo Training Grounds Stalfos Chest",
                     "Gerudo Training Grounds Beamos Chest",
                     "Gerudo Training Grounds Hidden Ceiling Chest",
                     "Gerudo Training Grounds Maze Path First Chest",
                     "Gerudo Training Grounds Maze Path Second Chest",
                     "Gerudo Training Grounds Maze Path Third Chest",
                     "Gerudo Training Grounds Maze Path Final Chest",
                     "Gerudo Training Grounds Maze Right Central Chest",
                     "Gerudo Training Grounds Maze Right Side Chest",
                     "Gerudo Training Grounds Freestanding Key",
                     "Gerudo Training Grounds Underwater Silver Rupee Chest",
                     "Gerudo Training Grounds Hammer Room Clear Chest",
                     "Gerudo Training Grounds Hammer Room Switch Chest",
                     "Gerudo Training Grounds Eye Statue Chest",
                     "Gerudo Training Grounds Near Scarecrow Chest",
                     "Gerudo Training Grounds Before Heavy Block Chest",
                     "Gerudo Training Grounds Heavy Block First Chest",
                     "Gerudo Training Grounds Heavy Block Second Chest",
                     "Gerudo Training Grounds Heavy Block Third Chest",
                     "Gerudo Training Grounds Heavy Block Fourth Chest"],
    'Wasteland':    ["Wasteland Chest"],
    'Colossus':     ["Colossus Freestanding PoH",
                     "Colossus Great Fairy Reward",
                     "Sheik at Colossus"],
    'Spirit Temple':    ["Spirit Temple Child Bridge Chest",
                         "Spirit Temple Child Early Torches Chest",
                         "Spirit Temple Child Climb East Chest",
                         "Spirit Temple Child Climb North Chest",
                         "Spirit Temple Compass Chest",
                         "Spirit Temple Early Adult Right Chest",
                         "Spirit Temple Map Chest",
                         "Spirit Temple First Mirror Right Chest",
                         "Spirit Temple First Mirror Left Chest",
                         "Spirit Temple Sun Block Room Chest",
                         "Spirit Temple Statue Room Hand Chest",
                         "Spirit Temple Statue Room Northeast Chest",
                         "Spirit Temple Silver Gauntlets Chest",
                         "Spirit Temple Mirror Shield Chest",
                         "Spirit Temple Near Four Armos Chest",
                         "Spirit Temple Hallway Left Invisible Chest",
                         "Spirit Temple Hallway Right Invisible Chest",
                         "Spirit Temple Boss Key Chest",
                         "Spirit Temple Topmost Chest",
                         "Spirit Temple Twinrova Heart",
                         "Twinrova"],
    'ZR':           ["ZR Frogs Ocarina Game",
                     "ZR Frogs in the Rain",
                     "ZR Near Open Grotto Freestanding PoH",
                     "ZR Near Domain Freestanding PoH",
                     "ZR Open Grotto Chest",
                     'Buy Magical Beans'],
    'ZD':           ["ZD Diving Minigame",
                     "ZD Chest",
                     "ZD King Zora Thawed",
                     'Deliver RL',
                     'Adult Trade Sequence 1'],
    'ZF':           ["ZF Iceberg Freestanding PoH",
                     "ZF Bottom Freestanding PoH",
                     "ZF Great Fairy Reward"],
    'Jabu Jabus Belly':     ["Jabu Jabus Belly Boomerang Chest",
                             "Jabu Jabus Belly Map Chest",
                             "Jabu Jabus Belly Compass Chest",
                             "Jabu Jabus Belly Barinade Heart",
                             "Barinade"],
    'Ice Cavern':           ["Sheik in Ice Cavern",
                             "Ice Cavern Map Chest",
                             "Ice Cavern Compass Chest",
                             "Ice Cavern Iron Boots Chest",
                             "Ice Cavern Freestanding PoH"],
    'Kak':          ["Sheik in Kakariko",
                     "Song from Windmill",
                     "Kak Anju as Adult",
                     "Kak Anju as Child",
                     "Kak Man on Roof",
                     "Kak 10 Gold Skulltula Reward",
                     "Kak 20 Gold Skulltula Reward",
                     "Kak 30 Gold Skulltula Reward",
                     "Kak 40 Gold Skulltula Reward",
                     "Kak 50 Gold Skulltula Reward",
                     "Kak Impas House Freestanding PoH",
                     "Kak Windmill Freestanding PoH",
                     "Kak Shooting Gallery Reward",
                     "Kak Redead Grotto Chest",
                     "Kak Open Grotto Chest",
                     'Child Trade Sequence 2'],
    'Graveyard':    ["Song from Composers Grave",
                     "Graveyard Freestanding PoH",
                     "Graveyard Dampe Gravedigging Tour",
                     "Graveyard Shield Grave Chest",
                     "Graveyard Heart Piece Grave Chest",
                     "Graveyard Composers Grave Chest",
                     "Graveyard Hookshot Chest",
                     "Graveyard Dampe Race Freestanding PoH"],
    'Shadow Temple':        ["Bongo Bongo",
                             "Shadow Temple Map Chest",
                             "Shadow Temple Hover Boots Chest",
                             "Shadow Temple Compass Chest",
                             "Shadow Temple Early Silver Rupee Chest",
                             "Shadow Temple Invisible Blades Visible Chest",
                             "Shadow Temple Invisible Blades Invisible Chest",
                             "Shadow Temple Falling Spikes Lower Chest",
                             "Shadow Temple Falling Spikes Upper Chest",
                             "Shadow Temple Falling Spikes Switch Chest",
                             "Shadow Temple Invisible Spikes Chest",
                             "Shadow Temple Freestanding Key",
                             "Shadow Temple Wind Hint Chest",
                             "Shadow Temple After Wind Enemy Chest",
                             "Shadow Temple After Wind Hidden Chest",
                             "Shadow Temple Spike Walls Left Chest",
                             "Shadow Temple Boss Key Chest",
                             "Shadow Temple Invisible Floormaster Chest",
                             "Shadow Temple Bongo Bongo Heart"],
    'Bottom of the Well':       ["Bottom of the Well Front Left Fake Wall Chest",
                                 "Bottom of the Well Front Center Bombable Chest",
                                 "Bottom of the Well Right Bottom Fake Wall Chest",
                                 "Bottom of the Well Compass Chest",
                                 "Bottom of the Well Center Skulltula Chest",
                                 "Bottom of the Well Back Left Bombable Chest",
                                 "Bottom of the Well Freestanding Key",
                                 "Bottom of the Well Lens of Truth Chest",
                                 "Bottom of the Well Invisible Chest",
                                 "Bottom of the Well Underwater Front Chest",
                                 "Bottom of the Well Underwater Left Chest",
                                 "Bottom of the Well Map Chest",
                                 "Bottom of the Well Fire Keese Chest",
                                 "Bottom of the Well Like Like Chest"],
    'DMT':      ["DMT Chest",
                 "DMT Freestanding PoH",
                 "DMT Biggoron",
                 "DMT Great Fairy Reward",
                 "DMT Storms Grotto Chest",
                 'Adult Trade Sequence 3'],
    'Dodongos Cavern':      ["King Dodongo",
                             "Dodongos Cavern Map Chest",
                             "Dodongos Cavern Compass Chest",
                             "Dodongos Cavern Bomb Flower Platform Chest",
                             "Dodongos Cavern Bomb Bag Chest",
                             "Dodongos Cavern End of Bridge Chest",
                             "Dodongos Cavern Boss Room Chest",
                             "Dodongos Cavern King Dodongo Heart"],
    'GC':       ["GC Maze Left Chest",
                 "GC Maze Center Chest",
                 "GC Maze Right Chest",
                 "GC Pot Freestanding PoH",
                 "GC Rolling Goron as Child",
                 "GC Rolling Goron as Adult",
                 "GC Darunias Joy"],
    'DMC Upper':     ["DMC Wall Freestanding PoH",
                      "DMC Great Fairy Reward",
                      "DMC Upper Grotto Chest"],
    'DMC Lower':    ["DMC Volcano Freestanding PoH",  # twice
                     "Sheik in Crater"],
    'Fire Temple':      ["Volvagia",
                         "Fire Temple Near Boss Chest",
                         "Fire Temple Flare Dancer Chest",
                         "Fire Temple Boss Key Chest",
                         "Fire Temple Volvagia Heart",
                         "Fire Temple Big Lava Room Lower Open Door Chest",
                         "Fire Temple Big Lava Room Blocked Door Chest",
                         "Fire Temple Boulder Maze Lower Chest",
                         "Fire Temple Boulder Maze Upper Chest",
                         "Fire Temple Boulder Maze Side Room Chest",
                         "Fire Temple Boulder Maze Shortcut Chest",
                         "Fire Temple Scarecrow Chest",
                         "Fire Temple Map Chest",
                         "Fire Temple Compass Chest",
                         "Fire Temple Highest Goron Chest",
                         "Fire Temple Megaton Hammer Chest"],
    'Deku Tree':        ["Queen Gohma",
                         "Deku Tree Map Chest",
                         "Deku Tree Compass Chest",
                         "Deku Tree Compass Room Side Chest",
                         "Deku Tree Basement Chest",
                         "Deku Tree Slingshot Chest",
                         "Deku Tree Slingshot Room Side Chest",
                         "Deku Tree Queen Gohma Heart"],
    'LLR':      ["Song from Malon",
                 "LLR Talons Chickens",
                 "LLR Freestanding PoH"],
    'LH':       ["LH Underwater Item",
                 "LH Sun",
                 "LH Freestanding PoH",
                 "LH Lab Dive",
                 "LH Child Fishing",
                 "LH Adult Fishing",
                 'Adult Trade Sequence 2'],
    'Water Temple':     ["Morpha",
                         "Water Temple Morpha Heart",
                         "Water Temple Map Chest",
                         "Water Temple Compass Chest",
                         "Water Temple Torches Chest",
                         "Water Temple Central Bow Target Chest",
                         "Water Temple Boss Key Chest",
                         "Water Temple Cracked Wall Chest",
                         "Water Temple Dragon Chest",
                         "Water Temple Central Pillar Chest",
                         "Water Temple Longshot Chest",
                         "Water Temple River Chest"],
    'Market':       ["Market 10 Big Poes",
                     "Market Shooting Gallery Reward",
                     "Market Bombchu Bowling First Prize",
                     "Market Bombchu Bowling Second Prize",
                     "Market Treasure Chest Game Reward",
                     "Market Lost Dog",
                     'Child Trade Sequence 1',
                     'Child Trade Sequence 3'],
    'Temple of Time':       ["Sheik at Temple",
                             'Time Travel'],
    'Hyrule Castle':        ["HC Great Fairy Reward"],
    'Outside Ganons Castle':        ["OGC Great Fairy Reward"],
    'Ganons Castle':        ["Ganons Castle Forest Trial Chest",
                             "Ganons Castle Water Trial Left Chest",
                             "Ganons Castle Water Trial Right Chest",
                             "Ganons Castle Shadow Trial Front Chest",
                             "Ganons Castle Shadow Trial Golden Gauntlets Chest",
                             "Ganons Castle Spirit Trial Crystal Switch Chest",
                             "Ganons Castle Spirit Trial Invisible Chest",
                             "Ganons Castle Light Trial First Left Chest",
                             "Ganons Castle Light Trial Second Left Chest",
                             "Ganons Castle Light Trial Third Left Chest",
                             "Ganons Castle Light Trial First Right Chest",
                             "Ganons Castle Light Trial Second Right Chest",
                             "Ganons Castle Light Trial Third Right Chest",
                             "Ganons Castle Light Trial Invisible Enemies Chest",
                             "Ganons Castle Light Trial Lullaby Chest",
                             "Ganons Tower Boss Key Chest"]
    }


spawns = {'Market': 'Market',
          'Kakariko Village': 'Kak',
          'Hyrule Field': 'HF',
          'Kokiri Forest': 'KF',
          'Lon Lon Ranch': 'LLR',
          'Zoras Domain': 'ZD',
          'Lake Hylia': 'LH',
          'Temple of Time': 'Temple of Time',
           'Market Entrance': 'Market',
           'Lost Woods': 'LW',
           'Castle Grounds': ['Hyrule Castle', 'Outside Ganons Castle'],
           'Graveyard': 'Graveyard',
           'ToT Entrance': 'Market',
           'Zora River': 'ZR',
           'Kak Impas Ledge': 'Kak',
           'Death Mountain Summit': 'DMT',
           'KF Links House': 'KF',
           'Kak Backyard': 'Kak',
           'Market Back Alley': 'Market',
           'GV Fortress Side': 'GV GF Side', 
           'LH Fishing Hole': 'LH',
           'Kak Potion Shop Back': 'Kak',
           'Market Shooting Gallery': 'Market',
           'LLR Stables': 'LLR',
           'LLR Tower': 'LLR',
           'Kak Shooting Gallery': 'Kak',
           'DMC Lower Local': 'DMC Upper',
           'Kak Bazaar': 'Kak',
           'Kak Potion Shop Front': 'Kak',
           'Market Bazaar': 'Market',
           'Kak Impas House Back': 'Kak',
           'Graveyard Dampes House': 'Graveyard',
           'Kak Windmill': 'Kak',
           'DMT Great Fairy Fountain': 'DMT',
           'LH Lab': 'LH',
           'Market Treasure Chest Game': 'Market',
           'Kak Impas House': 'Kak',
           'Market Man in Green House': 'Market',
           'ZD Shop': 'ZD',
           'DMC Upper Local': 'DMC Upper',
           'KF Sarias House': 'KF',
           'Market Potion Shop': 'Market',
           'LW Bridge From Forest': 'LW',
           'Death Mountain': 'DMT',
           'Market Bombchu Shop': 'Market',
           'GC Woods Warp': 'GC',
           'KF Know It All House': 'KF',
           'KF Kokiri Shop': 'KF',
           'KF Midos House': 'KF',
           'Kak House of Skulltula': 'Kak',
           'Graveyard Warp Pad Region': 'Graveyard',
           'LW Bridge': 'KF',
           'ZR Front': 'HF',
           'Gerudo Fortress': 'GF',
           'Market Bombchu Bowling': 'Market',
           'Market Mask Shop': 'Market',
           'LLR Talons House': 'LLR',
           'Gerudo Valley': 'GV HF Side',
           'KF House of Twins': 'KF',
           'ZR Behind Waterfall': 'ZD',
           'Kak Carpenter Boss House': 'Kak',
           'Kak Odd Medicine Building': 'Kak',
           'Market Guard House': 'Market',
           'Goron City': 'GC',
           'LW Beyond Mido': 'LW',
           'LH Fishing Island': 'LH',
           'SFM Entryway': 'SFM',
           'Sacred Forest Meadow': 'SFM',
           'GC Shop': 'GC',
           'DMC Great Fairy Fountain': 'DMC Upper',
           'OGC Great Fairy Fountain': 'Outside Ganons Castle',
           'GF Outside Gate': 'GF',
           'GC Darunias Chamber': 'GC',
           'HC Great Fairy Fountain': 'Hyrule Castle',
           'Kak Behind Gate': 'Kak',
           'GV Carpenter Tent': 'GV GF Side',
           'Wasteland Near Fortress': 'GF'
           }


class PathFinder:
    
    def __init__(self, state):
        self.locations_table = locations_table.copy()
        self.locations_to_zones = locations_to_zones
        self.locations_table.extend(self.savewarp(state))
        if ('anywhere', 'Colossus', 5, [('Requiem of Spirit', 1)]) in self.locations_table:
            print('Oups')
        self.locations_table.extend(self.songwarp())
    
    def convert_to_region(self, place):
        for k, v in self.locations_to_zones.items():
            if place in v:
                return k
        logger.error(f'No region found for place {place}')
        return ''
    
    @staticmethod
    def convert_spawn_to_region(place, age=0):
        try:
            if place == 'Castle Grounds':
                return spawns[place][age]
            else:
                return spawns[place]
        except:
            logger.error(f'No spawn found at {place}')
            return ''

    def savewarp(self, state):
        """
        Returns an array input from anywhere to the savewarp zone.
        """

        return [('anywhere', state.child_spawn, 10, [('isadult', 0)]),
                ('anywhere', state.adult_spawn, 10, [('isadult', 1)])]
        
    
    def songwarp(self):
        return [('anywhere', 'SFM', 5, [('Minuet of Forest', 1)]),
                ('anywhere', 'DMC Lower', 5, [('Bolero of Fire', 1)]),
                ('anywhere', 'Colossus', 5, [('Requiem of Spirit', 1)]),
                ('anywhere', 'Graveyard', 5, [('Nocturne of Shadow', 1)]),
                ('anywhere', 'LH', 5, [('Serenade of Water', 1)]),
                ('anywhere', 'Temple of Time', 5, [('Prelude of Light', 1)])]
    
    
    def from_to(self, a, b, state):
        """
        Returns the smallest time necessary from a to b given a state.
        """
        paths = []
        new_paths = [[[a], 0]]
        while True:
            paths = new_paths.copy()
            new_paths.clear()
            for path, t_tot in paths:
                if len(path) > 12:
                    continue
                if path[-1] == b:
                    new_paths.append([path, t_tot])
                    if t_tot == min([t for _, t in paths]):
                        return [t_tot, path]
                    continue
                
                nexts = []
                for (first, second, time, req) in self.locations_table:
                    if (path[-1] == first or (first == 'anywhere' and len(path) == 1)) and second not in path and second != 'anywhere' and self.in_logic(state, req, path[-1]):
                        nexts.append((second, time))
                        
                    if (path[-1] == second or (second == 'anywhere' and len(path) == 1)) and first not in path and first != 'anywhere' and self.in_logic(state, req, path[-1]):
                        nexts.append((first, time))
                    
                for n, t in nexts:
                    new_path = path.copy()
                    new_path.append(n)
                    new_paths.append([new_path, t_tot+t])
            if all([p_[-1] == b for p_, _ in new_paths]):  # termination if all paths end in b
                break
        return min([[t, p] for p, t in new_paths]) if len(new_paths) != 0 else [-1, []]  # return minimum time
                    
    
    def in_logic(self, state, req, where):
        if len(req) == 0:
            return True
        
        elif isinstance(req[0], tuple):  # Only one logic possible
            return requirements_in_logic(state, req, where)
        
        else:  # Many logics possible
            return any([requirements_in_logic(state, rr, where) for rr in req])