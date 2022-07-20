# Inspired by
# https://bioconductor.org/packages/release/bioc/vignettes/EnhancedVolcano/inst/doc/EnhancedVolcano.html

library(stringr)
library(EnhancedVolcano)
suppressPackageStartupMessages(library(DESeq2))
suppressPackageStartupMessages(library(org.Hs.eg.db))

# Get the outcome to analyze as an argument or assume "Gender"
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
    outcome_of_interest <- "Gender"
} else {
    outcome_of_interest <- args[1]
}

print(paste("Outcome of Interest:", outcome_of_interest))

cts <- read.csv(
    "outputs/dartmouthpipeline/count_results/all_counts.txt",
    comment.char = "#",
    sep = "\t",
    row.names = "Geneid"
)

# Remove everything but Geneid and count columns
cts <- cts[, -c(1:5)]

# Get outcome data
outcomes <- read.csv(
    "data/outcomes.csv",
    row.names = "ID"
)


# Make sure column names of cts matrix properly formated
for (cidx in seq_len(ncol(cts))) {
    old_colname <- colnames(cts)[cidx]
    id <- str_replace(
        str_split(old_colname, "_")[[1]][2], "results.", ""
    )

    id <- str_replace(id, "[.]", "-")


    colnames(cts)[cidx] <- id
}

# Ensure outcome rows and count columns have same order
cts <- cts[, rownames(outcomes)]
stopifnot(all(rownames(outcomes) == colnames(cts)))

dds <- DESeqDataSetFromMatrix(
    countData = cts,
    colData = outcomes,
    design = formula(paste("~", outcome_of_interest))
)

dds <- DESeq(dds)

res <- results(dds, alpha = 0.5)

summary(res)

res_fname <- sprintf("reports/deseq2/allres_%s.csv", outcome_of_interest)
write.csv(as.data.frame(res), file = res_fname)
filtered_res_fname <- sprintf(
    "reports/deseq2/filteredres_%s.csv",
    outcome_of_interest
)
filtered_res <- res[which(res$padj < 0.05), ]
write.csv(as.data.frame(filtered_res), file = filtered_res_fname)


vplot <- EnhancedVolcano(
    res,
    lab = rownames(res),
    x = "log2FoldChange",
    y = "pvalue",
    title = resultsNames(dds)[2],
    # boxedLabels = TRUE,
    # drawConnectors = TRUE
)

plt_fname <- sprintf("reports/deseq2/volcano_%s.png", outcome_of_interest)
ggsave(plt_fname, plot = vplot)
