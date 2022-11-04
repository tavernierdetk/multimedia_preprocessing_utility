import os, shutil

def get_visible_dir(path):
    dirs = _get_visible_dir_unsorted(path)
    return sorted(dirs)

def _get_visible_dir_unsorted(path):
    for f in os.listdir(f'{path}'):
        if not f.startswith('.'):
            yield f

def delete_dir_and_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(folder)

