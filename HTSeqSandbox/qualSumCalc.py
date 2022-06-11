import numpy as np
import HTSeq
import itertools

fastq_file = HTSeq.FastqReader("sampledata/sample.fastq")
sample_read = next(fastq_file)
qualsum = np.zeros(len(sample_read), int)


fastq_file = HTSeq.FastqReader("sampledata/sample.fastq")

for idx, read in enumerate(fastq_file):
    qualsum += read.qual
