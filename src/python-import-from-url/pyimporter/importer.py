import sys
import os
import logging
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
import importlib.util
from functools import wraps
from .finder import Finder
from .loader import BaseLoader

class PathHook:
    """Abstract [path hook](https://docs.python.org/3/library/sys.html#sys.path_hooks).
    """
    def get_finder(self):
        raise NotImplementedError('Not Implemented Error: get_finder should be implemented')

    def __call__(self, path):
        self.base_path = path
        return self.get_finder()



class PathImporter(PathHook, BaseLoader, Finder):

    @wraps(Finder.find_spec)
    def find_spec(self, fullname, path=None, target=None):
        self.spec = None
        self.fullname = fullname
        for is_package in [False, True]:
            try:
                self.is_package = is_package
                self.source = self.read_source()
                self.create_spec()
                break
            except FileNotFoundError:
                pass
        return self.spec

    @wraps(PathHook.get_finder)
    def get_finder(self):
        return self

    @wraps(Finder.get_loader)
    def get_loader(self):
        return self

    @wraps(BaseLoader.get_source)
    def get_source(self):
        return self.source
    
    @wraps(BaseLoader.get_source_path)
    def get_source_path(self):
        return [self.get_location()]

    def create_spec(self):
        self.spec = importlib.util.spec_from_loader(
                    self.fullname, 
                    self.get_loader(), 
                    origin=self.get_fullpath(), 
                    is_package=self.is_package)
        return self.spec

    def path_join(self, base_path, path):
        return os.path.join(base_path, path)

    def get_location(self):
        return self.path_join(self.base_path, self.fullname.replace('.', '/'))

    def get_fullpath(self):
        suffix = '/__init__.py' if self.is_package else '.py'
        fullpath = self.get_location() + suffix
        return fullpath

    def read_source(self):
        fullpath = self.get_fullpath()
        source = None
        with open(fullpath) as file:
            source = file.read().decode().replace("\r\n", "\n")
        return source

class UrlImporter(PathImporter):

    @wraps(PathImporter.path_join)
    def path_join(self, base_path, path):
        return urljoin(base_path, path)

    @wraps(PathImporter.read_source)
    def read_source(self):
        fullpath = self.get_fullpath()
        source = None
        try:
            with urlopen(fullpath) as file:
                source = file.read().decode().replace("\r\n", "\n")
        except HTTPError as exc:
            if '404' in str(exc):
                raise FileNotFoundError(f'File Not Found Error: {self.fullname} ({fullpath})')
            raise
        return source


