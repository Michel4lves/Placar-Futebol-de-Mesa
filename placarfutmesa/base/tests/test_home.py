import pytest
from django.urls import reverse
from placarfutmesa.django_assertions import assert_contains


@pytest.fixture
def resp(client):
    resp = client.get(reverse('base:home'))
    return resp


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, '<title>PLACAR - Futebol de Mese</title>')


def test_home_link(resp):
    assert_contains(resp, f'<a href="{reverse("base:home")}" class="logo">')
