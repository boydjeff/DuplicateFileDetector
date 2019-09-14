# (c) 2018 Jeffrey Boyd

import zlib
import os
from pathlib import Path
from collections import deque


if __name__ == "__main__":
    duplicate_count = 0
    duplicated_bytes = 0
    p = Path('.')
    dir_list = deque([x for x in p.iterdir() if x.is_dir()])
    file_hash_table = {}
    
    while len(dir_list) != 0:
        cur_dir = dir_list.popleft()
        print(cur_dir)
        # cur_dir_files = list(cur_dir.glob('*.*'))
        cur_dir_files = list([x for x in os.scandir(cur_dir) if x.is_file()])
        dir_duplicate_count = 0

        # print(cur_dir_files)
        for cur_file_path in cur_dir_files:
            try:
                with open(cur_file_path, "rb") as cur_file:
                    checksum = zlib.crc32(cur_file.read())
                if checksum not in file_hash_table:
                    file_hash_table[checksum] = cur_file_path
                else:
                    dir_duplicate_count = dir_duplicate_count + 1
                    print('{}:{} and {} are duplicates!'.format(duplicate_count,
                        cur_file_path, file_hash_table[checksum]))
                    duplicated_bytes = duplicated_bytes + os.path.getsize(cur_file_path)
            except:
                print("Error opening {}".format(cur_file_path))
        duplicate_count = duplicate_count + dir_duplicate_count
        dir_list.extend([x for x in cur_dir.iterdir() if x.is_dir()])
        print('\t{} duplicate files'.format(dir_duplicate_count))
    
    print("Number of duplicated files: {}".format(duplicate_count))
    print("Duplicated bytes: {}".format(duplicated_bytes))
