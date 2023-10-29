import json
import sys
import pandas as pd
import matplotlib.pyplot as plt


def add_aon_lines(df, n, num_std=1):
    mean_line = df["times"].rolling(n).mean()
    std_values = num_std * df["times"].rolling(n).std()
    df[f"ao{n}"] = mean_line
    df[f"ao{n} + {num_std} std"] = mean_line + std_values
    df[f"ao{n} - {num_std} std"] = mean_line - std_values


with open(sys.argv[1], "r") as f:
    data = json.load(f)
data_3x3 = data["session1"]
times_3x3 = [row[0][1] / 1000 for row in data_3x3]
df = pd.DataFrame({"times": times_3x3})
add_aon_lines(df, 50)
df.plot()
plt.show()
