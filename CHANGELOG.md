# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.2.0] - 2023-09-05

### Added:
+ New basic property for type coercion `CoercibleProperty` and its subclasses
`FloatProperty` and `IntProperty` (#6).
+ Abstract Config property `source_dir`, which should return the path to the source (#1).\
**Note:** This does not mean the `src` directory, but rather the `src/custom_conf/` directory.
+ Use `pre-commit` for git hooks. (See [pre-commit](https://pre-commit.com)).

### Changed:
+ Allow type coercion for `BoundedProperty` subclasses.
+ Use typeguard for type validation in `Property` (#9).
+ Show different error messages based on whether a property was
  - queried before being set (i.e., `Config.initialized == False`),
  - or was never set (i.e., `Config.initialized == True`) (#3).
+ Raise an error, if a config file could not be read, instead of only logging an error (#2).

### Removed:
+ `NestedProperty` - functionality is now possible in `Property` (#9).

# [0.1.0] - 2023-08-23
Baseline version.
Custom_conf can be used by other Python projects.
The different properties allow for type and range checks,
which can also be expanded, if necessary.
The Config class can be used to read a config and store the values.
The values are stored as instance variables, which makes checking for usage
of a value in an IDE easy.

However, some code can be improved or can be removed.
