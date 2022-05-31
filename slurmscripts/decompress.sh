#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=3:00:00
#SBATCH --output ./logs/decompress-%j.log


cd ~/data/ECMO_RNASeq/30-573159527/00_fastq/

for FILE in *.gz; 
do 
    UNCOMPRESSED=${FILE::-3}
    echo Unzipping $FILE to $UNCOMPRESSED
    gunzip -c $FILE >../../decompressed/$UNCOMPRESSED; 
done