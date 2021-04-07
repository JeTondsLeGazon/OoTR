"""
Items and actions bonus and malus
"""

items_bonus = {
    'Bow':                                  50,
    'Megaton Hammer':                       50,
    'Bomb Bag':                             50,
    'Boomerang':                            30,
    'Progressive Hookshot':                 50,
    'Minuet of Forest':                     30,
    'Bolero of Fire':                       30,
    'Serenade of Water':                    20,
    'Requiem of Spirit':                    40,
    'Nocturne of Shadow':                   40,
    'Prelude of Light':                     30,
    'Zeldas Lullaby':                       50,
    'Eponas Song':                          20,
    'Sarias Song':                          20,
    'Suns Song':                            20,
    'Song of Time':                         20,
    'Song of Storms':                       30,
    'Boss Key (Forest Temple)':             15,
    'Boss Key (Fire Temple)':               20,
    'Boss Key (Water Temple)':              20,
    'Boss Key (Spirit Temple)':             15,
    'Boss Key (Shadow Temple)':             15,
    'Small Key (Forest Temple)':            10,
    'Small Key (Fire Temple)':              10,
    'Small Key (Water Temple)':             10,
    'Small Key (Spirit Temple)':            10,
    'Small Key (Shadow Temple)':            10,
    'Small Key (Gerudo Training Grounds)':  5,
    'Forest Medallion':                     500,
    'Fire Medallion':                       500,
    'Water Medallion':                      500,
    'Shadow Medallion':                     500,
    'Spirit Medallion':                     500,
    'Light Medallion':                      500,
    'Kokiri Emerald':                       30,
    'Goron Ruby':                           30,
    'Zora Sapphire':                        30,
    'Magic Meter':                          50,
    'Progressive Strength Upgrade':         50,
    'Dins Fire':                            30,
    'Fire Arrows':                          20,
    'Light Arrows':                         40,
    'Hover Boots':                          40,
    'Iron Boots':                           20,
    'Mirror Shield':                        30,
    'Hylian Shield':                        5,
    'Rutos Letter':                         20,
    'Bottle':                               10,
    'Big Poe':                              10
    }

def compute_bonus(state, item_found):
    """
    Computes the bonus associated with the item found and the current state.
    """
    if item_found in items_bonus.keys():
        if state.items[item_found]['current'] == state.items[item_found]['max']:
            return 0
        else:
            return items_bonus[item_found]
    else:
        return 0