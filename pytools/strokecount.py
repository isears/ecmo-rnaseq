"""
Analyze expression of stroke-related genes identified here:
Theofilatos, K., Korfiati, A., Mavroudi, S. et al. 
Discovery of stroke-related blood biomarkers from gene expression network models. 
BMC Med Genomics 12, 118 (2019). https://doi.org/10.1186/s12920-019-0566-8
"""

import pandas as pd


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
    mc = pd.read_csv("./outputs/subread/mergedcounts.csv")
    filtered = mc[mc["Geneid"].isin(top_10_stroke_genes)]

    count_cols = [c for c in filtered.columns if "CPM_Count" in c]
    filtered["standard_deviation"] = filtered[count_cols].std()
    filtered["mean"] = filtered[count_cols].mean()

    zscore_cols = list()
    for cc in count_cols:
        id = cc.split("_")[-1]
        filtered[f"zscore_{id}"] = (filtered[cc] - filtered[cc].mean()) / filtered[
            cc
        ].std()

        zscore_cols.append(f"zscore_{id}")

    output = filtered[["Symbol"] + zscore_cols]
    output.to_csv("outputs/strokecounts.csv", index=False)
