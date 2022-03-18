import pandas as pd


df = pd.read_csv("Final_bik_dataset.tsv", sep='\t', encoding = "ISO-8859-1")

titles= df["Title"].tolist()
print(len(titles))