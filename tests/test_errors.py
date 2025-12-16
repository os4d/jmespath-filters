from contextlib import nullcontext as does_not_raise

import pytest
from jsonschema import ValidationError

from jmespath_filters.filter import Filter


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
        pytest.param({'AND': "a"}, "AND needs at least 2 expressions", id='and-string'),
        pytest.param({'OR': "a"}, "OR needs at least 2 expressions", id='or-string'),
        pytest.param({'NOT': []}, "NOT needs 1 expression only", id='not-list-1'),
        pytest.param({'NOT': ["a", "b"]}, "NOT needs 1 expression only", id='not-list-2'),
    ],
)
def test_value_errors(expression, error):
    with pytest.raises(ValueError, match=error):
        Filter(expression)


@pytest.mark.parametrize(
    'expression, expectation',
    [
        pytest.param('aaa', does_not_raise(), id='string'),
        pytest.param('', pytest.raises(ValidationError, match="'' should be non-empty"), id='empty-string'),
        pytest.param({}, pytest.raises(ValidationError, match="Failed validating 'oneOf' in schema"), id='empty-dict'),
        pytest.param(
            {'and': ['a', 'b']},
            pytest.raises(ValidationError, match="Failed validating 'oneOf' in schema"),
            id='unknown-key',
        ),
        pytest.param(
            {'AND': ['', 'a']}, pytest.raises(ValidationError, match="'' should be non-empty"), id='empty-and'
        ),
        pytest.param({'AND': "a"}, pytest.raises(ValidationError, match="'a' is not of type 'array'"), id='and-string'),
        pytest.param({'OR': "a"}, pytest.raises(ValidationError, match="'a' is not of type 'array'"), id='or-string'),
        pytest.param(
            {'NOT': []}, pytest.raises(ValidationError, match="Failed validating 'oneOf' in schema"), id='not-list-1'
        ),
        pytest.param(
            {'NOT': ["a", "b"]},
            pytest.raises(ValidationError, match="Failed validating 'oneOf' in schema"),
            id='not-list-2',
        ),
    ],
)
def test_from_json(expression, expectation):
    with expectation:
        Filter.from_json(expression)
