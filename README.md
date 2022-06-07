# Things to Markdown

This repository contains code to dump a Things db into directories
and Markdown files. It relies on the awesome [things-cli](https://github.com/thingsapi/things-cli)
to collect the initial db snapshot.

This is not intended as a migration tool, I wrote it to give myself offline access to my database on Android.

### Known issues
* "Anytime" and "Someday" section unimplemented, for no other reason that it's 3am and want to commit.
Send a pull request! 😊
* No recurrent actions are captured anywhere nor present in the "Upcoming" list. This might be because I generated my
dump without the recursive option (**TODO**: verify) or because not outputted in the first place by [things-cli](https://github.com/thingsapi/things-cli).
* Code is admittedly ugly and in need of refactoring and TLC. Send a pull request! 😊