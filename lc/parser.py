import json
map_id_slug = {}
map_id_title = {}
with open("allproblems.json") as f:
    data = json.load(f)
    for row in data:
        map_id_slug[ row["stat"]["frontend_question_id"] ] = row["stat"]["question__title_slug"]
        map_id_title[ row["stat"]["frontend_question_id"] ] = row["stat"]["question__title"]

# print(map_id_slug)
print(map_id_title)