import pytest

from jmespath_filters import Filter


@pytest.mark.parametrize(
    'expression, error',
    [
        pytest.param('', "Expression must be a non-empty string or dictionary", id='empty-string'),
        pytest.param({}, "Expression must be a non-empty string or dictionary", id='empty-dict'),
        pytest.param(
            {'and': ['a', 'b']},
            "Rule dictionary may only contain one key for the following list: AND, OR, NOT. Found 'and'",
            id='unknown-key',
        ),
        pytest.param({'AND': ['', 'a']}, "Expression must be a non-empty string or dictionary", id='empty-and'),
    ],
)
def test_value_errors(expression, error, payload):
    with pytest.raises(ValueError, match=error):
        Filter(expression)
