from csv import DictReader

import json


def csv_to_json(csv_path, json_path, model):
    json_array = []

    with open(csv_path, encoding='utf-8') as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
            del row["id"]
            if "price" in row:
                row["price"] = int(row["price"])

            if "is_published" in row:
                if row["is_published"] == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            if "location_id" in row:
                row["location_id"] = [int(row["location_id"])]

            json_array.append({"model": model, "fields": row})

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_string = json.dumps(json_array, ensure_ascii=False)
        json_file.write(json_string)


csv_to_json('data/ad.csv', 'data/ad.json', 'ads.ad')
csv_to_json('data/category.csv', 'data/category.json', 'ads.category')
csv_to_json('data/location.csv', 'data/location.json', 'users.location')
csv_to_json('data/user.csv', 'data/user.json', 'users.user')
