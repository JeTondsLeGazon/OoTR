"""
Test script for logic.py file
"""

import unittest
import sys
import logging
from datetime import datetime
import os

sys.path.append('..')
from src import logic
from src import state


LOG = 'error_log.log'
if os.path.isfile(LOG):
    logging.shutdown()
    os.remove(LOG)

class TestLogicMethods(unittest.TestCase):
    
    def test_1(self):
        mystate = {}
        check = []
        self.assertTrue(logic.requirements_in_logic(mystate, check))
                
    def test_2(self):
        mystate = state.State(base_items=[('isadult', 1, 0)])
        self.assertTrue(logic.requirement_in_logic(mystate, 'isadult', 0))
        self.assertFalse(logic.requirement_in_logic(mystate, 'isadult', 1))
        self.assertFalse(logic.requirement_in_logic(mystate, 'Slingshot', 1))
        
    def test_3(self):
        mystate = state.State(base_items=[('isadult', 1, 0), ('Progressive Hookshot', 2, 2)])
        self.assertTrue(logic.requirement_in_logic(mystate, 'Progressive Hookshot', [0]))
        self.assertTrue(logic.requirement_in_logic(mystate, 'Progressive Hookshot', [1]))
        self.assertTrue(logic.requirement_in_logic(mystate, 'Progressive Hookshot', 2))
        self.assertFalse(logic.requirement_in_logic(mystate, 'Progressive Hookshot', 1))
        
    def test_4(self):
        mystate = state.State(base_items=[('isadult', 1, 0), ('Progressive Hookshot', 2, 2)])
        self.assertTrue(logic.requirements_in_logic(mystate, [('isadult', 0), ('Progressive Hookshot', 2)]))
        self.assertTrue(logic.requirements_in_logic(mystate, [('isadult', [0]), ('Progressive Hookshot', 2)]))
        self.assertFalse(logic.requirements_in_logic(mystate, [('isadult', 1), ('Progressive Hookshot', 2)]))

    def test_5(self):
        mystate = state.State(base_items=[])
        mylogic = {"Impa at Castle": []}
        self.assertTrue(logic.in_logic(mystate, logic=mylogic))

    def test_6(self):
        mystate = state.State(base_items=[('isadult', 1, 1), ('Progressive Hookshot', 2, 2)])
        mylogic = {"Gerudo Training Grounds Stalfos Chest": [('isadult', 1), ("has_access|GTG", 1)]}
        self.assertEqual(logic.in_logic(mystate, logic=mylogic), ["Gerudo Training Grounds Stalfos Chest"])
        
    def test_7(self):
        mystate = state.State(base_items=[('isadult', 1, 1), ('Progressive Hookshot', 2, 2)])
        mylogic = {"Ganons Castle Forest Trial Chest": [("has_access|Trials", 1), ('isadult', 1)]}
        self.assertFalse(logic.in_logic(mystate, logic=mylogic))
        
    def test_8(self):
        mystate = state.State(base_items=[('isadult', 1, 1), ('Forest Medallion', 1, 1), ('Fire Medallion', 1, 1)])
        mylogic = {"Ganons Castle Forest Trial Chest": [("has_access|Trials", 1), ('isadult', 1)]}
        self.assertEqual(logic.in_logic(mystate, logic=mylogic), ["Ganons Castle Forest Trial Chest"])
        
    def test_9(self):
        mystate = state.State(base_items=[('isadult', 1, 1), ('Forest Medallion', 1, 0), ('Fire Medallion', 1, 1)])
        mylogic = {"Ganons Castle Forest Trial Chest": [("has_access|Trials", 1), ('isadult', 1)]}
        self.assertNotEqual(logic.in_logic(mystate, logic=mylogic), ["Ganons Castle Forest Trial Chest"])
    
    def test_10(self):
        mystate = state.State(base_items=[('isadult', 1, 1), ('Zeldas Lullaby', 1, 1)])
        mylogic = {
        "Song at Windmill": [('isadult', 1)],
        "Song from Composer Grave": [('Zeldas Lullaby', 1)],
        "Sheik in Crater": [('has_access|Fire', 1)],
        "Song from Malon": [('isadult', 0)],
        "Sheik in Ice Cavern": [[('isadult', 1), ('Rutos Letter', 2), ('Zeldas Lullaby', 1)],
                                [('isadult', 1), ('Rutos Letter', 2), ('Hover Boots', 1)]],
        "Kokiri Sword Chest": [('isadult', 0)]
        }
        self.assertEqual(logic.in_logic(mystate, logic=mylogic), ['Song at Windmill', 'Song from Composer Grave'])



if __name__ == '__main__':
    try:
        logging.basicConfig(filename=LOG, filemode='w')
        logger = logging.getLogger()
        logger.setLevel(0)
        logger.info(datetime.now().strftime("%H:%M:%S"))
        unittest.main()
    except:
        logging.shutdown()