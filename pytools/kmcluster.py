from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd
import pprint
import json


def do_cluster(df: pd.DataFrame, num_clusters: int, pca: int = None):
    if pca:
        pca = PCA(n_components=pca, random_state=42)
        df = pca.fit_transform(df)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(df)

    try:
        sscore = silhouette_score(df, kmeans.labels_)
    except ValueError:
        print(
            f"[-] Warning: silhouette score no calculated for PCA {pca} and n_clusters {num_clusters}"
        )
        sscore = 0.0

    return sscore


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    # Can only do PCA up to # of samples
    hyperparam_pca = [None] + list(range(2, 18))

    # Should only go up to n_samples / 2
    hyperparam_n_clusters = list(range(2, 9))

    mc = pd.read_csv(
        "/gpfs/home/isears1/Repos/ecmo-rnaseq/outputs/subread/mergedcounts.csv"
    )

    kept_cols = [col for col in mc.columns if "CPM_" in col]

    # x axis: gene expression lvls (counts per million)
    # y axis: patients
    mc = mc.set_index("Geneid")
    mc = mc[kept_cols]
    mc = mc.T

    print(
        f"{len(hyperparam_pca)} PCA options and {len(hyperparam_n_clusters)} cluster options"
        f"for a total of {len(hyperparam_pca) * len(hyperparam_n_clusters)} iterations"
    )

    sscores = list()
    for pca in hyperparam_pca:
        plt_points = list()

        for n_clusters in hyperparam_n_clusters:
            print(f"PCA {pca}, clusters {n_clusters}")
            sscore = do_cluster(mc, n_clusters, pca)
            plt_points.append(sscore)
            sscores.append({"PCA": pca, "Clusters": n_clusters, "sscore": sscore})

        if pca == None or pca == 2 or pca == 13:
            plt.plot(hyperparam_n_clusters, plt_points, "o--", label=f"PCA {pca}")

    pp.pprint(sscores)
    with open("reports/kmeans_rawdata.json", "w") as f:
        json.dump(sscores, f)

    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Score")
    plt.legend()
    plt.savefig("reports/kmeans_lineplt.png")
