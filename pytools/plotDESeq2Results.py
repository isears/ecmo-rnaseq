import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    dres = pd.read_csv("outputs/deseq2_results.csv", index_col=0)
    dres = dres[~dres["padj"].isna()]

    print(dres)

    plt.scatter(dres["log2FoldChange"], -1 * np.log10(dres["padj"]), s=1)
    plt.xlabel("Log2 Fold Change")
    plt.ylabel("-Log10(p_value)")
    plt.title("Gender")
    plt.axhline(y=-1 * np.log10(0.05), color="r", linestyle="dotted")
    plt.savefig(f"reports/volcano_Gender.png")
    plt.clf()  # Clear after save in case running in loop
