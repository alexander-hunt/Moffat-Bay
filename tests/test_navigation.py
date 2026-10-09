"""Primary navigation current-page and visibility tests."""

from html.parser import HTMLParser

import pytest
from flask import render_template, session


class NavigationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_navigation = False
        self.links = []
        self.current_elements = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "nav" and attributes.get("aria-label") == "Primary navigation":
            self.in_navigation = True
        if self.in_navigation:
            if tag == "a":
                self.links.append(attributes["href"])
            if "aria-current" in attributes:
                self.current_elements.append(
                    (tag, attributes.get("href"), attributes["aria-current"])
                )

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_navigation = False


@pytest.mark.parametrize("signed_in", [False, True])
@pytest.mark.parametrize(
    ("path", "method", "current_href"),
    [
        ("/", "GET", "/#stay"),
        ("/?source=nav", "GET", "/#stay"),
        ("/attractions", "GET", "/attractions"),
        ("/about", "GET", "/about"),
        ("/account", "GET", "/account"),
        ("/login", "POST", "/account"),
        ("/register", "POST", "/account"),
        ("/reservations/book", "GET", "/reservations/book"),
        ("/reservations/book", "POST", "/reservations/book"),
        ("/reservations/summary", "GET", "/reservations/book"),
        ("/reservations/confirmation/1", "GET", "/reservations/book"),
        ("/reservations/stays", "GET", "/reservations/stays"),
        ("/reservations/stays?query=1", "GET", "/reservations/stays"),
        ("/logout", "POST", None),
        ("/reservations/cancel", "POST", None),
        ("/reservations/confirm", "POST", None),
        ("/health", "GET", None),
        ("/missing", "GET", None),
    ],
)
def test_primary_navigation_marks_only_visible_current_destinations(
    app, signed_in, path, method, current_href
):
    with app.test_request_context(path, method=method):
        if signed_in:
            session["customer_id"] = 1
        parser = NavigationParser()
        parser.feed(render_template("base.html"))

    expected_links = ["/#stay", "/attractions", "/about"]
    expected_links += (
        ["/reservations/book", "/reservations/stays"] if signed_in else ["/account", "/account"]
    )
    assert parser.links == expected_links
    assert parser.current_elements == [
        ("a", href, "page") for href in expected_links if href == current_href
    ]


@pytest.mark.parametrize(
    ("path", "expected_href", "expected_count"),
    [
        ("/", "/#stay", 1),
        ("/attractions", "/attractions", 1),
        ("/about", "/about", 1),
        ("/account", "/account", 2),
    ],
)
def test_public_responses_mark_current_navigation(client, path, expected_href, expected_count):
    response = client.get(path)
    parser = NavigationParser()
    parser.feed(response.get_data(as_text=True))

    assert response.status_code == 200
    assert parser.current_elements == [("a", expected_href, "page")] * expected_count


@pytest.mark.parametrize("path", ["/reservations/book", "/reservations/stays"])
def test_guest_redirect_marks_account_navigation(client, path):
    response = client.get(path, follow_redirects=True)
    parser = NavigationParser()
    parser.feed(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response.request.path == "/account"
    assert parser.current_elements == [("a", "/account", "page")] * 2
