from pca2d import prep_for_pca
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    mc, labels = prep_for_pca()
    print(f"Original shape: {mc.values.shape}")

    pca = PCA(n_components=3, random_state=42)
    mc_pca = pca.fit_transform(mc)

    print(pca.explained_variance_ratio_)
    print(f"Shape after PCA: {mc_pca.shape}")

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(mc_pca[:, 0], mc_pca[:, 1], mc_pca[:, 2])

    ax.set_xlabel(f"PCA 1 ({pca.explained_variance_ratio_[0] * 100:.2f} %)")
    ax.set_ylabel(f"PCA 2 ({pca.explained_variance_ratio_[1] * 100:.2f} %)")
    ax.set_zlabel(f"PCA 3 ({pca.explained_variance_ratio_[2] * 100:.2f} %)")

    for idx, label in enumerate(labels):
        label = label.split("_")[-1]
        ax.text(mc_pca[idx, 0], mc_pca[idx, 1], mc_pca[idx, 2], label, None)

    ax.figure.tight_layout()
    plt.savefig("reports/pca3d_scatter.png")
