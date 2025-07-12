#!/usr/bin/env python3
""" Task 5: Expiring Web Cache """
import redis
import requests
from typing import Callable

r = redis.Redis()


def get_page(url: str) -> str:
    """Fetch and cache HTML content for a given URL"""
    key = f"count:{url}"
    cached_html = r.get(url)

    if cached_html:
        return cached_html.decode('utf-8')

    # Increment access count
    r.incr(key)

    # Fetch and cache the page
    response = requests.get(url)
    html = response.text
    r.setex(url, 10, html)  # Cache for 10 seconds
    return html