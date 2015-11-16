def RecordFieldsValidation():
    return [\
            ['accession number', ["^\d{4}-\d{3}$"]],\
            ['department', []],\
            ['summary', []],\
            ['fiscalYear', [".{1,}"]],\
            ['ark', ["^\w{13}$"]],\
            ['collection', [".{1,}"]],\
            ['eadid', [".{1,}"]],\
            ['spanDate', []],\
            ['type', ["^AR$|^Ar$|^MS$|^Ms$|^CJA$|^OTHER$"]],\
            ['prc', ["^P$|^p$|^R$|^r$|^C$|^c$"]],\
            ['rights', [".{1,}"]],\
            ['restrictions', ["^R-|^r-"]],\
            ['restrictionComment', []],\
            ['totalDigitalSize', []],\
            ['digitalCondition', []],\
            ['totalPhysicalSize', []],\
            ['physicalCondition', []],\
            ['physicalLocation', []],\
            ['fileRecDate', []],\
            ['fileInfo', []],\
            ['fileAccDate', [".{1,}"]],\
            ['fileTransDate', []],\
            ['fileBackDate', []],\
            ['fileDelDate', []],\
            ['donor', []],\
            ['source', []],\
            ['origin', []],\
            ['permittedUseAccess', ["^True$|^False$"]],\
            ['permittedUseDiscover', ["^True$|^False$"]],\
            ['adminNote', []],\
            ['priority', []],\
            ['existingDigitalCollection', ["^True$|^False$"]],\
            ['dasRecDate', [".{1,}"]],\
            ['recLetter', ["^True$|^False$"]],\
            ['sendInv', ["^True$|^False$"]],\
            ['giftAckOrDeed', ["^True$|^False$"]],\
            ['access', []],\
            ['recBy', []],\
            ['dasRecBy', []],\
            ['addenda', ["^True$|^False$"]],\
            ['physicalMedia', []],\
            ['existingPhysicalCollection', ["^True$|^False$"]],\
            ['physicalHasFindingAid', ["^True$|^False$"]],\
            ['sentToDASOn', []]\
]
