
from django.conf import settings
import pandas as pd
import pytest

from crm import services


@pytest.fixture
def sample_lighthouse_data():
    return {
        "lighthouseResult": {
            "categories": {
                "performance": {"score": 0.8},
                "accessibility": {"score": 0.9}
            },
            "audits": {
                "first-contentful-paint": {"score": 0.9},
                "color-contrast": {"score": 0.4}
            }
        }
    }


def test_parse_category_scores(sample_lighthouse_data):
    client = services.LighthouseAnalysisClient()
    client._parse_category_scores(
        sample_lighthouse_data["lighthouseResult"]["categories"])
    assert client.data["scores"] == {
        "performance": 0.8,
        "accessibility": 0.9
    }


@pytest.mark.parametrize("input_desc, expected", [
    ("[Link text](url) and more", "Link text and more"),
    ("[Learn more](url)", "Learn more"),
    ("Text [with link](url) here. Learn more.", "Text with link here."),
])
def test_clean_description_regex(input_desc, expected):
    assert services.clean_description_regex(input_desc) == expected


@pytest.mark.parametrize("score, expected_tier", [
    (0.95, "Pass"),
    (0.75, "Needs Work"),
    (0.3, "Fail"),
    (0.9, "Pass"),
    (0.5, "Needs Work"),
])
def test_get_tier(score, expected_tier):
    assert services.get_tier(score) == expected_tier


@pytest.fixture
def sample_lighthouse_data():
    return {
        "lighthouseResult": {
            "categories": {
                "performance": {"score": 0.8},
                "accessibility": {"score": 0.9}
            },
            "audits": {
                "first-contentful-paint": {"score": 0.9, "weight": 1},
                "color-contrast": {"score": 0.4, "weight": 0.1}
            }
        }
    }


def test_parse_category_scores(sample_lighthouse_data):
    client = services.LighthouseAnalysisClient()
    client._parse_category_scores(
        sample_lighthouse_data["lighthouseResult"]["categories"])
    assert client.data["scores"] == {
        "performance": 0.8,
        "accessibility": 0.9
    }


@pytest.mark.django_db
def test_init():
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    key = settings.GOOGLE_API_KEY
    data = {
        "scores": {},
        "insights": {"passed": [], "failed": []},
        "sections": [],
    }

    client = services.LighthouseAnalysisClient()
    assert client.endpoint == endpoint
    assert client.key == key
    assert client.data == data


@pytest.mark.django_db
def test_build_params():
    key = settings.GOOGLE_API_KEY
    site = "https://www.charlie-marshall.dev"
    expected_params = f"?url={site}&key={key}&category=1&category=2&category=3&category=4&category=5"

    client = services.LighthouseAnalysisClient()
    actual_params = client._build_params(site)

    assert actual_params == expected_params


@pytest.mark.django_db
def test_build_params():
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    key = settings.GOOGLE_API_KEY
    site = "https://www.charlie-marshall.dev"
    params = f"?url={site}&key={key}&category=1&category=2&category=3&category=4&category=5"
    expected_url = f"{endpoint}{params}"

    client = services.LighthouseAnalysisClient()
    client_params = client._build_params(site)
    actual_url = client._build_url(client_params)

    assert actual_url == expected_url
