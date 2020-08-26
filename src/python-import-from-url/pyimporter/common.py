import sys
from .importer import UrlImporter

def register_finder(finder, as_priority=False):
    if as_priority:
        sys.path_hooks.insert(0, finder)
    else:
        sys.path_hooks.append(finder)

def enable_url_import(as_priority=False):
    register_finder(UrlImporter(), as_priority)
