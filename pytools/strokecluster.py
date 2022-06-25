import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


top_10_stroke_genes = [
    # Down expressed, by p-value smallest to largest
    "ENSG00000077348",
    "ENSG00000104980",
    "ENSG00000189046",
    "ENSG00000117318",
    "ENSG00000007312",
    "ENSG00000154016",
    "ENSG00000140545",
    "ENSG00000215788",
    # Up expressed, by p-value smallest to largest
    "ENSG00000118520",
    "ENSG00000138411",
]

if __name__ == "__main__":
    mc = pd.read_csv(
        "/gpfs/home/isears1/Repos/ecmo-rnaseq/outputs/subread/mergedcounts.csv"
    )

    kept_cols = [col for col in mc.columns if "CPM_" in col]

    # x axis: gene expression lvls (counts per million)
    # y axis: patients
    mc = mc.set_index("Geneid")
    mc = mc[kept_cols]
    mc = mc.T

    # Filter down to only stroke-related genes
    mc = mc.filter(items=top_10_stroke_genes)

    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(mc)

    groupings = pd.DataFrame(
        columns=["Group Number", "Members"],
        index=range(0, 2),
        data=[(gidx, []) for gidx in range(0, 2)],
    )

    for group_num, id in zip(kmeans.labels_, mc.index):
        id = id.split("_")[-1]

        groupings.loc[group_num]["Members"].append(id)

    print(groupings)
    sscore = silhouette_score(mc, kmeans.labels_)
    print(f"Silhouette score: {sscore}")

    groupings.to_csv("reports/stroke_kmeans.csv", index=False)
