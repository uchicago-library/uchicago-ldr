def WriteFixityLog(path, batch, existingHashes=None):
    from os.path import relpath

    newHashes = {}
    for item in batch.find_items(from_directory=True):
        if item.test_readability():
            item.set_root_path(batch.root)
            if existingHashes:
                if relpath(
                        item.get_file_path(), start=item.get_root_path()
                ) in existingHashes:
                    continue
            item.set_sha256(item.find_sha256_hash())
            item.set_md5(item.find_md5_hash())
            newHashes[relpath(
                item.get_file_path(), start=item.get_root_path()
                    )] = [item.get_sha256(), item.get_md5()]
    with open(path, 'a') as f:
        for entry in newHashes:
            f.write(entry+'\t'+newHashes[entry][0] +
                    "\t"+newHashes[entry][1]+'\n')
