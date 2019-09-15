# Copyright (c) 2019 Jeffrey Boyd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
