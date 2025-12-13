import pytest

from jmespath_filters import Filter


@pytest.fixture
def payload():
    return {
        "people": [
            {
                "general": {"id": 100, "age": 20, "other": "foo", "name": "Bob"},
                "history": {"first_login": "2014-01-01", "last_login": "2014-01-02"},
            },
            {
                "general": {"id": 101, "age": 30, "other": "bar", "name": "Bill"},
                "history": {"first_login": "2014-05-01", "last_login": "2014-05-02"},
            },
        ]
    }


@pytest.mark.parametrize(
    'pk, expected',
    [
        pytest.param(999, False, id='no-match'),
        pytest.param(101, True, id='match'),
    ],
)
def test_simple_expression(pk, expected, payload):
    jfilter = Filter(f"people[?general.id==`{pk}`].general | [0]")
    assert jfilter.match(payload) is expected


@pytest.mark.parametrize(
    'pk, expected',
    [
        pytest.param(101, False, id='no-match'),
        pytest.param(999, True, id='match'),
    ],
)
def test_not_expression(pk, expected, payload):
    jfilter = Filter({'NOT': f"people[?general.id==`{pk}`].general | [0]"})
    assert jfilter.match(payload) is expected


@pytest.mark.parametrize(
    'pk, expected',
    [
        pytest.param(999, False, id='no-match'),
        pytest.param(101, True, id='match'),
    ],
)
def test_or_expression(pk, expected, payload):
    jfilter = Filter({'OR': [f"people[?general.id==`{pk}`].general | [0]", "people[?general.id==`888`].general | [0]"]})
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
                f"people[?general.id==`{pk}`].general | [0]",
                "people[?history.first_login==`2014-05-01`].general | [0]",
            ]
        }
    )
    assert jfilter.match(payload) is expected
