from nfdi_kg.constants import DATA
import pandas as pd


def main():
    for path in DATA.glob("*.tsv"):
        pd.read_csv(path, sep='\t', dtype=str).to_csv(path, sep='\t', index=False)


if __name__ == '__main__':
    main()
