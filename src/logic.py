from mylog import logger

# Free Scarecrow
# No reverse Wasteland
# Automatic Bean plantation everywhere upon purchase
# Rupies not taken into account
# Time of day always favorable
# Skulltulas incrementely updated

mylogic = {
    "Links Pocket":                                          [],
    "Queen Gohma":                                           [('isadult', 0), ('Kokiri Sword', 1)],
    "King Dodongo":                                          [("Bomb Bag", 1), ('isadult', 1)],
    "Barinade":                                              [[("Progressive Scale", [1]), ("Rutos Letter", 2), ("Boomerang", 1), ('isadult', 0)], 
                                                              [("Bomb Bag", 1), ("Rutos Letter", 2), ("Boomerang", 1), ('isadult', 0), ('Zeldas Lullaby', 1)]],
    "Phantom Ganon":                                         [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', 5), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1]), ('Boss Key (Forest Temple)', 1)],
    "Volvagia":                                              [('isadult', 1), ('Megaton Hammer', 1), ('Boss Key (Fire Temple)', 1)],
    "Morpha":                                                [('isadult', 1), ('Progressive Hookshot', 2), ('Boss Key (Water Temple)', 1)],
    "Bongo Bongo":                                           [[('isadult', 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Water Temple)", [5]), ('Progressive Hookshot', 1), ('Zeldas Lullaby', 1), ('Bow', 1), ('Boss Key (Shadow Temple)', 1)],
                                                              [('isadult', 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Water Temple)", [5]), ('Progressive Hookshot', 2), ('Zeldas Lullaby', 1), ('Boss Key (Shadow Temple)', 1)]],
    "Twinrova":                                              [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [5]), ('Mirror Shield', 1), ('Progressive Hookshot', [1]), ('Bomb Bag', 1), ('Boss Key (Spirit Temple)', 1)],
    "Song from Saria":                                       [('isadult', 0)],
    "Sheik in Forest":                                     [('isadult', 1)],
    "Song from Ocarina of Time":                             [('Kokiri Emerald', 1), ('Goron Ruby', 1), ('Zora Sapphire', 1), ('isadult', 0)],
    "Sheik at Colossus":                                     [[('Requiem of Spirit', 1)],
                                                              [('isadult', 1), ("has_access|GTG", 1)]],
    "Sheik at Temple":                                       [('Forest Medallion', 1), ('isadult', 1)],
    "Sheik in Kakariko":                                     [('Forest Medallion', 1), ('Fire Medallion', 1), ('Water Medallion', 1), ('isadult', 1)],
    "Song from Windmill":                                      [('isadult', 1)],
    "Song from Composers Grave":                              [('Zeldas Lullaby', 1)],
    "Sheik in Crater":                                       [('has_access|Fire', 1)],
    "Song from Malon":                                       [('isadult', 0)],
    "Sheik in Ice Cavern":                                   [[('isadult', 1), ('Rutos Letter', 2), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Rutos Letter', 2), ('Hover Boots', 1)]],
    "KF Kokiri Sword Chest":                                    [('isadult', 0)],
    "KF Midos Top Left Chest":                                   [],
    "KF Midos Top Right Chest":                                  [],
    "KF Midos Bottom Left Chest":                                [],
    "KF Midos Bottom Right Chest":                               [],
    "LW Skull Kid":                                             [('isadult', 0), ('Sarias Song', 1)],
    "LW Ocarina Memory Game":                                   [('isadult', 0)],
    "LW Target in Woods":                                       [('isadult', 0), ('Slingshot', 1)],
    "LW Deku Scrub Near Bridge":                      [('isadult', 0)],
    "LH Underwater Item":                                     [('isadult', 0), ("Progressive Scale", [1])],
    "LH Sun":                                                [[('isadult', 1), ('Bow', 1), ("Progressive Hookshot", 2)],
                                                              [('isadult', 1), ('Bow', 1), ('Boss Key (Water Temple)', 1)]],
    "LH Freestanding PoH":                                   [[("Progressive Hookshot", [1]), ('isadult', 1)],
                                                              [('isadult', 1), ('Magic Bean', 1)]],
    "LH Lab Dive":                                           [[('Progressive Scale', 2)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Iron Boots', 1)]],
    "LH Child Fishing":                                      [('isadult', 0)],
    "LH Adult Fishing":                                      [[('isadult', 1), ('Progressive Hookshot', [1])],
                                                              [('isadult', 1), ('Magic Bean', 1)]],
    "GV Waterfall Freestanding PoH":                         [[('isadult', 0)],
                                                              [('isadult', 1), ('Eponas Song', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', 2)]],
    "GV Crate Freestanding PoH":                             [[('isadult', 0)],
                                                              [('isadult', 1), ('Progressive Hookshot', 2)]],
    "GV Chest":                                              [('isadult', 1), ('has_access|GTG', 1), ('Megaton Hammer', 1)],
    "GF Chest":                                              [[('isadult', 1), ('has_access|GTG', 1), ('Progressive Hookshot', [1])],
                                                              [('isadult', 1), ('has_access|GTG', 1), ('Hover Boots', 1)]],
    "GF HBA 1000 Points":                                    [('isadult', 1), ('Eponas Song', 1), ('Bow', 1)],
    "GF HBA 1500 Points":                                    [('isadult', 1), ('Eponas Song', 1), ('Bow', 1)],
    "Wasteland Chest":                                       [[('isadult', 1), ('has_access|GTG', 1), ('Magic Meter', 1), ('Dins Fire', 1)],
															  [('isadult', 1), ('has_access|GTG', 1), ('Magic Meter', 1), ('Fire Arrows', 1), ('Bow', 1)]],
    "Colossus Freestanding PoH":                             [('isadult', 1), ('Magic Bean', 1), ('Requiem of Spirit', 1)],
    "Colossus Great Fairy Reward":                           [[('isadult', 1), ('Eponas Song', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', 2), ('Bomb Bag', 1)],
                                                              [('Requiem of Spirit', 1), ('Bomb Bag', 1)]],
    "HC Great Fairy Reward":                            [('isadult', 0), ('Bomb Bag', 1), ('Zeldas Lullaby', 1)],
    "OGC Great Fairy Reward":                            [('isadult', 1), ('Progressive Strength Upgrade', 3), ('Zeldas Lullaby', 1)],
    "Market 10 Big Poes":                                    [[('isadult', 1), ('Eponas Song', 1), ('Bow', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('Big Poe', 1)]],
    "Market Shooting Gallery Reward":                                [('isadult', 0)],
    "Market Bombchu Bowling First Prize":                              [('isadult', 0), ('Bomb Bag', 1)],
    "Market Bombchu Bowling Second Prize":                        [('isadult', 0), ('Bomb Bag', 1)],
    "Market Treasure Chest Game Reward":                                   [('isadult', 0), ('Lens of Truth', 1)],
    "Market Lost Dog":                                              [('isadult', 0)],
    "Kak Anju as Adult":                                         [('isadult', 1)],
    "Kak Anju as Child":                                        [('isadult', 0)],
    "Kak Man on Roof":                                           [('isadult', 1)],
    "Kak 10 Gold Skulltula Reward":                              [('Gold Skulltula Token', [10])],
    "Kak 20 Gold Skulltula Reward":                              [('Gold Skulltula Token', [20])],
    "Kak 30 Gold Skulltula Reward":                              [('Gold Skulltula Token', [30])],
    "Kak 40 Gold Skulltula Reward":                              [('Gold Skulltula Token', [40])],
    "Kak 50 Gold Skulltula Reward":                              [('Gold Skulltula Token', 50)],
    "Kak Impas House Freestanding PoH":                           [('isadult', 1)],
    "Kak Windmill Freestanding PoH":                             [('isadult', 1)],
    "Kak Shooting Gallery Reward":                                [('isadult', 1), ('Bow', 1)],
    "Graveyard Freestanding PoH":                            [[('isadult', 0), ('Boomerang', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', 2)],
                                                              [('isadult', 1), ('Magic Bean', 1)]],
    "Graveyard Dampe Gravedigging Tour":                                     [('isadult', 0)],
    "Graveyard Shield Grave Chest":                                    [],
    "Graveyard Heart Piece Grave Chest":                               [('Suns Song', 1)],
    "Graveyard Composers Grave Chest":                                  [[('isadult', 0), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Zeldas Lullaby', 1), ('Magic Meter', 1), ('Dins Fire', 1)],
                                                              [('isadult', 1), ('Zeldas Lullaby', 1), ('Magic Meter', 1), ('Fire Arrows', 1), ('Bow', 1)]],
    "Graveyard Hookshot Chest":                                        [('isadult', 1)],
    "Graveyard Dampe Race Freestanding PoH":                           [('isadult', 1)],
    "DMT Chest":                                            [[('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Progressive Strength Upgrade', [1])],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "DMT Freestanding PoH":                             [],
    "DMT Biggoron":                                              [('adult trade sequence', 4), ('isadult', 1)],
    "GC Maze Left Chest":                        [[('isadult', 1), ('Megaton Hammer', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [2])]],
    "GC Maze Center Chest":                            [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [2])],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "GC Maze Right Chest":                           [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [2])],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "GC Pot Freestanding PoH":                       [[('isadult', 0), ('Bomb Bag', 1), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 0), ('Bomb Bag', 1), ('Dins Fire', 1), ('Magic Meter', 1)]],
    "GC Rolling Goron as Child":                                [('isadult', 0), ('Bomb Bag', 1)],
    "GC Rolling Goron as Adult":                                        [[('isadult', 1), ('Bow', 1)],
                                                              [('isadult', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1])]],
    "GC Darunias Joy":                                          [('isadult', 0), ('Zeldas Lullaby', 1), ('Sarias Song', 1)],
    "DMC Volcano Freestanding PoH":                       [[('isadult', 1), ('Bow', 1), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Bomb Bag', 1), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1]), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Magic Bean', 1), ('Bolero of Fire', 1)],
                                                              [('isadult', 1), ('Hover Boots', 1), ('Bolero of Fire', 1)]],
    "DMC Wall Freestanding PoH":                    [[('Bomb Bag', 1)],
                                                     [('Magic Bean', 1), ('Bolero of Fire', 1), ('isadult', 1)],
                                                     [('isadult', 1), ('Megaton Hammer', 1)],
                                                     [('Bolero of Fire', 1), ('isadult', 1), ('Hover Boots', 1)],
                                                     [('Bolero of Fire', 1), ('isadult', 1), ('Progressive Hookshot', [1])],
                                                     [('Progressive Strength Upgrade', [1]), ('isadult', 1)],
                                                     [('Bow', 1), ('isadult', 1)],
                                                     [('Dins Fire', 1), ('isadult', 1), ('Magic Meter', 1)]],
    "DMC Great Fairy Reward":                                   [[('isadult', 1), ('Bow', 1), ('Megaton Hammer', 1), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Bomb Bag', 1), ('Megaton Hammer', 1), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1]), ('Megaton Hammer', 1), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Bolero of Fire', 1), ('Megaton Hammer', 1), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Hover Boots', [1]), ('Bolero of Fire', 1), ('Megaton Hammer', 1), ('Zeldas Lullaby', 1)]],
    "DMT Great Fairy Reward":                          [[('Bomb Bag', 1), ('Zeldas Lullaby', 1)],
                                                        [('isadult', 1), ('Megaton Hammer', 1), ('Zeldas Lullaby', 1)]],
    "ZR Frogs Ocarina Game":                                     [[('Zeldas Lullaby', 1), ('Sarias Song', 1), ('Suns Song', 1), ('Song of Storms', 1), ('Eponas Song', 1), ('Song of Time', 1), ('Bomb Bag', 1), ('isadult', 0)],
                                                              [('Zeldas Lullaby', 1), ('Sarias Song', 1), ('Suns Song', 1), ('Song of Storms', 1), ('Eponas Song', 1), ('Song of Time', 1), ('Progressive Scale', [1]), ('isadult', 0)]],
    "ZR Frogs in the Rain":                                     [[('isadult', 0), ('Song of Storms', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Song of Storms', 1), ('Progressive Scale', [1])]],
    "ZR Near Open Grotto Freestanding PoH":                     [[('isadult', 1)],
                                                              [('isadult', 0), ('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Progressive Scale', [1])]],
    "ZR Near Domain Freestanding PoH":                     [[('isadult', 1)],
                                                              [('isadult', 0), ('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Progressive Scale', [1])]],
    "ZD Diving Minigame":                                       [[('isadult', 0), ('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Progressive Scale', [1])]],
    "ZD Chest":                                [[('isadult', 0), ('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Progressive Scale', [1])]],
    "ZD King Zora Thawed":                                      [[('isadult', 1), ('Bottle', 1), ("has_access|Trials", 1), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Bottle', 1), ("has_access|Trials", 1), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Bottle', 1), ('Rutos Letter', 2), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Bottle', 1), ('Rutos Letter', 2), ('Hover Boots', 1)]],
    "ZF Iceberg Freestanding PoH":               [[('isadult', 1), ('Rutos Letter', 2), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ('Rutos Letter', 2), ('Hover Boots', 1)]],
    "ZF Bottom Freestanding PoH":                [[('isadult', 1), ('Rutos Letter', 2), ('Zeldas Lullaby', 1), ('Iron Boots', 1)],
                                                              [('isadult', 1), ('Rutos Letter', 2), ('Hover Boots', 1), ('Iron Boots', 1)]],
    "ZF Great Fairy Reward":                           [('Rutos Letter', 2), ('Bomb Bag', 1), ('Zeldas Lullaby', 1)],
    "LLR Talons Chickens":                                       [('isadult', 0)],
    "LLR Freestanding PoH":                        [('isadult', 0)],
    "Ganons Tower Boss Key Chest":                           [("has_access|Trials", 1), ('isadult', 1)],
    "KF Storms Grotto Chest":                     [('Song of Storms', 1)],
    "LW Near Shortcuts Grotto Chest":                       [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "Deku Theater Skull Mask":                               [('child trade sequence', 3), ('isadult', 0)],
    "LW Deku Scrub Grotto Front":                 [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "SFM Wolfos Grotto Chest":                                   [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "HF Open Grotto Chest":                          [],
    "HF Southeast Grotto Chest":            [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "HF Deku Scrub Grotto":                   [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "HF Near Market Grotto Chest":                   [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "HF Tektite Grotto Freestanding PoH":                       [[('Bomb Bag', 1), ('Progressive Scale', 2)],
                                                              [('isadult', 1), ('Megaton Hammer', 1), ('Progressive Scale', 2)],
                                                              [('isadult', 1), ('Megaton Hammer', 1), ('Iron Boots', 1)]],
    "Kak Redead Grotto Chest":                                   [[('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)]],
    "Kak Open Grotto Chest":                            [('isadult', 1)],
    "DMT Storms Grotto Chest":                          [('Song of Storms', 1)],
    "DMC Upper Grotto Chest":                            [('Bomb Bag', 1)],
    "ZR Open Grotto Chest":                  [[('isadult', 1)],
                                                              [('isadult', 0), ('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Progressive Scale', [1])]],
    "Deku Tree Map Chest":                                 [('isadult', 0), ('Kokiri Sword', 1)],
    "Deku Tree Compass Chest":                               [('isadult', 0), ('Kokiri Sword', 1)],
    "Deku Tree Compass Room Side Chest":                     [('isadult', 0), ('Kokiri Sword', 1)],
    "Deku Tree Basement Chest":                              [('isadult', 0), ('Kokiri Sword', 1)],
    "Deku Tree Slingshot Chest":                             [('isadult', 0), ('Kokiri Sword', 1)],
    "Deku Tree Slingshot Room Side Chest":                   [('isadult', 0), ('Kokiri Sword', 1)],
    "Deku Tree Queen Gohma Heart":                           [('isadult', 0), ('Kokiri Sword', 1)],
    "Dodongos Cavern Map Chest":                             [[('isadult', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1])]],
    "Dodongos Cavern Compass Chest":                         [[('isadult', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1])]],
    "Dodongos Cavern Bomb Flower Platform Chest":                  [[('isadult', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1), ('Bow', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1])]],
    "Dodongos Cavern Bomb Bag Chest":                        [[('isadult', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1), ('Bow', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1])]],
    "Dodongos Cavern End of Bridge Chest":                   [[('isadult', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1), ('Bow', 1)],
                                                              [('isadult', 1), ('Megaton Hammer', 1), ('Progressive Strength Upgrade', [1])]],
    "Dodongos Cavern Boss Room Chest":                              [('isadult', 1), ('Bomb Bag', 1)],
    "Dodongos Cavern King Dodongo Heart":                                    [('isadult', 1), ('Bomb Bag', 1)],
    "Jabu Jabus Belly Boomerang Chest":                                       [[('isadult', 0), ('Rutos Letter', 2), ('Progressive Scale', [1]), ('Slingshot', 1)],
                                                              [('isadult', 0), ('Rutos Letter', 2), ('Progressive Scale', [1]), ('Boomerang', 1)],
                                                              [('isadult', 0), ('Rutos Letter', 2), ('Bomb Bag', 1)]],
    "Jabu Jabus Belly Map Chest":                            [[('isadult', 0), ('Rutos Letter', 2), ('Progressive Scale', [1]), ('Boomerang', 1)],
                                                              [('isadult', 0), ('Rutos Letter', 2), ('Bomb Bag', 1), ('Boomerang', 1)]],
    "Jabu Jabus Belly Compass Chest":                        [[('isadult', 0), ('Rutos Letter', 2), ('Progressive Scale', [1]), ('Boomerang', 1)],
                                                              [('isadult', 0), ('Rutos Letter', 2), ('Bomb Bag', 1), ('Boomerang', 1)]],
    "Jabu Jabus Belly Barinade Heart":                                        [[('isadult', 0), ('Rutos Letter', 2), ('Progressive Scale', [1]), ('Boomerang', 1)],
                                                              [('isadult', 0), ('Rutos Letter', 2), ('Bomb Bag', 1), ('Boomerang', 1)]],
    "Forest Temple First Room Chest":                             [('isadult', 1), ('Progressive Hookshot', [1])],
    "Forest Temple First Stalfos Chest":                      [('isadult', 1), ('Progressive Hookshot', [1])],
    "Forest Temple Raised Island Courtyard Chest":                  [[('isadult', 1), ('Progressive Hookshot', [1]), ('Bow', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Song of Time', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Progressive Strength Upgrade', [1])]],
    "Forest Temple Well Chest":                              [[('isadult', 1), ('Progressive Hookshot', [1]), ('Bow', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Song of Time', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Progressive Strength Upgrade', [1])]],
    "Forest Temple Map Chest":                               [[('isadult', 1), ('Progressive Hookshot', [1]), ('Bow', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Song of Time', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Progressive Strength Upgrade', [1])]],
    "Forest Temple Falling Ceiling Room Chest":             [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', 5), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1])],
    "Forest Temple Eye Switch Chest":                        [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', [1]), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1])],
    "Forest Temple Boss Key Chest":                          [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', [2]), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1])],
    "Forest Temple Floormaster Chest":                       [[('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Hover Boots', 1)],
                                                              [('isadult', 1), ('Progressive Hookshot', [1]), ('Small Key (Forest Temple)', [1]), ('Progressive Strength Upgrade', [1])]],
    "Forest Temple Bow Chest":                               [('isadult', 1), ('Small Key (Forest Temple)', [3]), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1])],
    "Forest Temple Red Poe Chest":                           [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', [3]), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1])],
    "Forest Temple Blue Poe Chest":                          [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', [3]), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1])],
    "Forest Temple Basement Chest":                         [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', 5), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1])],
    "Forest Temple Phantom Ganon Heart":                                   [('isadult', 1), ('Bow', 1), ('Small Key (Forest Temple)', 5), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', [1]), ('Boss Key (Forest Temple)', 1)],
    "Bottom of the Well Front Left Fake Wall Chest":             [('isadult', 0), ('Song of Storms', 1)],
    "Bottom of the Well Front Center Bombable Chest":              [('isadult', 0), ('Song of Storms', 1), ('Bomb Bag', 1)],
    "Bottom of the Well Right Bottom Fake Wall Chest":           [('isadult', 0), ('Song of Storms', 1)],
    "Bottom of the Well Compass Chest":                 [('isadult', 0), ('Song of Storms', 1)],
    "Bottom of the Well Center Skulltula Chest":                 [('isadult', 0), ('Song of Storms', 1)],
    "Bottom of the Well Back Left Bombable Chest":                 [('isadult', 0), ('Song of Storms', 1), ('Bomb Bag', 1)],
    "Bottom of the Well Freestanding Key":                   [('isadult', 0), ('Song of Storms', 1)],
    "Bottom of the Well Lens of Truth Chest":                        [('isadult', 0), ('Song of Storms', 1), ('Zeldas Lullaby', 1)],
    "Bottom of the Well Invisible Chest":                    [('isadult', 0), ('Song of Storms', 1), ('Zeldas Lullaby', 1)],
    "Bottom of the Well Underwater Front Chest":             [('isadult', 0), ('Song of Storms', 1), ('Zeldas Lullaby', 1)],
    "Bottom of the Well Underwater Left Chest":              [('isadult', 0), ('Song of Storms', 1), ('Zeldas Lullaby', 1)],
    "Bottom of the Well Map Chest":                     [[('isadult', 0), ('Song of Storms', 1), ('Bomb Bag', 1)],
                                                              [('isadult', 0), ('Song of Storms', 1), ('Progressive Strength Upgrade', [1])]],
    "Bottom of the Well Fire Keese Chest":                        [('isadult', 0), ('Song of Storms', 1)],
    "Bottom of the Well Like Like Chest":                 [('isadult', 0), ('Song of Storms', 1)],
    "Fire Temple Near Boss Chest":                           [('isadult', 1), ("has_access|Fire", 1)],
    "Fire Temple Flare Dancer Chest":                         [('isadult', 1), ("has_access|Fire", 1), ('Megaton Hammer', 1)],
    "Fire Temple Boss Key Chest":                            [('isadult', 1), ("has_access|Fire", 1), ('Megaton Hammer', 1)],
    "Fire Temple Volvagia Heart":                                        [('isadult', 1), ("has_access|Fire", 1), ('Megaton Hammer', 1), ('Boss Key (Fire Temple)', 1)],
    "Fire Temple Big Lava Room Lower Open Door Chest":       [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [1])],
    "Fire Temple Big Lava Room Blocked Door Chest":          [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [1]), ('Bomb Bag', 1)],
    "Fire Temple Boulder Maze Lower Chest":                  [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [3])],
    "Fire Temple Boulder Maze Upper Chest":                  [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [5])],
    "Fire Temple Boulder Maze Side Room Chest":                    [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [3])],
    "Fire Temple Boulder Maze Shortcut Chest":                 [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [5]), ('Bomb Bag', 1)],
    "Fire Temple Scarecrow Chest":                           [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [5]), ('Progressive Hookshot', [1])],
    "Fire Temple Map Chest":                                 [[('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [5])],
                                                              [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [4]), ('Bow', 1)]],
    "Fire Temple Compass Chest":                             [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [6])],
    "Fire Temple Highest Goron Chest":                       [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [6]), ('Megaton Hammer', 1)],
    "Fire Temple Megaton Hammer Chest":                      [[('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [6]), ('Bomb Bag', 1)],
                                                              [('isadult', 1), ("has_access|Fire", 1), ('Small Key (Fire Temple)', [6]), ('Progressive Hookshot', [1])]],
    "Ice Cavern Map Chest":                                  [[('isadult', 1), ('Hover Boots', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('Zeldas Lullaby', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('has_spawn|ZD', 1), ('Bottle', 1)]],
    "Ice Cavern Compass Chest":                              [[('isadult', 1), ('Hover Boots', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('Zeldas Lullaby', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('has_spawn|ZD', 1), ('Bottle', 1)]],
    "Ice Cavern Iron Boots Chest":                           [[('isadult', 1), ('Hover Boots', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('Zeldas Lullaby', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('has_spawn|ZD', 1), ('Bottle', 1)]],
    "Ice Cavern Freestanding PoH":                           [[('isadult', 1), ('Hover Boots', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('Zeldas Lullaby', 1), ('Bottle', 1)],
                                                              [('isadult', 1), ('has_spawn|ZD', 1), ('Bottle', 1)]],
    "Water Temple Morpha Heart":                             [('isadult', 1), ("has_access|Water", 1), ('Progressive Hookshot', 2), ('Boss Key (Water Temple)', 1)],
    "Water Temple Map Chest":                                [('isadult', 1), ("has_access|Water", 1)],
    "Water Temple Compass Chest":                            [('isadult', 1), ("has_access|Water", 1)],
    "Water Temple Torches Chest":                            [[('isadult', 1), ("has_access|Water", 1), ('Bow', 1), ('Zeldas Lullaby', 1)],
                                                              [('isadult', 1), ("has_access|Water", 1), ('Dins Fire', 1), ('Magic Meter', 1), ('Zeldas Lullaby', 1)]],
    "Water Temple Central Bow Target Chest":                 [[('isadult', 1), ("has_access|Water", 1), ('Bow', 1), ('Zeldas Lullaby', 1), ('Progressive Strength Upgrade', [1]), ('Progressive Hookshot', 2)],
                                                              [('isadult', 1), ("has_access|Water", 1), ('Bow', 1), ('Zeldas Lullaby', 1), ('Progressive Strength Upgrade', [1]), ('Hover Boots', 1)]],
    "Water Temple Boss Key Chest":                           [[("Small Key (Water Temple)", [5]), ('isadult', 1), ("has_access|Water", 1), ('Hover Boots', 1)],
                                                              [("Small Key (Water Temple)", [5]), ('isadult', 1), ("has_access|Water", 1), ('Progressive Hookshot', 2)]],
    "Water Temple Cracked Wall Chest":                       [('isadult', 1), ("has_access|Water", 1), ('Zeldas Lullaby', 1), ('Bomb Bag', 1)],
    "Water Temple Dragon Chest":                             [[('isadult', 1), ("Small Key (Water Temple)", [5]), ('Bow', 1)],
                                                              [('isadult', 1), ("Small Key (Water Temple)", [5]), ('Iron Boots', 1)],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [1]), ("has_access|Water", 1), ('Zeldas Lullaby', 1)]],
    "Water Temple Central Pillar Chest":                     [('isadult', 1), ('Iron Boots', 1), ('Zeldas Lullaby', 1)],
    "Water Temple Longshot Chest":                          [('isadult', 1), ("Small Key (Water Temple)", [5])],
    "Water Temple River Chest":                              [('isadult', 1), ("Small Key (Water Temple)", [5]), ('Song of Time', 1), ('Bow', 1)],
    "Shadow Temple Map Chest":                               [('isadult', 1), ("has_access|Shadow", 1)],
    "Shadow Temple Hover Boots Chest":                       [('isadult', 1), ("has_access|Shadow", 1)],
    "Shadow Temple Compass Chest":                           [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1)],
    "Shadow Temple Early Silver Rupee Chest":                [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1)],
    "Shadow Temple Invisible Blades Visible Chest":          [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [1])],
    "Shadow Temple Invisible Blades Invisible Chest":        [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [1])],
    "Shadow Temple Falling Spikes Lower Chest":              [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [1])],
    "Shadow Temple Falling Spikes Upper Chest":              [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [1])],
    "Shadow Temple Falling Spikes Switch Chest":             [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [1])],
    "Shadow Temple Invisible Spikes Chest":                  [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [2])],
    "Shadow Temple Freestanding Key":                        [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [2]), ('Progressive Hookshot', [1])],
    "Shadow Temple Wind Hint Chest":                         [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [3]), ('Progressive Hookshot', [1])],
    "Shadow Temple After Wind Enemy Chest":                  [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [3]), ('Progressive Hookshot', [1])],
    "Shadow Temple After Wind Hidden Chest":                 [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [3]), ('Progressive Hookshot', [1])],
    "Shadow Temple Spike Walls Left Chest":                  [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [4]), ('Progressive Hookshot', [1]), ('Zeldas Lullaby', 1)],
    "Shadow Temple Boss Key Chest":                          [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [4]), ('Progressive Hookshot', [1]), ('Zeldas Lullaby', 1)],
    "Shadow Temple Invisible Floormaster Chest":                [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [4]), ('Progressive Hookshot', [1]), ('Zeldas Lullaby', 1)],
    "Shadow Temple Bongo Bongo Heart":                                     [[('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [5]), ('Progressive Hookshot', 1), ('Zeldas Lullaby', 1), ('Bow', 1), ('Boss Key (Shadow Temple)', 1)],
                                                              [('isadult', 1), ("has_access|Shadow", 1), ('Hover Boots', 1), ('Bomb Bag', 1), ("Small Key (Shadow Temple)", [5]), ('Progressive Hookshot', 2), ('Zeldas Lullaby', 1), ('Boss Key (Shadow Temple)', 1)]],
    "Gerudo Training Grounds Lobby Left Chest":              [('isadult', 1), ("has_access|GTG", 1), ('Bow', 1)],
    "Gerudo Training Grounds Lobby Right Chest":             [('isadult', 1), ("has_access|GTG", 1), ('Bow', 1)],
    "Gerudo Training Grounds Stalfos Chest":                 [('isadult', 1), ("has_access|GTG", 1)],
    "Gerudo Training Grounds Beamos Chest":                  [('isadult', 1), ("has_access|GTG", 1), ('Bomb Bag', 1)],
    "Gerudo Training Grounds Hidden Ceiling Chest":          [('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [3])],
    "Gerudo Training Grounds Maze Path First Chest":         [('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [4])],
    "Gerudo Training Grounds Maze Path Second Chest":        [('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [5])],
    "Gerudo Training Grounds Maze Path Third Chest":         [('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [7])],
    "Gerudo Training Grounds Maze Path Final Chest":         [('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [9])],
    "Gerudo Training Grounds Maze Right Central Chest":      [[('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [9])],
                                                              [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Song of Time', 1)],
                                                              [('isadult', 1), ("has_access|GTG", 1), ('Bomb Bag', 1), ('Song of Time', 1)]],
    "Gerudo Training Grounds Maze Right Side Chest":         [[('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [9])],
                                                              [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Song of Time', 1)],
                                                              [('isadult', 1), ("has_access|GTG", 1), ('Bomb Bag', 1), ('Song of Time', 1)]],
    "Gerudo Training Grounds Freestanding Key":              [[('isadult', 1), ("has_access|GTG", 1), ('Small Key (Gerudo Training Grounds)', [9])],
                                                              [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Song of Time', 1)],
                                                              [('isadult', 1), ("has_access|GTG", 1), ('Bomb Bag', 1), ('Song of Time', 1)]],
    "Gerudo Training Grounds Underwater Silver Rupee Chest": [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Song of Time', 1), ('Iron Boots', 1)],
    "Gerudo Training Grounds Hammer Room Clear Chest":       [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1])],
    "Gerudo Training Grounds Hammer Room Switch Chest":      [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1])],
    "Gerudo Training Grounds Eye Statue Chest":              [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Bow', 1)],
    "Gerudo Training Grounds Near Scarecrow Chest":          [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Bow', 1)],
    "Gerudo Training Grounds Before Heavy Block Chest":      [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1])],
    "Gerudo Training Grounds Heavy Block First Chest":       [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Progressive Strength Upgrade', [2])],
    "Gerudo Training Grounds Heavy Block Second Chest":      [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Progressive Strength Upgrade', [2])],
    "Gerudo Training Grounds Heavy Block Third Chest":       [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Progressive Strength Upgrade', [2])],
    "Gerudo Training Grounds Heavy Block Fourth Chest":      [('isadult', 1), ("has_access|GTG", 1), ('Progressive Hookshot', [1]), ('Progressive Strength Upgrade', [2])],
    "Spirit Temple Child Bridge Chest":                        [[('Requiem of Spirit', 1), ('Boomerang', 1), ('isadult', 0)],
                                                              [('Requiem of Spirit', 1), ('Slingshot', 1), ('isadult', 0)]],
    "Spirit Temple Child Early Torches Chest":               [[('Requiem of Spirit', 1), ('Boomerang', 1), ('isadult', 0)],
                                                              [('Requiem of Spirit', 1), ('Slingshot', 1), ('isadult', 0)]],
    "Spirit Temple Child Climb East Chest":                  [[('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Boomerang', 1), ('Bow', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Boomerang', 1), ('Progressive Hookshot', [1])],
                                                              [('Small Key (Spirit Temple)', [1]), ('Slingshot', 1), ('Bow', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Slingshot', 1), ('Progressive Hookshot', [1])]],
    "Spirit Temple Child Climb North Chest":                 [[('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Boomerang', 1), ('Bow', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Boomerang', 1), ('Progressive Hookshot', [1])],
                                                              [('Small Key (Spirit Temple)', [1]), ('Slingshot', 1), ('Bow', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Slingshot', 1), ('Progressive Hookshot', [1])]],
    "Spirit Temple Compass Chest":                           [("has_access|Spirit", 1), ('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Zeldas Lullaby', 1), ('Progressive Hookshot', [1])],
    "Spirit Temple Early Adult Right Chest":                 [[("has_access|Spirit", 1), ('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Bomb Bag', 1)],
                                                              [("has_access|Spirit", 1), ('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Bow', 1)],
                                                              [("has_access|Spirit", 1), ('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Progressive Hookshot', [1])]],
    "Spirit Temple First Mirror Right Chest":                [("has_access|Spirit", 1), ('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [3])],
    "Spirit Temple First Mirror Left Chest":                 [("has_access|Spirit", 1), ('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [3])],
    "Spirit Temple Map Chest":                               [[('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1), ('Magic Meter', 1), ('Dins Fire', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1), ('Magic Meter', 1), ('Dins Fire', 1), ('isadult', 0), ('Requiem of Spirit', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1), ('Magic Meter', 1), ('Bow', 1), ('Fire Arrows', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [3]), ('Progressive Strength Upgrade', [2]), ('Magic Meter', 1), ('Bow', 1), ('Fire Arrows', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [3]), ('Progressive Strength Upgrade', [2]), ('Magic Meter', 1), ('Dins Fire', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [5]), ('Bomb Bag', 1), ('Requiem of Spirit', 1), ('isadult', 0)]],
    "Spirit Temple Sun Block Room Chest":                    [[('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1), ('Magic Meter', 1), ('Dins Fire', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1), ('Magic Meter', 1), ('Dins Fire', 1), ('isadult', 0), ('Requiem of Spirit', 1)],
                                                              [('Small Key (Spirit Temple)', [1]), ('Bomb Bag', 1), ('Magic Meter', 1), ('Bow', 1), ('Fire Arrows', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [3]), ('Progressive Strength Upgrade', [2]), ('Magic Meter', 1), ('Bow', 1), ('Fire Arrows', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [3]), ('Progressive Strength Upgrade', [2]), ('Magic Meter', 1), ('Dins Fire', 1), ('isadult', 1)],
                                                              [('Small Key (Spirit Temple)', [5]), ('Bomb Bag', 1), ('Requiem of Spirit', 1), ('isadult', 0)]],
    "Spirit Temple Statue Room Hand Chest":                       [("has_access|Spirit", 1), ('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [3]), ('Zeldas Lullaby', 1)],
    "Spirit Temple Statue Room Northeast Chest":                      [[('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [3]), ('Zeldas Lullaby', 1), ('Progressive Hookshot', [1])],
                                                              [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [3]), ('Zeldas Lullaby', 1), ('Hover Boots', 1)]],
    "Spirit Temple Silver Gauntlets Chest":                                [[('Small Key (Spirit Temple)', [3]), ('Progressive Strength Upgrade', [2]), ('isadult', 1), ('Progressive Hookshot', 2)],
                                                              [('Small Key (Spirit Temple)', 5)]],
    "Spirit Temple Mirror Shield Chest":                                   [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [4]), ('Bomb Bag', 1)],
    "Spirit Temple Near Four Armos Chest":                   [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [4]), ('Bomb Bag', 1), ('Mirror Shield', 1)],
    "Spirit Temple Hallway Left Invisible Chest":            [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [4]), ('Bomb Bag', 1)],
    "Spirit Temple Hallway Right Invisible Chest":           [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [4]), ('Bomb Bag', 1)],
    "Spirit Temple Boss Key Chest":                          [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [5]), ('Zeldas Lullaby', 1)],
    "Spirit Temple Topmost Chest":                           [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [5]), ('Mirror Shield', 1)],
    "Spirit Temple Twinrova Heart":                                        [('isadult', 1), ('Progressive Strength Upgrade', [2]), ('Small Key (Spirit Temple)', [5]), ('Mirror Shield', 1), ('Progressive Hookshot', [1]), ('Bomb Bag', 1), ('Boss Key (Spirit Temple)', 1)],
    "Ganons Castle Forest Trial Chest":                      [("has_access|Trials", 1), ('isadult', 1)],
    "Ganons Castle Water Trial Left Chest":                  [("has_access|Trials", 1), ('isadult', 1)],
    "Ganons Castle Water Trial Right Chest":                 [("has_access|Trials", 1), ('isadult', 1)],
    "Ganons Castle Shadow Trial Front Chest":                [[("has_access|Trials", 1), ('isadult', 1), ('Hover Boots', 1)],
                                                              [("has_access|Trials", 1), ('isadult', 1), ('Song of Time', 1)],
                                                              [("has_access|Trials", 1), ('isadult', 1), ('Progressive Hookshot', [1])],
                                                              [("has_access|Trials", 1), ('isadult', 1), ('Bow', 1), ('Fire Arrows', 1), ('Magic Meter', 1)]],
    "Ganons Castle Shadow Trial Golden Gauntlets Chest":     [[("has_access|Trials", 1), ('isadult', 1), ('Progressive Hookshot', 2), ('Dins Fire', 1), ('Magic Meter', 1)],
                                                              [("has_access|Trials", 1), ('isadult', 1), ('Bow', 1), ('Fire Arrows', 1), ('Magic Meter', 1)],
                                                              [("has_access|Trials", 1), ('isadult', 1), ('Progressive Hookshot', 2), ('Hover Boots', 1)]],
    "Ganons Castle Spirit Trial Crystal Switch Chest":                [("has_access|Trials", 1), ('isadult', 1), ('Progressive Hookshot', [1])],
    "Ganons Castle Spirit Trial Invisible Chest":               [[("has_access|Trials", 1), ('isadult', 1), ('Progressive Hookshot', [1]), ('Bomb Bag', 1)],
                                                              [("has_access|Trials", 1), ('isadult', 1), ('Progressive Hookshot', [1]), ('Bow', 1)]],
    "Ganons Castle Light Trial First Left Chest":            [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3)],
    "Ganons Castle Light Trial Second Left Chest":           [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3)],
    "Ganons Castle Light Trial Third Left Chest":            [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3)],
    "Ganons Castle Light Trial First Right Chest":           [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3)],
    "Ganons Castle Light Trial Second Right Chest":          [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3)],
    "Ganons Castle Light Trial Third Right Chest":           [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3)],
    "Ganons Castle Light Trial Invisible Enemies Chest":     [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3)],
    "Ganons Castle Light Trial Lullaby Chest":               [("has_access|Trials", 1), ('isadult', 1), ('Progressive Strength Upgrade', 3), ('Zeldas Lullaby', 1)]
    }


dungeons_acess = {
    'GTG':      [[('isadult', 1), ('Progressive Hookshot', 2)],
                  [('isadult', 1), ('Eponas Song', 1)],
                  [('isadult', 1), ('has_spawn|GV GF Side', 1)],
                  [('isadult', 1), ('has_spawn|GF', 1)],
				  [('isadult', 1), ('Requiem of Spirit', 1)]],
    'Fire':     [[('isadult', 1), ('Bolero of Fire', 1)],
                 [('isadult', 1), ('Hover Boots', 1), ('Bomb Bag', 1)],
                 [('isadult', 1), ('Hover Boots', 1), ('Megaton Hammer', 1)],
                 [('isadult', 1), ('Progressive Hookshot', [1]), ('Bomb Bag', 1)],
                 [('isadult', 1), ('Progressive Hookshot', [1]), ('Bow', 1)],
                 [('isadult', 1), ('Hover Boots', 1), ('Bow', 1)],
                 [('isadult', 1), ('Hover Boots', 1), ('Progressive Strength Upgrade', [1])],
                 [('isadult', 1), ('Progressive Hookshot', [1]), ('Progressive Strength Upgrade', [1])],
                 [('isadult', 1), ('Progressive Hookshot', 2), ('Megaton Hammer', 1)]],
    'Water':    [[('isadult', 1), ('Progressive Scale', 2), ('Progressive Hookshot', 2)],
                 [('isadult', 1), ('Iron Boots', 1), ('Progressive Hookshot', [1])]],
    'Shadow':   [[('isadult', 1), ('Nocturne of Shadow', 1), ('Dins Fire', 1), ('Magic Meter', 1), ('Progressive Hookshot', [1])],
                 [('isadult', 1), ('Nocturne of Shadow', 1), ('Dins Fire', 1), ('Magic Meter', 1), ('Hover Boots', 1)]],
    'Spirit':   [[('Requiem of Spirit', 1)],
                 [('isadult', 1), ('Progressive Hookshot', 2)],
                 [('isadult', 1), ('Eponas Song', 1)]]
    }


additionnal_actions = {
    'Time Travel': ([], 'change_age'),
    'Deliver RL': ([[('Rutos Letter', 1), ('isadult', 0), ('Progressive Scale', [1])],
                    [('Rutos Letter', 1), ('isadult', 0), ('Bomb Bag', 1)],
                    [('Rutos Letter', 1), ('isadult', 0), ('has_spawn|ZD', 1)]], ["item_update|Rutos Letter", 'item_update|Bottle']),
    'Child Trade Sequence 1': ([('isadult', 0), ('child trade sequence', 0)], "item_update|child trade sequence"),
    'Child Trade Sequence 2': ([('isadult', 0), ('child trade sequence', 1)], "item_update|child trade sequence"),
    'Child Trade Sequence 3': ([('isadult', 0), ('child trade sequence', 2)], "item_update|child trade sequence"),
    'Adult Trade Sequence 1': ([[('isadult', 1), ('adult trade sequence', 1), ('Hover Boots', 1)],
                                [('isadult', 1), ('adult trade sequence', 1), ('Zeldas Lullaby', 1)]], "item_update|adult trade sequence"),
    'Adult Trade Sequence 2': ([('isadult', 1), ('adult trade sequence', 2)], "item_update|adult trade sequence"),
    'Adult Trade Sequence 3': ([('isadult', 1), ('adult trade sequence', 3), ('has_access|Biggoron', 1)], "item_update|adult trade sequence"),
    'Buy Magical Beans': ([[('isadult', 0), ('Bomb Bag', 1), ('Magic Bean', 0)],
                           [('isadult', 0), ('Progressive Scale', [1]), ('Magic Bean', 0)],
                           [('isadult', 0), ('has_spawn|ZR', 1)],
                           [('isadult', 0), ('has_spawn|ZD', 1)]], 'item_update|Magic Bean')
    }


MED_BRIDGE = 2
def bridge_open(nb_med_req, state):
    """
    Checks whether the bridge to GC is open according to Medallions.
    
    state(State): state of the player
    """
    return state.current_med() >= MED_BRIDGE


def is_where(zone, where):
    return zone == where

def has_spawn(zone, state):
    if state.items['isadult']['current'] == 0:
        return zone == state.child_spawn
    else:
        return zone == state.adult_spawn


def has_access(zone, state) -> bool:
    """
    Checks the conditions to access particular zone given a state.
    
    zone(str): zone whose conditions of access will be evaluated.
    state(State): state of the player.
    """
    if zone == 'Trials':
        return bridge_open(MED_BRIDGE, state)
    
    elif zone in dungeons_acess:
        if isinstance(dungeons_acess[zone][0], tuple):
            return requirements_in_logic(state, dungeons_acess[zone])
        else:
            return any([requirements_in_logic(state,rr) for rr in dungeons_acess[zone]])
    
    elif zone == 'Biggoron':
        req = [[('Bolero of Fire', 1), ('Progressive Hookshot', [1]), ('isadult', 1)],
               [('Bolero of Fire', 1), ('Hover Boots', 1), ('isadult', 1)],
               [('Bomb Bag', 1), ('isadult', 1)],
               [('Bow', 1), ('isadult', 1)],
               [('Progressive Strength Upgrade', [1]), ('isadult', 1)],
               [('Megaton Hammer', 1), ('isadult', 1)],
               [('Dins Fire', 1), ('Magic Meter', 1), ('isadult', 1)],
               [('isadult', 1), ('has_spawn|DMC Upper', 1)]]
        return any([requirements_in_logic(state, rr) for rr in req])
    
    else:
        logger.error(f'Zone {zone} not found in has_access function')
        return False


def in_logic(state, logic=mylogic):
    """
    Returns all checks that can be accessed according to played logic given a
    state.
    
    state(State): state of the player
    logic(dict): logic used
    """
    checks_in_logic = []
    for l, r in logic.items():
        if len(r) == 0:
            checks_in_logic.append(l)
        
        elif isinstance(r[0], tuple):  # Only one logic possible
            if requirements_in_logic(state, r):
                checks_in_logic.append(l)
        
        else:  # Many logics possible
            if any([requirements_in_logic(state, rr) for rr in r]):
                checks_in_logic.append(l)
    return checks_in_logic


def bool_logic(state, logic=mylogic):
    """
    Returns logic in the form of boolean array.
    """
    checks_in_logic = in_logic(state, logic)
    return [1 if check in checks_in_logic else 0 for check in logic]


def requirements_in_logic(state, requirements, where=None) -> bool:
    """
    Returns whether the requirements list is fullfilled by state or not.
    
    state(State): state of the player
    requirement(list): list of requirements in the form of tuples.
    where(str): location of the player
    """
    try:
        for (requirement, num) in requirements:
            if not requirement_in_logic(state, requirement, num, where):
                return False
        return True
    except:
        logger.error(f'Set of requirements: {requirements} badly formated')
        return False


def requirement_in_logic(state, requirement, number, where=None) -> bool:
    """
    Returns if the requirement is fullfilled by the state or not.
    
    state(State): state of the player
    requirement(str): name of the status to check
    number(int or list): exact or minimum state number to return True
    where(str): location of the player
    """
    
    if requirement in state.items:
        if isinstance(number, int):
            return state.items[requirement]['current'] == number
        else:  #should be a list
            try:
                return state.items[requirement]['current'] >= number[0]
            except Exception as e:
                logger.error(f'Unable to check requirement for check {requirement}'
                             f'due to {e}')
                return False
                
    else:
        if '|' not in requirement:
            logger.error(f'Requirement {requirement} not in correct form')
            return False
        
        function_name, param = requirement.split('|')
        try:
            if function_name == 'is_where':
                return is_where(param, where)
            else:
                return globals()[function_name](param, state)
        except Exception as e:
            logger.error(e)
            return False


def get_logic():
    return mylogic

def get_additionnal_actions():
    return additionnal_actions

def get_additionnal_logic(state):
    logic_array = []
    for (r, _) in additionnal_actions.values():
        if len(r) == 0:
            logic_array.append(True)
        elif isinstance(r[0], tuple):
            logic_array.append(requirements_in_logic(state, r))
        else:
            logic_array.append(any([requirements_in_logic(state, rr) for rr in r]))
    return logic_array