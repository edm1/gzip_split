#!/usr/bin/env bash
#

mkdir -p output

python gzip_split.py \
  --inf example_data/homo_sapiens-chr21.vcf.gz \
  --out_pattern output/homo_sapiens-chr21.split{}.vcf.gz \
  --chunks 200 \
  --comment "##" \
  --header all
