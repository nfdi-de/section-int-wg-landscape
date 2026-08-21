import pandas as pd

from nfdi_kg.constants import DATA


def main():
    for path in DATA.glob("*.tsv"):
        df = pd.read_csv(path, sep="\t", dtype=str)
        for column in df.columns:
            df[column] = df[column].map(lambda s: s.strip(), na_action="ignore")
        df.to_csv(path, sep="\t", index=False)


if __name__ == "__main__":
    main()
