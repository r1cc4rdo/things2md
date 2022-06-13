wget https://github.com/thingsapi/things-cli/raw/master/tests/main.sqlite -O test.sqlite
things-cli -d test.sqlite -j --recursive all > test.json
python things2md.py -i test.json -o test --all
