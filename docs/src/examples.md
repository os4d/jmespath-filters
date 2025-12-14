---
title: Examples
---

# Examples

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

A Jmespath-filters Expression can be any of the following:
- An str containing a "Simple Json statement"