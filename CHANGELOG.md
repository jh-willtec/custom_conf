# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added:
+ New basic property for type coercion `CoercibleProperty` and its subclasses `FloatProperty` and `IntProperty`

### Changed:
+ Allow type coercion for `BoundedProperty` subclasses


# [0.1.0] - 2023-08-23
Baseline version.
Custom_conf can be used by other Python projects.
The different properties allow for type and range checks, 
which can also be expanded, if necessary.
The Config class can be used to read a config and store the values.
The values are stored as instance variables, which makes checking for usage 
of a value in an IDE easy.

However, some code can be improved or can be removed.
