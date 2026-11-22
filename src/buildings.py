import re
import json
from pathlib import Path

# The wiki's building data files (see the README), one per building type
DATA_FILES = ["Workshops", "Farms", "Institutions", "RainCatchers", "Extractors", "Camps", "FishingHuts", "GathererHuts", "Mines", "Blight Posts"]
SKIPPED = {"Field Engineering Station"}  # only built during a glade event

# The wiki's specialization tags, by the names the game shows
PROFICIENCY_TAGS = {"Alchemy": "Alchemy", "Farming": "Farming", "Metallurgy": "Metallurgy", "Stone": "Masonry", "Animals": "Meat production", "Wood": "Woodworking"}
COMFORT_TAGS = {"Brewing": "Brewing", "FoxesCooperation": "Cooperation", "Tech": "Engineering", "Rainwater": "Rainwater", "Cloth": "Tailoring", "Warmth": "Warmth"}

workshops = []
for name in DATA_FILES:
    with open(f"../data/{name}.json", encoding="utf-8") as file:
        workshops += [building for building in json.load(file) if building["id"] not in SKIPPED]

for workshop in workshops:
    workshop["icon"] = f"img/buildings/{workshop['id'].replace(' ', '_')}_icon.png"
    tags = workshop.pop("tags", [])
    unknown = [tag for tag in tags if tag not in PROFICIENCY_TAGS and tag not in COMFORT_TAGS]
    if unknown:
        raise SystemExit(f"{workshop['id']}: unknown specialization tags {unknown}, add them to PROFICIENCY_TAGS or COMFORT_TAGS")
    workshop["proficiencyTags"] = [PROFICIENCY_TAGS[tag] for tag in tags if tag in PROFICIENCY_TAGS]
    workshop["comfortTags"] = [COMFORT_TAGS[tag] for tag in tags if tag in COMFORT_TAGS]
    del workshop["description"]
    for recipe in workshop["recipes"]:
        if "ingredients" in recipe:
            for ingredient_group in recipe["ingredients"]:
                for ingredient in ingredient_group:
                    ingredient["name"] = ingredient["name"].split("]")[-1].strip()
        if "product" in recipe:
            recipe["product"]["name"] = recipe["product"]["name"].split("]")[-1].strip()
        elif "servedNeed" in recipe:
            recipe["product"] = {"name": recipe["servedNeed"].strip()}
        elif "seekedResource" in recipe:
            recipe["product"] = {"name": recipe["seekedResource"].split("]")[-1].strip()}
        elif "seekedDeposits" in recipe:
            recipe["product"] = {"name": recipe["seekedDeposits"].split("]")[-1].strip(), "grade": recipe["grade"]}

        if "grade" in recipe:
            match recipe["grade"]:
                case "Grade0":
                    recipe["grade"] = "☆"
                case "Grade1":
                    recipe["grade"] = "★"
                case "Grade2":
                    recipe["grade"] = "★★"
                case "Grade3":
                    recipe["grade"] = "★★★"
                case grade if grade.endswith("- institution"):
                    recipe["grade"] = ""  # services have no star rating
        else:
            recipe["grade"] = ""
    
    for good in workshop["requiredGoods"]:
        good["name"] = good["name"].split("]")[-1].strip()

# Escaped for a JS string: backslashes first, so JSON escapes like \" survive
text = '\'' + json.dumps(workshops).replace('\\', '\\\\').replace("'", '\\\'') + '\''

with open('../js/buildings.json', 'w') as file:
    file.write(f'buildings_data = {text}')
