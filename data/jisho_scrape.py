import json
from pathlib import Path

import requests

# word = input("Please input a Japanese word: ")

url = "https://jisho.org/api/v1/search/words"
params = {"keyword": "#jlpt-n5 #verb"}

try:
    response = requests.get(url, params=params, timeout=10)
except requests.RequestException as error:
    print("Request to Jisho failed")
    print(f"Error: {error}")
    exit()


if response.status_code != 200:
    print("Jisho request fail:", response.status_code)
    exit()

data = response.json()

MAIN_DIR = Path(__file__).resolve().parent
DICT_DATA = MAIN_DIR / "jisho_dict.json"
print(DICT_DATA)
dict_of_data = []


def write_to_dict():
    with open(DICT_DATA, "w", encoding="utf-8") as file:
        json.dump(dict_of_data, file, ensure_ascii=False, indent=4)


def read_from_dict():
    global dict_of_data
    with open(DICT_DATA, "r", encoding="utf-8") as file:
        dict_of_data = json.load(file)


# Checks if data points are empty
if data["data"]:
    for entry in data["data"]:
        verb_sense = None
        verb_part = None
        verb_type = None
        for sense in entry["senses"]:
            for part in sense["parts_of_speech"]:
                if "ichidan" in part.lower():
                    verb_type = "ichidan"
                    verb_sense = sense
                    verb_part = part
                elif "godan" in part.lower():
                    verb_type = "godan"
                    verb_sense = sense
                    verb_part = part
                elif "suru" in part.lower() or "kuru" in part.lower():
                    verb_type = "irregular"
                    verb_sense = sense
                    verb_part = part

                if verb_type is not None:
                    break
            if verb_type is not None:
                break

        word = "NA"
        reading = "NA"
        meaning = "NA"
        jlpt = "NA"
        part_of_speech = "NA"

        if verb_type is not None:
            if entry["slug"]:
                if verb_part == "Suru verb":
                    if entry["slug"].endswith("する"):
                        word = entry["slug"]
                    else:
                        word = entry["slug"] + "する"
                else:
                    word = entry["slug"]
            else:
                word = "Not Available"

            if entry["japanese"]:
                if entry["japanese"][0]["reading"]:
                    if verb_part == "Suru verb":
                        if entry["japanese"][0]["reading"].endswith("する"):
                            reading = entry["japanese"][0]["reading"]
                        else:
                            reading = entry["japanese"][0]["reading"] + "する"
                    else:
                        reading = entry["japanese"][0]["reading"]
                else:
                    reading = "Not Available"
            else:
                reading = "Not Available"

            if verb_sense["english_definitions"]:
                meaning = verb_sense["english_definitions"][0]
            else:
                meaning = "Not Available"

            part_of_speech = verb_part

            if entry["jlpt"]:
                jlpt = entry["jlpt"][0]
            else:
                jlpt = "Not Available"

            verb_data = {
                "word": word,
                "reading": reading,
                "meaning": meaning,
                "jlpt": jlpt,
                "verb_type": verb_type,
                "part_of_speech": part_of_speech,
            }
            dict_of_data.append(verb_data)
else:
    entry = "Data not Available"
    verb_data = {
        "word": "Data not Available",
        "reading": "Data not Available",
        "meaning": "Data not Available",
        "jlpt": "Data not Available",
        "verb_type": "Data not Available",
        "part_of_speech": "Data not Available",
    }
    dict_of_data.append(verb_data)

write_to_dict()


for verb in dict_of_data:
    print(f"Word: {verb['word']}")
    print(f"Reading: {verb['reading']}")
    print(f"Meaning: {verb['meaning']}")
    print(f"JLPT Level: {verb['jlpt']}")
    print(f"Verb Type: {verb['verb_type']}")
    print(f"Part of Speech: {verb['part_of_speech']}")
    print()
