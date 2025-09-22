import pandas as pd #load pandas, nickname as pd

#load CSV into data frame
df = pd.read_csv("data/sample.csv")

#print the first few rows
print("Here are the first few rows:")
print(df.head())


import matplotlib.pyplot as plt #only importing pyplot from the big library matplotlib for plotting
from pathlib import Path        #The modern python way to handle files/folders

#Group the data by voltage and take the mean
#[] picks the column you care about within each group
grouped = df.groupby("voltage")["feature_width_um"].mean()

print("Average feature width at each voltage:")
print(grouped)



#Add Error Bars
import numpy as np

#group by voltage and compute mean, count, std
g = df.groupby("voltage")["feature_width_um"].agg(["mean", "count", "std"]).reset_index()
    #agg = aggregate(集団); applies 1 or more functions to each group
    #"std" shows how scattered the data is
    #"count" counts how many rows in the group
    #.reset_index: makes the index to regular column again (the index was voltage before)

#SEM = std / sqrt(n). SEM: "Standard error of the mean"; tells us how precise the mean is
g["sem"] = g["std"] / np.sqrt(g["count"])
print("\nSummary table (mean, n, SEM):")
print(g[["voltage", "mean", "count", "sem"]])


#Make sure an outputs/folder exists
Path("outputs").mkdir(exist_ok=True)    #Path("outputs") looks for a folder named outputs in my project
                                        #.mkdir() makes a directory(file) at this path
                                        #exist_ok=True -> The default is false but if file already exists, it ignores it and moves on

#Create a simple plot
plt.figure(figsize=(6,4))     #figure is a blank canvas for a plot
                              #figsize(6,4) means 6inches wide, 4inches tall
plt.errorbar(       #this plots with errorbar
    g["voltage"],       #x
    g["mean"],          #y = mean
    yerr=g["sem"],      #error bar height; yerr stands for "y errors"
    fmt="o-",           #circles connected by a line; fmt stands for "format string"
    capsize=3           #little caps on error bars
)
"""*OLD* plt.plot(grouped.index, grouped.values, marker = "o")       #plt.plot(x, y)plots points
                                                            #marker="o" puts a circle marker at each point """
plt.xlabel("voltage")
plt.ylabel("feature_width_um")
plt.title("Average feature width vs voltage")
plt.grid(True, alpha = 0.3)     #True means turn the grid on
                                #alpha = 0.3 makes the gridlines faint(not too distracting)

#Save it to a file and also show it
plt.savefig("outputs/voltage_vs_feature_width.png", bbox_inches="tight", dpi=150)
    #bbox_inches="tight" trims the whitespace around the plot
    #dpi=150 means "dots per inch"; controlls resolution
plt.show()  #pops up a window with the plot & closes when you dismiss the window

