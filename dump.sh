wget https://github.com/thingsapi/things-cli/raw/master/tests/main.sqlite -o test_things.sqlite
things-cli -d test_things.sqlite -j --recursive all > test_things.json
python convert.py --output test_vault test_things.json
