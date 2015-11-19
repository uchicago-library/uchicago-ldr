def createStagingStructure(root,ark,ead,accno):
    from os.path import join,exists

    from uchicagoldr.bash_cmd import BashCommand

    assert(exists(root))
    mkAdminDirArgs=['mkdir','-p',join(root,ark,ead,accno,"admin")]
    mkAdminDirCommand=BashCommand(mkAdminDirArgs)
    assert(mkAdminDirCommand.run_command()[0])
    assert(mkAdminDirCommand.get_data()[1].returncode == 0)
    mkDataDirArgs=['mkdir',join(root,ark,ead,accno,"data")]
    mkDataDirCommand=BashCommand(mkDataDirArgs)
    assert(mkDataDirCommand.run_command()[0])
    assert(mkDataDirCommand.get_data()[1].returncode == 0)
    return join(root,ark)
