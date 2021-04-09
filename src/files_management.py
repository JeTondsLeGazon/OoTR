"""
This file extracts the information from the spoiler logs via the extract_logs
function.

"""

import json
import os
import logging
from mylog import logger

def list_files(path):
    """
    Returns a sorted list of json files in path.
    
    path (str): path to the spoiler log files
    """
    return list(sorted([f for f in os.listdir(path=path) if
                          f.endswith('.json')]))


def extract_json(path, json_files):
    """
    Loads json dict from many json files
    
    path (str): path to json files
    json_files (list(str)): json files to extract in the path
    """
    extracted_dicts = []
    for json_file in json_files:
        with open(os.path.join(path, json_file)) as f:
            extracted_dicts.append(json.load(f))
    return extracted_dicts


def extract_locations(spoiler_logs):
    """
    Extracts the locations from the spoiler logs dicts and checks whether
    the json files are spoiler logs.
    
    spoiler_logs (list(dict)): list of extracted json dicts
    """
    locations = []
    
    for log in spoiler_logs:  # loop to check the spoiler log with try-except
        try:
            locations.append(log['locations'])
        except KeyError:
            print("Invalid spoiler log ...")
    return locations


def extract_age(spoiler_logs):
    """
    Extracts the starting age from the spoiler logs dicts.
    
    spoiler_logs (list(dict)): list of extracted json dicts
    """
    return [0 if log["randomized_settings"]['starting_age'] == "child" else 1 for log in spoiler_logs]


def extract_spawn(spoiler_logs, ages):
    """
    Extracts the starting spawns from the spoiler logs dicts.
    
    spoiler_logs (list(dict)): list of extracted json dicts
    """
    spawns = [[log['entrances']["Child Spawn -> KF Links House"], 
               log['entrances']["Adult Spawn -> Temple of Time"]] for log in spoiler_logs]
    
    return [[xx['region'] if isinstance(xx, dict) else xx for xx in x] for x in spawns]


def extract_logs(path, n=1000, from_=0, to=1000):
    """
    Extracts items location from n spoiler log files and return list of dict.
    
    path (str): path to the spoiler log files
    n (int): maximum number of files to extract
    Returns: list of dict
    """
    assert from_ < to, 'from_ must be smaller than to'
    json_files = list_files(path=path)
    nb_files = n if n <= len(json_files) else len(json_files)
    json_files = json_files[:nb_files]
    
    spoiler_logs = extract_json(path, json_files)
    
    locations = extract_locations(spoiler_logs)
    starting_age = extract_age(spoiler_logs)
    starting_spawn = extract_spawn(spoiler_logs, starting_age)
    no_logs = [f.split('-')[-1].split('_Spoiler')[0] for f in json_files]
    logger.info(f"Successfully extracted locations from {len(locations)} files")
    return locations[from_:to], starting_age[from_:to], starting_spawn[from_:to], no_logs[from_:to]