
class Loader:
    """Interface defintion for a [Loader](https://docs.python.org/3/glossary.html#term-loader)
    See also [Loader reference](https://docs.python.org/3/reference/import.html#loaders).
    """
    def create_module(self, spec):
        raise NotImplementedError('Not Implemented Error: create_module should be implemented')

    def exec_module(self, mod):
        raise NotImplementedError('Not Implemented Error: exec_module should be implemented')

class BaseLoader(Loader):
    def create_module(self, spec):
        return None

    def get_source_path(self):
        raise NotImplementedError('Not Implemented Error: get_source should be implemented')

    def get_source(self):
        raise NotImplementedError('Not Implemented Error: get_source should be implemented')

    def exec_module(self, mod):
        mod.__path__ = self.get_source_path()
        exec(self.get_source(), mod.__dict__)
    