gzip_split
==========

Tool for splitting gzipped files while:
- skipping comment lines
- preserving/stripping headers
- removing source file

### Usage

```
python gzip_split.py --help
usage: gzip_split.py [-h] --inf <file> [--out_pattern <str>] --chunks <int>
                     [--comment <str>] [--delete] --header
                     {no_header,first,all,none}

optional arguments:
  -h, --help            show this help message and exit
  --inf <file>          Input gzip file
  --out_pattern <str>   Output pattern, using "{}" as a wildcard. If not
                        specified, will use input path.
  --chunks <int>        Number of chunks to split into
  --comment <str>       Skip lines at top of file that start with this
                        character
  --delete              Deletes the source file upon successful completion
  --header {no_header,first,all,none}
                        Header mode:
                          (a) no_header, the input does not contain a header
                          (b) first, copy the header to the first split only
                          (c) all, copy the header to all splits
                          (d) none, skip the header (don't copy to any outputs)
```
