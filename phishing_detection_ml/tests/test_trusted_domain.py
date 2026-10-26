import pytest
from src.trusted_domains import trusted_domain

@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://github.com/", "github.com"),
        ("https://github.com", "github.com"),
        ("http://google.com/", "google.com"),
        ("https://www.wikipedia.org/", "wikipedia.org"),
        ("https://amazon.in/", "amazon.in"),

        ("https://www.github.com/", "github.com"),
        ("https://mail.google.com/", "google.com"),


        ("https://github.com/attacker/malicious-repo", "github.com"),


        ("https://gist.github.com/", None),
        ("https://pages.github.com/", None),
        ("https://docs.google.com/", None),
        ("https://drive.google.com/", None),


        ("https://github.com.example.com/", None),
        ("https://notgithub.com/", None),
        ("https://example.com/", None),


        ("", None),
        ("   ", None),
        (None, None),
        (123, None),
    ],
)
def test_trusted_domain_cases(url, expected):
    assert trusted_domain(url) == expected

def test_trailing_dot_hostname():
    assert trusted_domain("https://github.com./") == "github.com"

def test_case_insensitive_hostname():
    assert trusted_domain("https://GITHUB.COM/") == "github.com"

def test_untrusted_subdomain_of_trusted_domain():
    assert trusted_domain("https://attacker.github.com/") == "github.com"

def test_excluded_host_with_path():
    assert trusted_domain("https://gist.github.com/someone/repo") is None
