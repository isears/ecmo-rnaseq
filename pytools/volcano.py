import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # To reset the plot on loop

from scipy.stats import ttest_ind


def augment(col: str, pos_str: str = "Yes", neg_str: str = "No"):
    mc = pd.read_csv("outputs/dartmouthpipeline/mergedcounts.csv")
    mc = mc.set_index("Geneid")
    outcomes = pd.read_csv("data/outcomes.csv")

    pos_ids = outcomes[outcomes[col] == pos_str]["ID"].to_list()

    neg_ids = outcomes[outcomes[col] == neg_str]["ID"].to_list()

    assert len(pos_ids) + len(neg_ids) == len(outcomes)

    cpm_cols = [col for col in mc.columns if "CPM_" in col]
    pos_cpm_cols = [col for col in cpm_cols if col.split("_")[-1] in pos_ids]
    neg_cpm_cols = [col for col in cpm_cols if col.split("_")[-1] in neg_ids]
    pos_df = mc[pos_cpm_cols]
    neg_df = mc[neg_cpm_cols]

    pos_df["avg_exp"] = pos_df.mean(axis=1)
    neg_df["avg_exp"] = neg_df.mean(axis=1)

    mc["log2fold"] = np.log2(pos_df["avg_exp"] / neg_df["avg_exp"])

    def get_pval(row):
        _, pval = ttest_ind(row[pos_cpm_cols], row[neg_cpm_cols])
        return pval

    mc["pval"] = mc.apply(get_pval, axis=1)

    # TODO: Bonferonni threshold
    mc.to_csv("outputs/dartmouthpipeline/mergedcounts_augmented.csv")
    return mc


def make_plot(outcome: str):

    mc = pd.read_csv("outputs/dartmouthpipeline/mergedcounts_augmented.csv")

    # Need to filter out -inf, inf, nan
    mc_clean = mc

    # mc_clean = mc_clean[~mc_clean["pval"].isin([np.nan, np.inf, -np.inf])]
    # mc_clean = mc_clean[~mc_clean["log2fold"].isin([np.nan, np.inf, -np.inf])]
    mc_clean = mc_clean[~mc_clean["pval"].isna()]
    # Technically shouldn't be necessary after prev
    mc_clean = mc_clean[~mc_clean["log2fold"].isna()]

    # TODO: this is a HACK
    mc_clean["log2fold"] = mc_clean["log2fold"].replace({np.inf: 8, -np.inf: -8})

    bonferonni_threshold = -1 * np.log10(0.05 / len(mc))

    labels_df = mc_clean.nsmallest(10, columns="pval")
    # labels_df.apply(
    #     lambda row: plt.annotate(
    #         row["Geneid"], (row["log2fold"], -1 * np.log10(row["pval"])), fontsize=5
    #     ),
    #     axis=1,
    # )
    plt.scatter(mc_clean["log2fold"], -1 * np.log10(mc_clean["pval"]), s=1)
    plt.xlabel("Log2 Fold Change")
    plt.ylabel("-Log10(p_value)")
    plt.title(outcome)
    plt.axhline(y=bonferonni_threshold, color="r", linestyle="dotted")
    plt.savefig(f"reports/volcano_{outcome.replace(' ', '_')}.png")
    plt.clf()  # Clear after save in case running in loop

    print(f"Bonferonni Threshold: {bonferonni_threshold:.5f}")
    print(f"Top 10 by p value for {outcome}:")
    print(labels_df[["Geneid", "Symbol", "log2fold", "pval"]])
    labels_df[["Geneid", "Symbol", "log2fold", "pval"]].to_csv(
        f"reports/top10pval_{outcome.replace(' ', '_')}.csv", index=False
    )


if __name__ == "__main__":
    # outcome = "Neurological Complication (choice=Intracerebral hemorrhage (ICH))"
    outcomes_dict = {
        "Thrombosis": ("Yes", "No"),
        "Hemorrhage": ("Yes", "No"),
        "Gender": ("Male", "Female"),
        "Intracranial complication?": ("Yes", "No"),
    }

    for outcome, (pos_str, neg_str) in outcomes_dict.items():
        augment(outcome, pos_str, neg_str)
        make_plot(outcome)
