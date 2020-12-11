# dragalia-data-parse

[![time tracker](https://wakatime.com/badge/github/RaenonX-DL/dragalia-data-parse.svg)](https://wakatime.com/badge/github/RaenonX-DL/dragalia-data-parse)

------

This parses the original Dragalia Lost assets to be the file usable for [DL info website][DL-info].

Developed under Python 3.9.

[DL-info]: http://dl.raenonx.cc

[RaenonX-DL]: https://github.com/RaenonX-DL

------

# Prerequisites

- Install Python 3.9.

- **No dependencies required for now (2020/12/07).**

    - If you want to develop this instead, run the below for installing the development dependencies.

      ```commandline
      pip install -r requirements-dev.txt
      ```

- Get all the data from the [data depot][data-depot], and place it inside `.data/media`.

    - You should have a valid path like this: `.data/media/assets`.

[data-depot]: https://github.com/RaenonX-DL/dragalia-data-depot

------

# Usage

Currently, there are *no* interactional scripts or CLI exists.

Instead, there are some express scripts. To use them, directly modify the paramters inside.

> These express scripts will be named as `script_*` where `*` will be the purpose of that script.

### `script_chara_overview`

Get a quick overview of a certain character by specifying the character ID. Character ID should be an 8-digit number.

### `script_data_diff`

Check the data difference between different versions of the assets.

One asset will be the local version, and another will be one of the [remote][data-depot] versions.

### `script_export`

Export all skill data as csv to the specified location.

------

# Credits

### Main Developer

- \[OM\] [RaenonX][GH-raenonx]

### Correctness double-check

- \[OM\] Andy / Toasty

- \[OM\] Huang

- \[OM\] Kevin Tu

- \[OM\] Leo

- \[OM\] Spark / AAAAA

- \[OM\] Yorkwarm

### Data inspection

- \[SimCord\] Anastasia

- \[SimCord\] [Mushymato / Chu][GH-mushymato]

- \[OM\] [RaenonX][GH-raenonx]

- \[OM\] [Ryo][GH-ryo]

- \[OM\] Spark / AAAAA

- \[SimCord\] ThatOneGuy

### Datamining and data deploying pipeline

- \[OM\] [Ryo][GH-ryo]

### Miscellaneous discussions

- \[OM\] Siena

[GH-mushymato]: https://github.com/Mushymato

[GH-raenonx]: https://github.com/RaenonX

[GH-ryo]: https://github.com/ryoliao

------

# Notes

Most of the sample skill data for correctness checking will locate at `test_transformer/test_skill`.

Some skill data will be different from what is on [Gamepedia][Gamepedia]. This is most likely due to some human reading
errors or outdated information because of the v2.0 update.

[Gamepedia]: https://dragalialost.gamepedia.com/

### Development Goals

- This parser aims to parse **all** game assets correctly and automatically.

  > Doing so gives the ability to automate the game data deploying process,
  > reducing unnecessary works for every new updates.

- As few dependencies as possible to run the parser.

  > Doing so reduces the difficulty to deploy the data processing pipeline,
  > since Python native packages only has a few calls which results will differ across different platforms.
  >
  > This assumes that any possible additional dependency will not significantly boost the data processing speed
  > (if necessary), which rarely happens in general.

If you are looking for some asset notes or explanations, try visiting the [notes] section. Note that the notes may be
incomplete.

[notes]: https://github.com/RaenonX-DL/dragalia-data-parse/tree/main/notes

------

# Milestones

- `2020/11/18 AM 11:01 CST`: Project started.

- `2020/11/19 PM 07:04 CST`: First commit of the project (1b2c776).
