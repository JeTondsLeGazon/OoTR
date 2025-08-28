import json
from src.logic.utils import Requirement
from pydantic import BaseModel


with open("resources/zones_to_locations.json", "r") as f:
    zones_to_locations_table = json.load(f)


class ZoneToZoneInfo(BaseModel):
    from_zone: str
    to_zone: str
    time: int
    requirements: list[Requirement]


class ZonesToZonesInfo(BaseModel):
    zones_to_zones: list[ZoneToZoneInfo]


class ZoneToLocationsInfo(BaseModel):
    zone: str
    locations: list[str]


class ZonesToLocationsInfo(BaseModel):
    zones_to_locations: list[ZoneToLocationsInfo]


def get_zones_to_zones_info() -> ZonesToZonesInfo:
    with open("resources/zones_to_zones.json", "r") as f:
        data = json.load(f)
    # TODO: continue from here, requirement may not always be list of list but only list
    infos = [
        ZoneToZoneInfo(
            from_zone=from_zone,
            to_zone=to_zone,
            time=time,
            requirements=[
                Requirement.from_dict(requirement) for requirement in requirements
            ],
        )
        for from_zone, to_zone, time, requirements in data
    ]

    return ZonesToZonesInfo(zones_to_zones=infos)
