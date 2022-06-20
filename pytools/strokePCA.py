from sklearn.decomposition import PCA
from pca2d import prep_for_pca
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    mc, labels = prep_for_pca()

    # Filter down to only stroke-related genes
    mc = mc.filter(items=top_10_stroke_genes)
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
    plt.savefig("reports/stroke_pca2d_scatter.png")
