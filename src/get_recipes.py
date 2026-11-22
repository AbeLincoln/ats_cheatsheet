import io
import re
import json
import numpy as np
import pandas as pd

# The wiki's Template:Goods_csv page as saved: the CSV is inside its <pre> block
with open('../data/Goods.csv', encoding='utf-8') as file:
    text = file.read()
if '</pre>' in text:
    text = text[text.index('id,displayName'):text.rindex('</pre>')]
goods = pd.read_csv(io.StringIO(text), quotechar='"')

# Goods no building makes or uses, left out of the cheatsheet: tutorial and glade event items, and Fertilizer from the Fluffbeak
SKIPPED_GOODS = {'Scrolls - tutorial', 'Sparkdew', 'Fertilizer', 'Fuel Rod', 'Fuel Core'}

# Goods Data
filt = re.compile(r'(\s*\[.+?\]\s*)|(\s*Ruins\s*)|(\s*\(.+?\)\s*)|(\s*T[0-9]\s*)')
columns = list(goods.columns[1:-1])
goods_data = {}
for i, name in enumerate(goods.loc[:, 'id']):
    good_name = filt.sub('', name).strip()
    if not '_Meta' in name and good_name not in SKIPPED_GOODS:
        goods_data[good_name] = {col: goods.loc[i, col] for col in columns}
        goods_data[good_name]['description'] = goods_data[good_name]['description'].splitlines()[0].strip()

# Recipe Data, from js/buildings.json (run buildings.py first), so both files have the same recipes
with open('../js/buildings.json', encoding='utf-8') as file:
    text = file.read()
buildings = json.loads(re.sub(r"\\([\\'])", r"\1", text[text.index("'") + 1:text.rindex("'")]))

# Ingredient Sets, in recipe slot order so the grid's slot colours match the recipes
good_ingredient_sets = {}
for building in buildings:
    for recipe in building['recipes']:
        good_name = recipe['product']['name']
        if 'ingredients' not in recipe or good_name not in goods_data:  # gathering, or a service
            continue
        isets = good_ingredient_sets.setdefault(good_name, [])
        for ingredients in recipe['ingredients']:
            iset = [ingredient['name'] for ingredient in ingredients]
            if iset not in isets:
                isets.append(iset)

    # Fishing Huts make their own bait from a Pack of Crops
    if 'bait' in building:
        bait_name = building['bait']['name'].split(']')[-1].strip()
        iset = [building['baitIngredient']['name'].split(']')[-1].strip()]
        isets = good_ingredient_sets.setdefault(bait_name, [])
        if iset not in isets:
            isets.append(iset)

# Reverse ingredient sets
reverse_sets = {}
for good in good_ingredient_sets:
    for ingredient_set in good_ingredient_sets[good]:
        for ingredient in ingredient_set:
            if ingredient not in reverse_sets:
                reverse_sets[ingredient] = []
            if good not in reverse_sets[ingredient]:
                reverse_sets[ingredient].append(good)

# Add Info
for good in goods_data:
    isets = good_ingredient_sets[good] if good in good_ingredient_sets else []
    goods_data[good]['ingredient_sets'] = isets
    goods_data[good]['reverse_set'] = [reverse_sets[good]] if good in reverse_sets else []
    # The wiki writes some icon names with spaces ("Icon_Resource_Fish 1"); its files use underscores
    goods_data[good]['icon_path'] = f'img/goods/{goods_data[good]["iconName"].replace(" ", "_")}.png'

# Pandas using numpy types, which json does not like
class CustomJSONizer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            val = super().encode(bool(obj))
        elif isinstance(obj, np.int64):
            val = super().encode(int(obj))
        else:
            val = super().default(obj)
        return val

# Escaped for a JS string: backslashes first, so JSON escapes like \" survive
text = '\'' + json.dumps(goods_data, cls=CustomJSONizer).replace('\\', '\\\\').replace("'", '\\\'') + '\''

with open('../js/goods.json', 'w') as file:
    file.write(f'goods_data = {text}')
