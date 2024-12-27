import pytest
from django.urls import reverse
from placarfutmesa.django_assertions import assert_contains


@pytest.fixture
def resp(client):
    resp = client.get(reverse('home'))
    return resp


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, '<title>Curso de Python e Django</title>')


def test_home_link(resp):
    assert_contains(resp, f'<a class="navbar-brand text-light" href="{reverse("home")}">')
