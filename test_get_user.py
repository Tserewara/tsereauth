import pytest

from application import get_user

fake_db = [
    {
        'id': 1,
        'username': 'Alvaro',
        'password': 'pass123'
    },
    {
        'id': 2,
        'username': 'Tserewara',
        'password': 'pass123'
    }
]


def test_returns_user_when_it_exists():
    user = get_user('Alvaro', fake_db)
    assert user == fake_db[0]


def test_raises_error_if_user_does_not_exist():
    with pytest.raises(Exception, match='Wrong credentials'):
        get_user('John', fake_db)
