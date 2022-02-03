import os
import pandas as pd
import matplotlib.pyplot as plt

"""
This module was used for evaluating and comparing optimizers for the final report
For using the DSS, or simulating a day, this file is irrelevant 
"""


path_parent = os.path.dirname(os. getcwd())
os.chdir(path_parent)
path = os.getcwd()
print(path)
df=pd.read_csv(path+'/data/Output/result.csv')
titles = df['Unnamed: 0']
plt.figure(figsize=(22, 26))
# fig, axes = plt.subplots(nrows=2, ncols=6, figsize=(20, 8), dpi=100)
for row, typ in enumerate(['Orders delivered', 'Num_delayed_orders', 'Percentage delayed orders', 'Total delay time', \
                           'Avg. delay', 'Total waiting time', 'Avg. waiting time', 'kms driven']):
    cols = []
    for col in df.columns:
        if col.startswith(typ):
            cols.append(col)
    temp = df[cols]

    for i in range(1, 7, 1):
        plt.subplot(8, 6, row * 6 + i)
        # x ; height ,color="blue", width=0.8
        x = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'Paris']
        tit = titles[i - 1]
        p1 = plt.bar(x, height=temp.iloc[i - 1, :], width=0.5)
        # plt.title(typ +'-'+ tit)
        if row == 0:
            plt.title(tit)
        if i == 1:
            plt.ylabel(typ)

plt.savefig(path+'/data/Output/plot.png')
#plt.show()