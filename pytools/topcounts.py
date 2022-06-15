import pandas as pd
import mygene
import os


if __name__ == "__main__":
    mg = mygene.MyGeneInfo()
    data_path = "/gpfs/home/isears1/Repos/ecmo-rnaseq/outputs/subread/"

    for item in os.listdir(data_path):
        if os.path.isdir(f"{data_path}/{item}"):
            print(f"\n====={item}====")
            counts_df = pd.read_csv(
                f"{data_path}/{item}/counts.txt", sep="\t", skiprows=1
            )
            counts_df.columns = [*counts_df.columns[:-1], "Count"]

            top_10 = counts_df.nlargest(10, "Count")[["Geneid", "Count"]]
            top_10["Name"] = top_10.apply(
                lambda row: mg.getgene(row["Geneid"], fields="name")["name"], axis=1
            )
            print(top_10[["Name", "Count"]])
