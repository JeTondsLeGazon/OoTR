from dataclasses import dataclass


@dataclass
class Item:
    name: str
    max_progression: int
    current_progression: int

    def update_progression(self) -> None:
        if self.current_progression >= self.max_progression:
            raise ValueError(f"{self.name} is already at max progression.")
        self.current_progression += 1


class State:
    """
    Represents the state of the player in the game, including its items and their potential upgrades.
    """

    def __init__(
        self,
        items_pool: list[tuple[str, int, int]],
    ):
        self.items = {
            name: Item(name, max_progression, current_progression)
            for name, max_progression, current_progression in items_pool
        }
        self.current_location = None
        self._is_adult = None
        self.child_spawn_location: str | None = None
        self.adult_spawn_location: str | None = None

    @property
    def is_adult(self) -> bool:
        if self._is_adult is None:
            raise ValueError("Age has not been set. Use set_age() to set the age.")
        return self._is_adult

    def item_update(self, item_name: str) -> None:
        item = self.items.get(item_name)
        if not item:
            raise ValueError(f"Item {item_name} not found in items pool.")
        item.update_progression()

    def change_age(self) -> None:
        self._is_adult = not self._is_adult

    def set_age(self, age: int) -> None:
        self._is_adult = bool(age)

    def set_initial_items(self, locations):
        self.item_update(locations["starting_items"])

    def can_beat_ganon(self):
        return (
            self.current_number_medallions() == 6
            and self.items["Light Arrow"].current_progression >= 1
        )

    def current_number_medallions(self):
        return sum(
            self.items[item_name].current_progression
            for item_name in self.items
            if "Medallion" in item_name
        )
