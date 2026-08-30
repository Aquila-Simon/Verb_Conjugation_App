import requests, json
from pathlib import Path

# word = input("Please input a Japanese word: ")

url = "https://jisho.org/api/v1/search/words"
params = {"keyword": "#jlpt-n5 #verb"}

response = requests.get(url, params=params)

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
        is_verb = False
        verb_sense = None
        verb_part = None
        for sense in entry["senses"]:
            for part in sense["parts_of_speech"]:
                if "verb" in part.lower():
                    is_verb = True
                    verb_sense = sense
                    verb_part = part
                    break
            if is_verb:
                break

        word = "NA"
        reading = "NA"
        meaning = "NA"
        jlpt = "NA"
        verb_type = "NA"
        part_of_speech = "NA"

        if is_verb:
            if entry["slug"]:
                word = entry["slug"]
            else:
                word = "Not Available"

            if entry["japanese"]:
                if entry["japanese"][0]["reading"]:
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

            if "ichidan" in verb_part.lower():
                verb_type = "ichidan"
            elif "godan" in verb_part.lower():
                verb_type = "godan"
            elif "suru" in verb_part.lower() or "kuru" in verb_part.lower():
                verb_type = "irregular"
            else:
                verb_type = "Unknown Verb Type"

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
    print("Word:", verb["word"])
    print("Reading:", verb["reading"])
    print("Meaning:", verb["meaning"])
    print("JLPT:", verb["jlpt"])
    print("Verb Type:", verb["verb_type"])
    print("Part of Speech:", verb["part_of_speech"])
    print()
