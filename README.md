# dragalia-data-parse

[![Parser-ci]][Parser-ci-link]
[![Parser-cq-badge]][Parser-cq-link]
[![Parser-coverage-badge]][Parser-coverage-link]
[![Parser-lgtm-alert-badge]][Parser-lgtm-alert-link]
[![Parser-lgtm-quality-badge]][Parser-lgtm-quality-link]
[![Parser-time-badge]][Parser-time-link]

This parses the original Dragalia Lost assets to be the file usable for [DL info website][DL-info].

Developed under Python 3.9 (or higher).

[DL-info]: https://dl.raenonx.cc

[Parser-ci]: https://github.com/RaenonX-DL/dragalia-data-parse/workflows/CI/badge.svg
[Parser-ci-link]: https://github.com/RaenonX-DL/dragalia-data-parse/actions?query=workflow%3ACI
[Parser-coverage-badge]: https://app.codacy.com/project/badge/Coverage/0053d85597a740c393a6bfd007e4033b
[Parser-coverage-link]: https://www.codacy.com/gh/RaenonX-DL/dragalia-data-parse/dashboard
[Parser-cq-badge]: https://app.codacy.com/project/badge/Grade/0053d85597a740c393a6bfd007e4033b
[Parser-cq-link]: https://www.codacy.com/gh/RaenonX-DL/dragalia-data-parse/dashboard
[Parser-time-badge]: https://wakatime.com/badge/github/RaenonX-DL/dragalia-data-parse.svg
[Parser-time-link]: https://wakatime.com/badge/github/RaenonX-DL/dragalia-data-parse
[Parser-lgtm-alert-badge]: https://img.shields.io/lgtm/alerts/g/RaenonX-DL/dragalia-data-parse.svg?logo=lgtm&logoWidth=18
[Parser-lgtm-alert-link]: https://lgtm.com/projects/g/RaenonX-DL/dragalia-data-parse/alerts/
[Parser-lgtm-quality-badge]: https://img.shields.io/lgtm/grade/python/g/RaenonX-DL/dragalia-data-parse.svg?logo=lgtm&logoWidth=18
[Parser-lgtm-quality-link]: https://lgtm.com/projects/g/RaenonX-DL/dragalia-data-parse/context:python

------

# Prerequisites

- Install Python 3.9 or higher.

- **No dependencies required for now (2021/01/22).**

    - If you want to develop this instead, run the below for installing the development dependencies.

      ```bash
      pip install -r requirements-dev.txt
      ```

- Get all the data from the [data depot][data-depot].

    - This will be done by using `git submodule`.

      Initialize the submodule:

      ```bash
      git submodule init
      ```

      Update (download) the content of the submodule:

      ```bash
      git submoule update --remote
      ```

    - To update the data, simply run the `git submodule update` command:

      ```bash
      git submoule update --remote
      ```

[data-depot]: https://github.com/RaenonX-DL/dragalia-data-depot

------

# Usage

Currently, there are *no* interactional scripts or CLI exists.

Instead, there are some express scripts. To configure them, directly modify the paramters inside.

> These express scripts will be named as `script_*` where `*` will be the purpose of that script.

### `script_chara_overview`

Get a quick overview of a certain character by specifying the character ID. Character ID should be an 8-digit number.

### `script_check_skill`

Check if the newly added skills are all parsed.

### `script_data_diff`

Check the data difference between different versions of the assets.

One asset will be the local version, and another will be one of the [remote][data-depot] versions.

### `script_export_local`

Export things (currently skills, and some enum texts) to a specific location.

Note that this is intended to export things for non-pipelining purposes, such as data viewing or correcting. For the
pipelined data exporting, use `script_export_pipeline` instead.

### `script_export_pipeline`

Export resources for the use of the [DL info website][DL-info].

For exporting things locally for viewing or other non-pipelining purposes, use `script_export_local` instead.

### `script_view_hit_attr`

View the data of all given hit attributes.

------

# Credits

### Main Developer

- **\[OM\] [RaenonX][GH-raenonx]**

### Correctness double-check

- **\[OM\] Andy / Toasty**

- \[OM\] Huang

- \[OM\] Kevin Tu

- \[OM\] Leo

- **\[OM\] Spark / AAAAA**

- \[OM\] Yorkwarm

### Data inspection

- \[SimCord\] Anastasia

- **\[SimCord\] [Mushymato / Chu][GH-mushymato]**

- **\[OM\] [RaenonX][GH-raenonx]**

- **\[OM\] [Ryo][GH-ryo]**

- **\[OM\] Spark / AAAAA**

- \[SimCord\] ThatOneGuy

### Datamining and data deploying pipeline

- \[SimCord\] qwewqa / Mustard Yellow

- \[SimCord\] eave

- **\[OM\] [Ryo][GH-ryo]**

### Miscellaneous discussions

- \[OM\] Siena

Also thanks to everyone who had contributed to [Gamepedia].

[GH-mushymato]: https://github.com/Mushymato

[GH-raenonx]: https://github.com/RaenonX

[GH-ryo]: https://github.com/ryoliao

------

# Notes

Some skill data in the tests is different from what is on [Gamepedia][Gamepedia].

[Gamepedia]: https://dragalialost.wiki/w/

### Development Goals

- This parser aims to parse **all** game assets correctly and automatically.

  > Doing so gives the ability to automate the game data deploying process,
  > reducing unnecessary works for every new updates.

- As few dependencies as possible to run the parser.

  > Doing so reduces the difficulty to deploy the data processing pipeline,
  > since native Python packages seldom have cross-platform problems.
  >
  > This assumes that additional dependencies do not significantly boost the data processing speed
  > or impact the security, which rarely happens in general.

For some asset notes or explanations, try visiting the [notes] section. Note that these documents may be incomplete or
inaccurate.

[notes]: https://github.com/RaenonX-DL/dragalia-data-parse/tree/main/notes

------

# Milestones

- `2020/11/18 AM 11:01 CST`: Project started.

- `2020/11/19 PM 07:04 CST`: First commit of the project ([v0.1]).

- `2020/12/14 AM 06:09 CST`: Completed attacking skills parsing ([v1.0]).

  > This excludes Gala Laxi S2. Also, debuffs are not yet confirmed at this point.

- `2020/12/22 PM 08:31 CST`: Completed parsed data exporting ([v1.1]).

- `2021/01/22 AM 10:58 CST`: Completed EX ability/Co-ability parsing ([v1.2]).

- `2021/01/23 PM 06:17 CST`: Completed chained EX ability/Co-ability (CCA) parsing ([v1.3]).

- `2021/01/24 PM 11:57 CST`: Completed chained EX ability/Co-ability (CCA) exporting ([v1.4]).

[v0.1]: https://github.com/RaenonX-DL/dragalia-data-parse/releases/tag/v0.1

[v1.0]: https://github.com/RaenonX-DL/dragalia-data-parse/releases/tag/v1.0

[v1.1]: https://github.com/RaenonX-DL/dragalia-data-parse/releases/tag/v1.1

[v1.2]: https://github.com/RaenonX-DL/dragalia-data-parse/releases/tag/v1.2

[v1.3]: https://github.com/RaenonX-DL/dragalia-data-parse/releases/tag/v1.3

[v1.4]: https://github.com/RaenonX-DL/dragalia-data-parse/releases/tag/v1.4
