def find_destination_path(source_filepath, root_path, new_root_directory):
    path_sans_root = relpath(source_filepath, root_path)
    destination_full_path = join(new_root_directory, path_sans_root)
    return destination_full_path

def move_into_new_location(original_location, new_location):
    try:
        move(original_location, new_location)
    except Exception as e:
        return False
    return True

def copy_source_directory_tree_to_destination(new_path):
    assert not exists(new_path)
    destination_directories = dirname(new_path).split('/')
    directory_tree = ""
    for f in destination_directories:
        directory_tree = join(directory_tree,f)
        if not exists(directory_tree):
            try:
                mkdir(directory_tree,0o740)
            except Exception as e:
                return False
    return True

def clean_out_source_directory_tree(self):
    directory_tree = dirname(self.filepath)
    for src_dir, dirs, files in walk(directory_tree):
        try:
            rmdir(src_dir)
        except Exception as e:
            return False
    return True

def set_destination_ownership(file_path, user_name, group_name):
    assert exists(file_path)
    uid = getpwnam(user_name).pw_uid
    gid = getgrnam(group_name).gr_gid
    try:
        chown(file_path, uid, gid)
    except Exception as e:
        return False
    return True
