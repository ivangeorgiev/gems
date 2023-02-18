from fnmatch import fnmatch

def ls_matching(path, pattern):
    result = [f for f in dbutils.fs.ls(path)]
    pass
