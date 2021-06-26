import os
import json
from collect_data import collect_data
from tqdm import tqdm


def main():

    if os.path.isfile("data.jsonlines"):
        os.remove("data.jsonlines")

    tickers = list()
    with open("tickers.jsonlines", "r") as f:
        content = f.readline()
        while content != '':
            content = json.loads(content)
            tickers.append(content["ticker"])
            content = f.readline()

    with tqdm(total=len(tickers)) as pbar:
        for ticker in tickers:
            collect_data(ticker)
            pbar.update(1)


if __name__ == "__main__":
    main()