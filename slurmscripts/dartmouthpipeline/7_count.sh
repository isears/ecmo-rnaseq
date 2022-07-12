#!/bin/bash
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --cpus-per-task=32
#SBATCH --mem=40G
#SBATCH --time=2:00:00
#SBATCH --output ./logs/count-%j.log


rm -rf outputs/dartmouthpipeline/count_results/*
cd outputs/dartmouthpipeline/count_results


for fname in ../star_results/*_Aligned.sortedByCoord.out.bam; do
    id=`echo $fname | cut -d '/' -f3 | cut -d'_' -f 1`

    echo "Handling " $fname
    echo "ID: " $id

    # Htseq count throwing warnings that seem to be the result of bugs:
    # https://github.com/simon-anders/htseq/issues/37
    # TODO: confirm -s no (not stranded) if the results are strange
    # htseq-count \
    #     -f bam \
    #     -s no \
    #     -r pos \
    #     --additional-attr "gene_name" \
    #     $fname \
    #     /gpfs/data/shared/databases/refchef_refs/grch38_release98/gtf/Homo_sapiens.GRCh38.98.gtf > $id.htseq-counts &

    # -p for paired-end reads
    # -Q minimum quality score
    # -s 0 for unstranded library prep; -s 1 and -s 2 both yield about half as many counts
    featureCounts \
        -p \
        -t exon \
        -g gene_id \
        -Q 20 \
        -T 32 \
        -s 0 \
        -a /gpfs/data/shared/databases/refchef_refs/grch38_release98/gtf/Homo_sapiens.GRCh38.98.gtf \
        -o ./${id}_counts.txt \
        $fname
done

echo "[+] Counting completed"