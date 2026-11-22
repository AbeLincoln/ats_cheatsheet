# Against the Storm Cheatsheet

[live website](https://frankruis.github.io/ats_cheatsheet/)

![Screenshot](/img/example_screenshot.png)

A simple local interactive web app for against the storm, where you can see which resources require which ingredients to make, or which resources are used in which recipes, as well as all the (shared) needs for the species of your current game.

Game data: **1.11.5**, updated November 2026. Interface selections are saved in the browser and restored on the next visit.

Works locally in your web browser without any setup, just click the green `code` button at the top right of the repository and choose download as zip, unzip, and open `index.html`.
If you download the files I'm currently pulling from CDNs in the `index.html` header and update it to point at the local version it should also work offline.

## Ingredient Grid
- Click on any resource to see which ingredients are needed to make it.
- Alternatively, enable the switch in the top right (before clicking) to see which other resources can be made with the selected ingredient.
- The colors indicate sets of ingredients, where you can pick one ingredient per set for the recipe (e.g., in the screenshot above, you can make pickled goods with roots and pottery).
- The selected ingredient will filter the buildings table on buildings that can produce that ingredient.

## Species Needs
- Click on any of the species to enable them, click again to disable, select up to 4 species at a time (4 requires the Sacred Grove World Map modifier).
- Colored rings around the needs and species indicate which species require which needs.
- Needs with multiple colors are shared by multiple selected species.

See also the needs info tab to see a reverse mapping of overlapping species for each need.

## Buildings
- The buildings table contains all buildings that can produce items, and can be filtered on their category (as defined by the official wiki data) by clicking the buttons above the table.
- Clicking an ingredient will filter the table on buildings that produce that ingredient.
- Once filtered by ingredient you can also choose to enable the costs option, which will also show buildings that require the selected ingredient to build. Deselecting the products option will only show the buildings with the given ingredient as a cost.

## Contribution
The code is quite ugly since I just wanted to quickly make something usable without any server-side requirements, but I included everything I used such as the Python scripts to parse the CSV files with recipe data and download the icons from the official wiki.

- I collected the CSV files from the [official wiki template listing](https://hoodedhorse.com/wiki/Against_the_Storm/Special:AllPages?from=&to=&namespace=10) (all templates with `csv` in their name).
	- Update: some CSV files are now outdated, more recent data seems to be available in the json files referenced in the [Module namespace](https://hoodedhorse.com/wiki/Against_the_Storm/Special:AllPages?from=&to=&namespace=828) on the Wiki.
- The styling and images are all ripped from the official wiki as well.

### Updating the game data
`js/buildings.json` and `js/goods.json` are generated from the wiki's data pages, which come from the game developers. Don't edit them by hand: the next update would overwrite the change.

1. Save each page below into `data/` under the name shown (open the link, then save the page; the `?action=raw` pages are the plain file).

	| Save as | Wiki page |
	|---|---|
	| `Workshops.json` | [Module:WorkshopsData/Workshops.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:WorkshopsData/Workshops.json?action=raw) |
	| `Farms.json` | [Module:FarmsData/Farms.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:FarmsData/Farms.json?action=raw) |
	| `Institutions.json` | [Module:InstitutionsData/Institutions.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:InstitutionsData/Institutions.json?action=raw) |
	| `Camps.json` | [Module:CampsData/Camps.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:CampsData/Camps.json?action=raw) |
	| `GathererHuts.json` | [Module:GatheringData/GathererHuts.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:GatheringData/GathererHuts.json?action=raw) |
	| `FishingHuts.json` | [Module:FishingData/FishingHuts.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:FishingData/FishingHuts.json?action=raw) |
	| `RainCatchers.json` | [Module:RainCollectorsData/RainCatchers.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:RainCollectorsData/RainCatchers.json?action=raw) |
	| `Extractors.json` | [Module:ExtractorsData/Extractors.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:ExtractorsData/Extractors.json?action=raw) |
	| `Mines.json` | [Module:MinesData/Mines.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:MinesData/Mines.json?action=raw) |
	| `Blight Posts.json` | [Module:BlightPostsData/Blight Posts.json](https://wiki.hoodedhorse.com/Against_the_Storm/Module:BlightPostsData/Blight%20Posts.json?action=raw) |
	| `Goods.csv` | [Template:Goods_csv](https://wiki.hoodedhorse.com/Against_the_Storm/Template:Goods_csv?action=raw) (saved as is; the script reads the CSV out of the page) |

2. From `src/`, run `py buildings.py`, then `py get_recipes.py` (needs pandas and numpy). `get_recipes.py` reads the recipes from the new `js/buildings.json`.
3. Review the diff. `buildings.py` stops if the wiki adds a specialization tag it doesn't know; add it to `PROFICIENCY_TAGS` or `COMFORT_TAGS`. A new good shows up in the Ingredient Grid: leave it out with `SKIPPED_GOODS` in `get_recipes.py` if no building makes or uses it, or add its icon to `img/goods/`. A new building needs its icon in `img/buildings/`, named after its ID.
- I already downloaded the images for cornerstones, with the intention to also highlight relevant cornerstones in the future.
- I will likely add a list of buildings too, similar to [the recipe list on the wiki](https://hoodedhorse.com/wiki/Against_the_Storm/Copper_Bars#Product).
