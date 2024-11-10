# Changelog

## v2.0.1 (2024-11-10)

#### Fixes

* update edge version scraper

## v2.0.0 (2024-02-17)

#### Fixes

* fix pulling wrong chrome version
* check the value not the key when checking for poppers

#### Refactorings

* BREAKING remove `as_header` arg from 'get_agent()`
* improve type annotation coverage

#### Others

* update default browser versions

## v1.3.1 (2023-11-16)

#### Fixes

* fix edge updater and no longer inform user when update fails to avoid confusion

#### Performance improvements

* add default browser versions

## v1.3.0 (2023-11-02)

#### New Features

* add get_header()

## v1.2.0 (2023-03-05)

#### New Features

* add option to return dict from get_agent()

#### Fixes

* fix vivaldi updater

#### Others

* test as_dict param for get_agent()

## v1.1.1 (2023-02-23)

#### Fixes

* update chrome updater

#### Others

* build v1.1.1
* update changelog
* update readme

## v1.1.0 (2023-02-16)

#### New Features

* implement version randomization into get_agent()
* add func to randomize version numbers

#### Others

* build v1.1.0
* update changelog

## v1.0.10 (2023-02-16)

#### Fixes

* update chrome version updater

#### Others

* build v1.0.10
* update changelog

## v1.0.9 (2023-02-14)

#### Fixes

* update firefox version updater
* fix dict key removal during iteration

#### Others

* build v1.0.9
* update changelog

## v1.0.8 (2023-02-13)

#### Fixes

* fix creating browserVersions.json with {} instead of "{}" lol

#### Others

* build v1.0.8
* update changelog

## v1.0.7 (2023-02-13)

#### Fixes

* fix error occuring when browserVersions.json doesn't exist
* remove unused import

#### Others

* build v1.0.7
* update changelog
* update changelog

## v1.0.6 (2023-02-13)

#### Others

* build v1.0.6
* update changelog

## v1.0.5 (2023-02-13)

#### Others

* build v1.0.5
* update changelog

## v1.0.4 (2023-02-13)

#### Fixes

* wrap update_all() in try/except

#### Others

* build v1.0.4
* update changelog
* add browserVersions.json to .gitignore
