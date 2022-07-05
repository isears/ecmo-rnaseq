#!/bin/bash
#SBATCH -n 1
#SBATCH -p debug
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output ./logs/debug-%j.log


export PYTHONUNBUFFERED=TRUE
source /gpfs/runtime/opt/anaconda/3-5.2.0/bin/activate /users/isears1/anaconda/rnaseq
echo $1

echo "Establishing connection back to $SLURM_SUBMIT_HOST:45589"
python -m debugpy --connect $SLURM_SUBMIT_HOST:45589 --wait-for-client $1