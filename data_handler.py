import pandas as pd

def get_sum(dataframe: pd.DataFrame) -> float:
    return dataframe["Values"].sum()

def get_mean(dataframe: pd.DataFrame) -> float:
    return dataframe["Values"].mean()

class DataHandler:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.dates = self.data["Dates"].unique()
        self.groupby_overall = self.data.groupby(["Companies", "Products", "Types"])
        #self.df_dates = self.data.groupby(self.data["Dates"])
        #self.df_current = self.df_dates.last()

    def generate_index(self):
        start_date = self.dates[0]
        end_date = self.dates[-1]
        index = pd.date_range(start=start_date, end=end_date, freq='M')
        return index

    def get_overall_df(self):
        groupby = self.groupby_overall
        products = dict()
        for key, item in groupby:
            id = key[1] + " (" + key[0] + ")"
            products[id] = []
            group = groupby.get_group(key)
            for _ in self.dates:
                df = group[group["Dates"] == _]
                if len(df) == 0:
                    products[id].append(0)
                else:
                    products[id].append(df["Values"].values[0])        
        return pd.DataFrame(products, index=self.generate_index())

def main():
    data = pd.read_csv("./data_sample.csv")
    data_handler = DataHandler(data)
    for key, item in data_handler.groupby_overall:
        group = data_handler.groupby_overall.get_group(key)
    df = data_handler.get_overall_df()
    print(df)
    

if __name__ == "__main__":
    main()