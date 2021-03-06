gzip_split
==========

Tool for splitting gzipped files while:
- skipping comment lines
- preserving/stripping headers
- removing source file

### Usage

```
usage: python gzip_split.py [-h] --inf <file> [--out_pattern <str>]
                     --chunks <int> [--comment <str>] [--delete] --header
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
                          (d) none, don't copy header to any splits
```

### Example

```
# Split VCF, removing comments, copying header to all splits, removing source
python gzip_split.py \
  --inf example_data/homo_sapiens-chr21.vcf.gz \
  --out_pattern output/homo_sapiens-chr21.split{}.vcf.gz \
  --chunks 200 \
  --comment "##" \
  --header all
```

### Using gnu split

```
# Split file that has no header
inf='input_file'
outpref='outprefix'
gunzip -c $inf | gsplit -l 1000000 -d --additional-suffix '.gz' - $outpref --filter='gzip > $FILE'

```
