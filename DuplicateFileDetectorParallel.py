# (c) 2018 Jeffrey Boyd

import zlib
import os
from pathlib import Path
from collections import deque
from multiprocessing import Pool


def calculate_crc32(jpg):
    with open(jpg, "rb") as j_file:
        return zlib.crc32(j_file.read())

if __name__ == "__main__":
    duplicate_count = 0
    duplicated_bytes = 0
    p = Path('.')
    dir_list = deque([x for x in p.iterdir() if x.is_dir()])
    jpg_hash_table = {}
    
    while len(dir_list) != 0:
        cur_dir = dir_list.popleft()
        print(cur_dir)
        jpgs = list(cur_dir.glob('*.jpg'))
        dir_duplicate_count = 0
        cpu_pool = Pool(8)
        duplicate_list = cpu_pool.map(calculate_crc32, jpgs)
        # print(duplicate_list)
        
        for checksum, jpg in zip(duplicate_list, jpgs):
            if checksum not in jpg_hash_table:
                jpg_hash_table[checksum] = jpg
            else:
                duplicate_count = duplicate_count + 1
                dir_duplicate_count = dir_duplicate_count + 1
                # print('{}:{} and {} are duplicates!'.format(duplicate_count,
                #     jpg, jpg_hash_table[checksum]))
                duplicated_bytes = duplicated_bytes + os.path.getsize(jpg)
                    
        dir_list.extend([x for x in cur_dir.iterdir() if x.is_dir()])
        print('\t{} duplicate jpgs'.format(dir_duplicate_count))
    
    print("Number of duplicated files: {}".format(duplicate_count))
    print("Duplicated bytes: {}".format(duplicated_bytes))
