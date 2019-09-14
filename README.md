# DuplicateFileDetector
Python script for detecting duplicate files, optionally copying files to a new directory, excluding the duplicates, of course. It uses the CRC32 checksum to detect duplicate files.

I created this to clean up my father's picture folder because he would copy whole memory cards at a time, without bothering to delete files from the card that he had already copied over to his computer. The result was that he had multiple folders with many duplicates.

I thought I'd be clever and try out a version that does multiple crc32 calculations in parallel. However it wasn't faster than the non-parellel version in my first simple tests. Maybe I'll investigate why someday...

# Known Issues
It doesn't actually copy files into a new, clean, duplicate-free directory, yet.