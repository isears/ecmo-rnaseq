#!/bin/bash
#SBATCH -n 1
#SBATCH -p debug
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output ./logs/multiqc-%j.log

cd outputs/dartmouthpipeline/fastqc_results
multiqc .