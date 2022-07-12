#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=2:00:00
#SBATCH --output ./logs/alignqc-%j.log


rm -rf outputs/dartmouthpipeline/alignqc_results/*
cd outputs/dartmouthpipeline/alignqc_results


for fname in ../star_results/*_Aligned.sortedByCoord.out.bam; do
    id=`echo $fname | cut -d '/' -f3 | cut -d'_' -f 1`

    echo "Handling " $fname
    echo "ID: " $id

    # CollectRnaSeqMetrics
    picard CollectRnaSeqMetrics \
        I=$fname \
        O=${id}.output.RNA_Metrics \
        REF_FLAT=/gpfs/home/isears1/Repos/ecmo-rnaseq/data/ucsc_annotations_refFlat-GRCh38.txt \
        STRAND=NONE \
        RIBOSOMAL_INTERVALS=/gpfs/home/isears1/Repos/ecmo-rnaseq/data/hg38_rRNA.list &


    # MarkDuplicates
    picard MarkDuplicates \
        I=$fname \
        O=${id}.Aligned.sortedByCoord.dups.marked.bam \
        M=${id}.dups.out \
        OPTICAL_DUPLICATE_PIXEL_DISTANCE=100 \
        CREATE_INDEX=false &
    
done

wait

# Multiqc
cp ../star_results/*.final.out ./
multiqc . --filename "multiqc.alignment.qc"

echo "[+] Alignment QC complete"