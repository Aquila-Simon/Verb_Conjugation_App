import csv

verbs = []
skipped_count = 0
recorded_verbs = set()


def load_verbs():
    verbs = []
    skipped_count = 0
    recorded_verbs = set()

    with open("verbs.csv", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            if not row:
                print("This row is empty or does not contain enough data.")
                skipped_count += 1
                continue
            elif len(row) < 2:
                print(f"This row does not contain enough data: {row}")
                skipped_count += 1
                continue

            verb = row[0]
            verb_type = row[1]

            verb = verb.strip()
            verb_type = verb_type.strip().lower()

            if verb == "" or verb_type == "":
                print(f"This row contains empty fields: {row}")
                skipped_count += 1
                continue

            if verb_type not in ["ichidan", "godan", "irregular"]:
                print(
                    f"Unknown verb type '{verb_type}' for verb '{verb}'. Skipping this row."
                )
                skipped_count += 1
                continue

            if verb not in recorded_verbs:
                verbs.append((verb, verb_type))
            else:
                print(f"Duplicate verb '{verb}' found. Skipping this row.")
                skipped_count += 1
                continue

            recorded_verbs.add(verb)

    return verbs, skipped_count
