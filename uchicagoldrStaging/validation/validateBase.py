

def ValidateBase(path,
                 shouldBeRoot=None,
                 shouldBeArk=None,
                 shouldBeEAD=None,
                 shouldBeAccNo=None):

    from os import listdir
    from os.path import isdir, join, split
    from re import match

    observedRoot = None
    observedArk = None
    observedEAD = None
    observedAccNo = None

    if not (isdir(path)):
        return (False, observedRoot, observedArk, observedEAD, observedAccNo)

    if split(path)[-1] == '':
        observedRoot = split(split(path)[0])[0]
    else:
        observedRoot = split(path)[0]

    if shouldBeRoot != None:
        if shouldBeRoot != observedRoot:
            return (False,
                    observedRoot, observedArk,
                    observedEAD, observedAccNo)
    shouldBeRoot = observedRoot

    if split(path)[-1] == '':
        observedArk = split(split(path)[0])[1]
    else:
        observedArk = split(path)[1]
    if shouldBeArk != None:
        if shouldBeArk != observedArk:
            return (False,
                    observedRoot, observedArk,
                    observedEAD, observedAccNo)
    shouldBeArk = observedArk
    if not match("^\w{13}$", shouldBeArk):
        return (False,
                observedRoot, observedArk,
                observedEAD, observedAccNo)

    if len(listdir(join(shouldBeRoot, shouldBeArk))) == 1:
        observedEAD = listdir(join(observedRoot, shouldBeArk))[0]
    else:
        return (False,
                observedRoot, observedArk,
                observedEAD, observedAccNo)
    if shouldBeEAD != None:
        if shouldBeEAD != observedEAD:
            return (False,
                    observedRoot, observedArk,
                    observedEAD, observedAccNo)
    shouldBeEAD = observedEAD

    if len(listdir(join(shouldBeRoot, shouldBeArk, shouldBeEAD))) == 1:
        observedAccNo = listdir(join(
            shouldBeRoot, shouldBeArk, shouldBeEAD))[0]
    else:
        return (False,
                observedRoot, observedArk,
                observedEAD, observedAccNo)
    if shouldBeAccNo != None:
        if shouldBeAccNo != observedAccNo:
            return (False,
                    observedRoot, observedArk,
                    observedEAD, observedAccNo)
    shouldBeAccNo = observedAccNo
    if not match("^\d{4}-\d{3}$", shouldBeAccNo):
        return (False,
                observedRoot, observedArk,
                observedEAD, observedAccNo)

    for folder in ['admin', 'data']:
        if folder not in listdir(join(
                shouldBeRoot, shouldBeArk, shouldBeEAD, shouldBeAccNo)):
            return (False,
                    observedRoot, observedArk,
                    observedEAD, observedAccNo)
    if len(listdir(join(
            shouldBeRoot, shouldBeArk, shouldBeEAD, shouldBeAccNo))) != 2:
        return (False,
                observedRoot, observedArk,
                observedEAD, observedAccNo)

    return (True,
            observedRoot, observedArk,
            observedEAD, observedAccNo)
