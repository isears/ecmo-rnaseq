library(stringr)
suppressPackageStartupMessages(library(DESeq2))


cts <- read.csv(
    "outputs/dartmouthpipeline/count_results/all_counts.txt",
    comment.char = "#",
    sep = "\t",
    row.names = "Geneid"
)

outcomes <- read.csv(
    "data/outcomes.csv",
    row.names = "ID"
)

# Remove everything but Geneid and count columns
cts <- cts[, -c(1:5)]

ordered_outcomes <- c()

for (cidx in seq_len(ncol(cts))) {
    old_colname <- colnames(cts)[cidx]
    id <- str_replace(
        str_split(old_colname, "_")[[1]][2], "results.", ""
    )

    id <- str_replace(id, "[.]", "-")

    this_outcome <- outcomes[id, "Gender"]
    ordered_outcomes <- append(ordered_outcomes, this_outcome)

    colnames(cts)[cidx] <- id
}


condition <- factor(ordered_outcomes)
dds <- DESeqDataSetFromMatrix(cts, DataFrame(condition), ~condition)
dds <- DESeq(dds)

res <- results(dds, alpha = 0.5)
summary(res)

write.csv(as.data.frame(res), file = "outputs/deseq2_results.csv")
