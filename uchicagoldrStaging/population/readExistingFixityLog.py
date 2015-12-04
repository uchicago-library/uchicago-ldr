def ReadExistingFixityLog(path):
    existingFixity = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            splitLine = line.split('\t')
            splitLine[-1] = splitLine[-1].rstrip('\n')
            go = True
            for entry in splitLine[1:]:
                if entry == 'ERROR':
                    go = False
            if not go:
                continue
            try:
                existingFixity[splitLine[0]] = [splitLine[1], splitLine[2]]
            except IndexError:
                pass
    return existingFixity
