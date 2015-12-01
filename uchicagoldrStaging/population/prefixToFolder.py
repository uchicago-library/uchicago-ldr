def prefixToFolder(popRoot,prefix):
    from uchicagoldrStaging.lib import getImmediateSubDirs
    from re import match

    existingPopSubDirs=[name for name in getImmediateSubDirs(popRoot) if match('^'+prefix,name)]

    if len(existingPopSubDirs) == 0:
        return prefix+str(1)
    else:
        nums=[int(dirname.strip(prefix)) for dirname in existingPopSubDirs]
        nums.sort()
        nextNum=str(nums[-1]+1)
        return prefix+str(nextNum)
