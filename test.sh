wget https://github.com/thingsapi/things-cli/raw/master/tests/main.sqlite -O test.sqlite
things-cli -d test.sqlite -j --recursive all > test.json
python things2md.py -i test.json -o test --all

wget https://github.com/bboc/things3-export/raw/master/test-data/Things-testdb.sqlite -O test2.sqlite
things-cli -d test2.sqlite -j --recursive all > test2.json
python things2md.py -i test2.json -o test2 --all
