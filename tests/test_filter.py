import pytest

from jmespath_filters import Filter


@pytest.mark.parametrize(
    'pk, expected',
    [
        pytest.param(999, False, id='no-match'),
        pytest.param(101, True, id='match'),
    ],
)
def test_simple_expression(pk, expected, payload):
    jfilter = Filter(f"people[?general.id==`{pk}`]")
    assert jfilter.match(payload) is expected


@pytest.mark.parametrize(
    'pk, expected',
    [
        pytest.param(101, False, id='no-match'),
        pytest.param(999, True, id='match'),
    ],
)
def test_not_expression(pk, expected, payload):
    jfilter = Filter({'NOT': f"people[?general.id==`{pk}`]"})
    assert jfilter.match(payload) is expected


@pytest.mark.parametrize(
    'pk, expected',
    [
        pytest.param(999, False, id='no-match'),
        pytest.param(101, True, id='match'),
    ],
)
def test_or_expression(pk, expected, payload):
    jfilter = Filter({'OR': [f"people[?general.id==`{pk}`]", "people[?general.id==`888`]"]})
    assert jfilter.match(payload) is expected


@pytest.mark.parametrize(
    'pk, expected',
    [
        pytest.param(999, False, id='no-match'),
        pytest.param(101, True, id='match'),
    ],
)
def test_and_expression(pk, expected, payload):
    jfilter = Filter(
        {
            'AND': [
                f"people[?general.id==`{pk}`]",
                "people[?history.first_login==`2014-05-01`]",
            ]
        }
    )
    assert jfilter.match(payload) is expected


@pytest.mark.parametrize(
    'age, expected',
    [
        pytest.param(30, False, id='no-match'),
        pytest.param(50, True, id='match'),
    ],
)
def test_composed_expression(age, expected, payload):
    jfilter = Filter(
        {
            'AND': [
                "people[?history.last_login==`2014-12-02`]",
                {'NOT': f"people[?general.age==`{age}`]"},
            ]
        }
    )
    assert jfilter.match(payload) is expected
