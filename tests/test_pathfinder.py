import pytest

from src.pathfinder import PathFinder
from src.state import State


# TODO: redo tests


@pytest.fixture
def state() -> State:
    s = State(items_pool=[])
    s.set_age(0)
    s.child_spawn_location = "Graveyard"
    s.adult_spawn_location = "Temple of Time"
    return s


def test_pathfinder_init(state: State):
    # Arrange

    # Act
    p = PathFinder(state)

    # Assert
    assert p is not None
    assert len(p.locations_table) > 0
    assert len(p.locations_to_zones) > 0


def test_get_region_from_spawn():
    assert PathFinder.get_region_from_spawn("Graveyard") == "Graveyard"
    assert PathFinder.get_region_from_spawn("Temple of Time") == "Temple of Time"
    assert PathFinder.get_region_from_spawn("Kak Impas Ledge") == "Kak"
    assert PathFinder.get_region_from_spawn("Market") == "Market"


def test_pathfinder():
    s = State(items_pool=[])
    s.set_age(0)
    s.child_spawn_location = "Graveyard"
    s.adult_spawn_location = "Temple of Time"
    p = PathFinder(s)
    time, path = p.from_to("GV GF Side", "Graveyard", s)
    assert time == 15
    assert len(path) == 2


# class TestFromTo(unittest.TestCase):
#     def test2(self):
#         s = State()
#         s.set_age(1)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         p = PathFinder(s)
#         time, path = p.from_to("GV GF Side", "Graveyard", s)
#         self.assertLessEqual(time, 165)
#         self.assertIn("Temple of Time", path)
#
#     def test3(self):
#         s = State()
#         s.set_age(1)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         s.item_update("Bomb Bag")
#         p = PathFinder(s)
#         time, path = p.from_to("GC", "KF", s)
#         self.assertLessEqual(time, 60)
#         self.assertIn("LW", path)
#
#     def test4(self):
#         s = State()
#         s.set_age(1)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         p = PathFinder(s)
#         time, path = p.from_to("GC", "KF", s)
#         self.assertLessEqual(time, 200)
#         self.assertIn("Temple of Time", path)
#
#     def test5(self):
#         s = State()
#         s.set_age(0)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         s.item_update("Bow")
#         p = PathFinder(s)
#         time, path = p.from_to("GC", "KF", s)
#         self.assertLessEqual(time, 200)
#         self.assertIn("Graveyard", path)
#
#     def test6(self):
#         s = State()
#         s.set_age(0)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         p = PathFinder(s)
#         time, path = p.from_to("HF", "ZD", s)
#         self.assertEqual(time, -1)
#
#     def test7(self):
#         s = State()
#         s.set_age(1)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         s.item_update("Bow")
#         s.current_location = "GC"
#         p = PathFinder(s)
#         time, path = p.from_to("GC", "KF", s)
#         self.assertLessEqual(time, 60)
#         self.assertIn("LW", path)
#
#     def test8(self):
#         s = State()
#         s.set_age(1)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         s.item_update("Bow")
#         s.current_location = "KF"
#         p = PathFinder(s)
#         time, path = p.from_to("KF", "GC", s)
#         self.assertLessEqual(time, 200)
#         self.assertIn("HF", path)
#
#     def test9(self):
#         s = State()
#         s.set_age(1)
#         s.set_child_spawn("Graveyard")
#         s.set_adult_spawn("Temple of Time")
#         s.item_update("Bow")
#         s.item_update("Progressive Hookshot")
#         s.current_location = "Temple of Time"
#         p = PathFinder(s)
#         time, path = p.from_to(s.current_location, "DMC Lower", s)
#         self.assertLessEqual(time, 250)
#         self.assertGreater(time, 0)
#         self.assertIn("GC", path)
#
#
# class Optimization(unittest.TestCase):
#     def test1(self):
#         s = State()
#         s.set_age(0)
#         s.set_child_spawn("Market")
#         s.set_adult_spawn("Temple of Time")
#         s.current_location = "Bottom of the Well"
#         s.item_update("Bomb Bag")
#         p = PathFinder(s)
#         a = s.current_location
#         b = "ZR"
#         time_a = pc()
#         _, _ = p.from_to(a, b, s)
#         ETA = pc() - time_a
#         print(f"ETA from {a} to {b}: {ETA:.4f}")
#         self.assertLessEqual(ETA, 2)
#
#     def test2(self):
#         s = State()
#         s.set_age(0)
#         s.set_child_spawn("Market")
#         s.set_adult_spawn("Temple of Time")
#         s.current_location = "ZR"
#         s.item_update("Progressive Scale")
#         p = PathFinder(s)
#         a = s.current_location
#         b = "Bottom of the Well"
#         time_a = pc()
#         _, _ = p.from_to(a, b, s)
#         ETA = pc() - time_a
#         print(f"ETA from {a} to {b}: {ETA:.4f}")
#         self.assertLessEqual(ETA, 2)
#
#     def test3(self):
#         s = State()
#         s.set_age(1)
#         s.set_child_spawn("Market")
#         s.set_adult_spawn("Temple of Time")
#         s.current_location = "GTG"
#         s.item_update("Eponas Song")
#         s.item_update("Hover Boots")
#         s.item_update("Rutos Letter")
#         s.item_update("Rutos Letter")
#         s.item_update("Progressive Scale")
#         s.item_update("Bow")
#         s.item_update("Minuet of Forest")
#         s.item_update("Bolero of Fire")
#         s.item_update("Bomb Bag")
#         s.item_update("Requiem of Spirit")
#
#         p = PathFinder(s)
#         a = s.current_location
#         b = "Ice Cavern"
#         time_a = pc()
#         _, _ = p.from_to(a, b, s)
#         ETA = pc() - time_a
#         print(f"ETA from {a} to {b}: {ETA:.4f}")
#         self.assertLessEqual(ETA, 2)
