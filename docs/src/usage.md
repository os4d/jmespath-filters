---
title: Getting started
---

# How to use jmespath-filters

## Installation

* Install jmespath-filters using your package manager of choice, e.g. Pip:
  ```shell
  pip install jmespath-filters
  ```

## Definitions

A Jmespath-filters Expression can be any of the following:
- A str containing a "Simple JMESpath statement".
- A dict with exactly one key which value can only be either `AND`, `OR`, or `NOT` and a value that can be:
  - A single Expression if the key is `NOT`
  - A list of 2 or more Expressions if the key is either `AND` or `OR`

NB: It is a nested structure can be defined based on other Expressions using `AND`, `OR`, or `NOT`

## Example usage

For the examples we will assume the following payload:

```json
{
  "people": [
    {
      "general": {"id": 100, "age": 20, "other": "foo", "name": "Bob"},
      "history": {"first_login": "2014-01-01", "last_login": "2014-12-02"}
    },
    {
      "general": {"id": 101, "age": 30, "other": "bar", "name": "Bill"},
      "history": {"first_login": "2014-05-01", "last_login": "2014-05-02"}
    }
  ]
}
```

Example of simple expression:
```python
"people[?general.id==`100`]"
```

Example of a NOT expression:
```python
{'NOT': "people[?general.id==`100`]"}
```

Example of an AND expression:
```python
{
    'AND': [
        "people[?general.id==`100`]",
        "people[?history.first_login==`2014-05-01`]",
    ]
}
```


Example of a composite expression (nested:
```python
{
    'AND': [
        "people[?history.last_login==`2014-12-02`]",
        {'NOT': "people[?general.age==`20`]"},
    ]
}
```