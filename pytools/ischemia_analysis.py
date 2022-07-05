import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.spatial import distance
import json
import numpy as np
import operator


if __name__ == "__main__":
    # Kmeans cluster
    with open("outputs/GO0002931_Homo_Sapiens_Genes.txt") as f:
        ischemia_genes = f.readlines()

    ischemia_genes = [i.strip() for i in ischemia_genes]

    mc = pd.read_csv("outputs/subread/mergedcounts.csv")
    ischemia_cpm = mc[mc["Symbol"].isin(ischemia_genes)]
    cpm_cols = [c for c in ischemia_cpm.columns if c.startswith("CPM")]
    # ischemia_cpm = ischemia_cpm[cpm_cols]

    cluster_df = ischemia_cpm[cpm_cols].T

    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(cluster_df)

    sscore = silhouette_score(cluster_df, kmeans.labels_)
    print(f"Clustering silhouette score: {sscore}")
    groupings = pd.DataFrame(
        columns=["Group Number", "Members"],
        index=range(0, 2),
        data=[(gidx, []) for gidx in range(0, 2)],
    )

    for group_num, id in zip(kmeans.labels_, cluster_df.index):

        id = id.split("_")[-1]
        groupings.loc[group_num]["Members"].append(id)

    print(groupings)
    groupings.to_csv("reports/ischemia_kmeans.csv", index=False)

    # P-values
    distances = dict()

    for col_name in cpm_cols:
        id = col_name.split("_")[-1]
        sample = ischemia_cpm[col_name].values
        others = ischemia_cpm[[c for c in cpm_cols if c != col_name]].values

        euclid_distance = distance.euclidean(sample, np.median(others, axis=1))

        distances[id] = euclid_distance

    for id, dist in sorted(distances.items(), key=operator.itemgetter(1), reverse=True):
        print(f"{id}: {dist}")
