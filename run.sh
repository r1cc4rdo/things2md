things-cli -j --recursive all > things.json
python things2md.py -i things.json -o things
