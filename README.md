# Things to Markdown

This repository contains code to dump a Things db into directories
and Markdown files. It relies on the awesome [things-cli](https://github.com/thingsapi/things-cli)
to collect the initial db snapshot.

This is not intended as a migration tool, I wrote it to give myself offline access to my database on Android.

### Known issues
* Most templates currently only have inactive code inside. Send a pull request! 😊
* No recurrent actions are captured anywhere nor present in the "Upcoming" list. We inherit the limitation from [things-cli](https://github.com/thingsapi/things-cli), which would need to be amended for support.
* Current version of code does less than it did in the [previous commit](https://github.com/r1cc4rdo/things2md/commit/013389f0c0b9c2709b4c0a91372c903fa11666fc) but hey, it's waaaay more elegant now!