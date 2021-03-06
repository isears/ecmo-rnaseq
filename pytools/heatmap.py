import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import pandas as pd


if __name__ == "__main__":
    mc = pd.read_csv(
        "/gpfs/home/isears1/Repos/ecmo-rnaseq/outputs/subread/mergedcounts.csv"
    )

    top_20 = mc.nlargest(20, "TotalCount")

    cpm_cols = [col for col in mc.columns if "CPM_" in col]
    sample_labels = [x.split("_")[-1] for x in cpm_cols]
    top_20 = top_20[cpm_cols + ["Symbol"]]

    ax = sns.heatmap(
        top_20[cpm_cols].values,
        xticklabels=sample_labels,
        yticklabels=top_20["Symbol"].to_list(),
    )
    ax.figure.tight_layout()
    plt.savefig("reports/heatmap.png")
