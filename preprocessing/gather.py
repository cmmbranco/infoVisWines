import pandas as pd


dtframe = pd.read_csv("../winemag-data-130k-v2.csv")

f = open("descriptioncorpus.txt", "w")

for index, row in dtframe.iterrows():
    f.write(row.description + "\n")

f.close()
