def writeFixityLog(path,batch,existingHashes=None):
    newHashes={}
    with open(path,'a') as f:
        for item in batch.find_items(from_directory=True):
            if item.test_readability():
                item.set_root_path(batch.get_root())
                if relpath(item.get_file_path(),start=item.get_root_path()) not in existingHashes:
                    item.set_sha256(item.find_sha256_hash())
                    item.set_md5(item.find_md5_hash())
                    newHashes[relpath(item.get_file_path(),start=item.get_root_path())]=
        for entry in newHashes:
            f.wirte(entry+'\t'+newHashes[0]+newHashes[1]+'\n')
