#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

params.inputdir = "/gpfs/home/isears1/Repos/ecmo-rnaseq/data/30-573159527/00_fastq"
params.genome = "/gpfs/data/shared/databases/refchef_refs/grch38_release98/gtf/Homo_sapiens.GRCh38.98.gtf"
params.outdir = "results"

println "reads: $params.reads"

process 