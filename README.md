# Things to Markdown

This repository contains code to export/dump a Things db into directories and Markdown files.
It relies on the awesome [things-cli](https://github.com/thingsapi/things-cli) to collect the
initial db snapshot.

For displaying results I recommend [Obsidian](https://obsidian.md/), an unfortunately closed-source
but  otherwise free and freedom-respecting markdown editor/manager. This tool is designed to use the following skin/plugins:
* [Things skin](https://github.com/colineckert/obsidian-things) by [Colin Eckert](https://github.com/colineckert),
* [Breadcrumbs plugin](https://github.com/SkepticMystic/breadcrumbs) by [SkepticMystic](https://github.com/SkepticMystic): to provide navigation between lists,
* [Creases plugin](https://github.com/liamcain/obsidian-creases) by [Liam Cain](https://github.com/liamcain): to programmatically fold lists. See also [this unanswered post](https://forum.obsidian.md/t/where-are-the-collapsed-folded-states-of-lists-and-headings-stored/38614).

### Known issues
* Most templates currently only have inactive code inside. Send a pull request! 😊
* No recurrent actions are captured anywhere nor present in the "Upcoming" list. We inherit the limitation from [things-cli](https://github.com/thingsapi/things-cli), which would need to be amended for support.
* Current version of code does less than it did in a [previous commit](https://github.com/r1cc4rdo/things2md/tree/013389f0c0b9c2709b4c0a91372c903fa11666fc) but hey, it's waaaay more elegant now!

### Links for developers
* [SimpleTemplate engine](https://bottlepy.org/docs/dev/stpl.html#bottle.SimpleTemplate) documentation, from the [Bottle](https://bottlepy.org/) project.

### Links for Things
* [things-cli](https://github.com/thingsapi/things-cli): Python 3 CLI to read Things app data.
* [things.py](https://github.com/thingsapi/things.py/): Python 3 library to read data from Things app.
* [Things](https://culturedcode.com/things/): award-winning personal task manager, from [Cultured Code](https://culturedcode.com/).

### Links for Obsidian
* [Obsidian](https://obsidian.md/): markdown-based knowledge-base manager.
* [Things skin](https://github.com/colineckert/obsidian-things) for [Obsidian](https://obsidian.md/), by [Colin Eckert](https://github.com/colineckert)
* [Creases plugin](https://github.com/liamcain/obsidian-creases): to programmatically fold lists. See also [this unanswered post](https://forum.obsidian.md/t/where-are-the-collapsed-folded-states-of-lists-and-headings-stored/38614).
* [Breadcrumbs plugin](https://github.com/SkepticMystic/breadcrumbs): to provide navigation between lists
