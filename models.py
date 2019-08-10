# -*- coding: utf-8 -*-
import sys
import settings


class Section:
    def __init__(self, index, title, subsections, source=None):
        self._source = source
        self._index = index
        self._title = title
        self._subsections = subsections

        for subsection in self._subsections:
            subsection._parent = self

    def __str__(self):
        return f"[{self._index}] - {self._title}"

    def subsections(self):
        return self._subsections

    def isDefault(self):
        return self._source is None


class Subsection:
    def __init__(self, index, title, url=None, source=None):
        self._parent = None
        self._source = source
        self._index = index
        self._title = title
        self._url = url

    def __str__(self):
        return f"[{self._index}] - {self._title}"

    def isDefault(self):
        return self._source is None

    def url(self):
        return self._url
