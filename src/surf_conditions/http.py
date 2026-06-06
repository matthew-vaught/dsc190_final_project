"""Small HTTP helpers for public JSON/text APIs."""

from __future__ import annotations

import json
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


JsonObject = dict[str, Any]

USER_AGENT = "surf-conditions/0.1 (student project; contact: local-cli)"


class SurfConditionsError(Exception):
    """Raised when live surf condition data cannot be fetched or parsed."""


def fetch_json(url: str, params: dict[str, str] | None = None) -> JsonObject:
    full_url = _with_params(url, params)
    request = Request(full_url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except HTTPError as error:
        raise SurfConditionsError(f"{url} returned HTTP {error.code}") from error
    except URLError as error:
        raise SurfConditionsError(f"Could not reach {url}: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise SurfConditionsError(f"{url} returned invalid JSON") from error

    if not isinstance(payload, dict):
        raise SurfConditionsError(f"{url} returned an unexpected JSON shape")
    return cast(JsonObject, payload)


def fetch_text(url: str, params: dict[str, str] | None = None) -> str:
    full_url = _with_params(url, params)
    request = Request(full_url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=20) as response:
            body = cast(bytes, response.read())
    except HTTPError as error:
        raise SurfConditionsError(f"{url} returned HTTP {error.code}") from error
    except URLError as error:
        raise SurfConditionsError(f"Could not reach {url}: {error.reason}") from error
    return body.decode("utf-8")


def _with_params(url: str, params: dict[str, str] | None) -> str:
    if not params:
        return url
    return f"{url}?{urlencode(params)}"
