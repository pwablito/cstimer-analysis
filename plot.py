import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt


def add_aon_lines(df, n, num_std=1):
    mean_line = df["times"].rolling(n).mean()
    std_values = num_std * df["times"].rolling(n).std()
    df[f"ao{n}"] = mean_line
    df[f"ao{n} + {num_std} std"] = mean_line + std_values
    df[f"ao{n} - {num_std} std"] = mean_line - std_values


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <cstimer_export_file>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        data = json.load(f)
    sessions = {
        f"session{sess_num}": sess_props["name"]
        for sess_num, sess_props in json.loads(
            data["properties"]["sessionData"]
        ).items()
    }
    for session_id, session_name in sessions.items():
        data_session = data[session_id]
        times_session = [row[0][1] / 1000 for row in data_session]
        dates_session = [dt.fromtimestamp(row[-1]) for row in data_session]
        df = pd.DataFrame({"times": times_session}, index=dates_session)
        add_aon_lines(df, 100)
        plt.scatter(df.index, df['times'])
        df = df.drop(columns=["times"])
        for col in df.columns:
            plt.plot(df.index, df[col])
        plt.title(session_name)
        plt.savefig(f"{session_name}.png")
        plt.clf()


if __name__ == "__main__":
    main()
