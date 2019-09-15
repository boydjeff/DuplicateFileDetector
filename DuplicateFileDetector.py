# (c) 2018 Jeffrey Boyd

import zlib
import os
import sys
import shutil
from pathlib import Path
from collections import deque


if __name__ == "__main__":
    duplicate_count = 0
    duplicated_bytes = 0
    dir_list = deque([x for x in Path('.').iterdir() if x.is_dir()])
    file_hash_table = {}
    if len(sys.argv) == 2:
        dest_dir = Path(sys.argv[1])
        if (dest_dir.is_dir() == True):
            copy_files = True
        else:
            print("'{}' is not a valid directory.".format(dest_dir))
            sys.exit("You must specify a valid destination directory.")
    
    while len(dir_list) != 0:
        cur_dir = dir_list.popleft()
        print("Checking directory '{}'".format(cur_dir))
        cur_dir_files = list([x for x in os.scandir(cur_dir) if x.is_file()])
        dir_duplicate_count = 0

        # print(cur_dir_files)
        for cur_file_path in cur_dir_files:
            try:
                with open(cur_file_path, "rb") as cur_file:
                    checksum = zlib.crc32(cur_file.read())
                if checksum in file_hash_table:
                    dir_duplicate_count = dir_duplicate_count + 1
                    print('{} and {} are duplicates!'.format(cur_file_path.path,
                        file_hash_table[checksum].path))
                    duplicated_bytes = duplicated_bytes + os.path.getsize(cur_file_path)
                else:
                    file_hash_table[checksum] = cur_file_path
            except:
                print("Error opening {}".format(cur_file_path.path))
        duplicate_count = duplicate_count + dir_duplicate_count
        dir_list.extend([x for x in cur_dir.iterdir() if x.is_dir()])
        print('\t{} duplicate files'.format(dir_duplicate_count))
    
    print("Number of duplicated files: {}".format(duplicate_count))
    print("Duplicated bytes: {}".format(duplicated_bytes))

    # Now copy the files to a clean directory
    if copy_files == True:
        print("Copying files to {}".format(dest_dir))
        for file_path in file_hash_table.values():
            new_dest_dir = Path(os.path.join(dest_dir, file_path)).parent
            new_dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, new_dest_dir)
