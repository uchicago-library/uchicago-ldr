def getImmediateSubDirs(path):
    from os import listdir
    from os.path import isdir, join

    return [name for name in listdir(path) if isdir(join(path, name))]
