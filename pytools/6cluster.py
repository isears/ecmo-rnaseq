"""
On Silhouette score analysis, 6 groupings looked good, so generating the 6 groups
"""
from sklearn.cluster import KMeans
import pandas as pd
import pprint


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

    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans.fit(mc)

    groupings = pd.DataFrame(
        columns=["Group Number", "Members"],
        index=range(0, 6),
        data=[(gidx, []) for gidx in range(0, 6)],
    )

    for group_num, id in zip(kmeans.labels_, mc.index):
        id = id.split("_")[-1]

        groupings.loc[group_num]["Members"].append(id)

    print(groupings)

    groupings.to_csv("reports/6cluster_kmeans.csv", index=False)
