import pandas as pd
import mygene
import os


if __name__ == "__main__":
    mg = mygene.MyGeneInfo()
    mg.set_caching(cache_db="/gpfs/home/isears1/scratch/mygenecache")
    data_path = "/gpfs/home/isears1/Repos/ecmo-rnaseq/outputs/subread/"
    merged_counts = pd.DataFrame()
    count_cols = list()

    for sample_id in os.listdir(data_path):
        if os.path.isdir(f"{data_path}/{sample_id}"):
            print(f"Analysing {sample_id}")
            counts_df = pd.read_csv(
                f"{data_path}/{sample_id}/counts.txt", sep="\t", skiprows=1
            )

            count_col_name = f"Count_{sample_id}"
            counts_df.columns = [*counts_df.columns[:-1], count_col_name]
            counts_df = counts_df[["Geneid", count_col_name]]
            count_cols.append(count_col_name)

            if len(merged_counts) == 0:  # Should only need to do this once...
                print(f"[*] Requesting bulk gene info...")
                bulk_info = mg.getgenes(
                    counts_df["Geneid"].to_list(),
                )

                bulk_dict = dict()
                for item in bulk_info:
                    query = item["query"]
                    bulk_dict[query] = dict()

                    if "name" in item:
                        bulk_dict[query]["name"] = item["name"]
                    else:
                        bulk_dict[query]["name"] = "na"

                    if "symbol" in item:
                        bulk_dict[query]["symbol"] = item["symbol"]
                    else:
                        bulk_dict[query]["symbol"] = "na"

            counts_df["Name"] = counts_df["Geneid"].apply(
                lambda gid: bulk_dict[gid]["name"]
            )
            counts_df["Symbol"] = counts_df["Geneid"].apply(
                lambda gid: bulk_dict[gid]["symbol"]
            )

            if len(merged_counts) == 0:  # For the first one
                merged_counts = counts_df
            else:
                print("[*] Performing join, this may take some time...")
                merged_counts = pd.merge(
                    merged_counts,
                    counts_df[["Geneid", count_col_name]],
                    how="left",
                    on="Geneid",
                )

    print("[*] Summing / norming and saving...")
    merged_counts["TotalCount"] = merged_counts[count_cols].sum(axis=1)

    # Counts per million (CPM) scaling
    for count_col in count_cols:
        s = merged_counts[count_col].sum()
        merged_counts[f"CPM_{count_col}"] = merged_counts[count_col].apply(
            lambda x: x / (s / 1e6)
        )

    merged_counts.to_csv(f"{data_path}/mergedcounts.csv", index=False)

    print("Top 10 merged counts:")
    top_10 = merged_counts.nlargest(10, "TotalCount")
    print(top_10)
