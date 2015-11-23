def ValidateOrganization(targetPath,reqTopFiles=[],reqDirContents=[]):
    from os.path import isdir,isfile,join
    from os import listdir
    from re import match

    returnDict={}
    returnDict['dirs']=[]
    returnDict['notDirs']=[]
    returnDict['prefixes']=[]
    returnDict['badPrefixes']=[]
    returnDict['missingDirs']=[]
    returnDict['missingReqs']=[]

    if not isdir(targetPath):
        return((False,returnDict))

    targetTopFileList=[x for x in listdir(targetPath) if isfile(join(targetPath,x))]
    targetFolderList=[x for x in listdir(targetPath) if isdir(join(targetPath,x))]
    for x in targetFolderList:
        returnDict['dirs'].append(x)

    if targetFolderList != listdir(targetPath):
        for x in listdir(targetPath):
            if x not in targetFolderList:
                returnDict['notDirs'].append(x)

    for x in targetFolderList:
        prefix=match('^[a-zA-Z_\-]*',x)
        try:
            returnDict['badPrefixes'].append(prefix.group(1))
        except IndexError:
            returnDict['prefixes'].append(prefix.group(0))
        dirContents=[y for y in listdir(join(targetPath,x))]
        for req in reqDirContents:
            if req not in dirContents:
                returnDict['missingReqs'].append(join(targetPath,x,req))

    returnDict['prefixes']=set(returnDict['prefixes'])
    returnDict['badPrefixes']=set(returnDict['badPrefixes'])


    for prefix in returnDict['prefixes']:
        prefixSet=[directory for directory in listdir(targetPath) if match('^'+prefix,directory)]
        nums=[]
        for folder in prefixSet:
            num=folder.lstrip(prefix)
            nums.append(int(num))
        maxNum=max(nums)
        for i in range(1,maxNum+1):
            if i not in nums:
                returnDict['missingDirs'].append(prefix+str(num))
    if len(returnDict['missingDirs'])>0:
        return((False,returnDict))
    if len(returnDict['badPrefixes']) > 0:
        return((False,returnDict))
    if len(returnDict['missingReqs'])>0:
        return((False,returnDict))
    return ((True,returnDict))
