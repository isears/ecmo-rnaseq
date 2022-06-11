import HTSeq
import itertools

fastq_file = HTSeq.FastqReader("sampledata/sample.fastq")
print(fastq_file)

for idx, read in enumerate(fastq_file):
    print("Read name:")
    print(read.name)
    print("Read seq:")
    print(read.seq)
    print("Read qual:")
    print(read.qual)
    if idx > 3:
        break
