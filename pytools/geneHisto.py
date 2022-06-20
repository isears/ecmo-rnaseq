import pandas as pd


if __name__ == "__main__":
    mc = pd.read_csv("./outputs/subread/mergedcounts.csv")

    sample = "HaT-002"
    counts = mc[f"CPM_Count_{sample}"]
    # counts = counts.clip(upper=1000)
    ax = counts.plot.hist(bins=500, log=True)
    ax.get_figure().savefig(f"outputs/{sample}_hist.png")
