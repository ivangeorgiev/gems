import sys
from .importer import UrlImporter

_url_importer = None

def register_finder(finder, as_priority=False):
    global _url_importer
    if finder in sys.path_hooks:
        sys.path_hooks.remove(finder)
    if as_priority:
        sys.path_hooks.insert(0, finder)
    else:
        sys.path_hooks.append(finder)

def disable_url_import():
    global _url_importer
    if _url_importer in sys.path_hooks:
        sys.path_hooks.remove(_url_importer)

def enable_url_import(as_priority=False):
    global _url_importer
    if _url_importer is None:
        _url_importer = UrlImporter()
    register_finder(_url_importer, as_priority)
