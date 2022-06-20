from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def prep_for_pca():
    mc = pd.read_csv(
        "/gpfs/home/isears1/Repos/ecmo-rnaseq/outputs/subread/mergedcounts.csv"
    )

    kept_cols = [col for col in mc.columns if "CPM_" in col]

    # x axis: gene expression lvls (counts per million)
    # y axis: patients
    mc = mc.set_index("Geneid")
    mc = mc[kept_cols]
    mc = mc.T
    return mc, kept_cols


if __name__ == "__main__":
    mc, labels = prep_for_pca()
    print(f"Original shape: {mc.values.shape}")

    pca = PCA(n_components=2, random_state=42)
    mc_pca = pca.fit_transform(mc)

    print(pca.explained_variance_ratio_)
    print(f"Shape after PCA: {mc_pca.shape}")

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(mc_pca[:, 0], mc_pca[:, 1])

    ax.set_xlabel(f"PCA 1 ({pca.explained_variance_ratio_[0] * 100:.2f} %)")
    ax.set_ylabel(f"PCA 2 ({pca.explained_variance_ratio_[1] * 100:.2f} %)")

    for idx, label in enumerate(labels):
        label = label.split("_")[-1]
        ax.annotate(label, (mc_pca[idx, 0], mc_pca[idx, 1]))
        # ax.text(mc_pca[idx, 0], mc_pca[idx, 1], mc_pca[idx, 2], label, None)

    ax.figure.tight_layout()
    plt.savefig("reports/pca2d_scatter.png")
