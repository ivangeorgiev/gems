class Finder:
    """Interface defintion for a [finder](https://docs.python.org/3/glossary.html#term-finder).
    """
    
    def find_spec(self, fullname, path=None, target=None):
        raise NotImplementedError('Not Implemented Error: find_spec should be implemented')

    def get_loader(self):
        raise NotImplementedError('Not Implemented Error: get_loader should be implemented')

