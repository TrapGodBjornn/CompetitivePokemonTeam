import json

with open("OU.json", "r", encoding = "UTF-8") as f:
    dataa = json.load(f)


fuck = dataa["cinderace"]

#print(araquanidsshit)

print(json.dumps(fuck, indent=2))

    