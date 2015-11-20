def getImmediateSubDirs(path):
    return [name for name in listdir(path) if isdir(join(path,name))]
