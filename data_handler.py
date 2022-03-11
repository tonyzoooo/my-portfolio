import pandas as pd
from dataclasses import dataclass

class DataHandler:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.dates = self.data["date"].unique()
        self.data_structure = None
        self.index = self.generate_index()

    def generate_index(self):
        start_date = self.dates[0]
        end_date = self.dates[-1]
        index = pd.date_range(start=start_date, end=end_date, freq='M')
        return index

    def get_overall_df(self):
        groupby = self.data.groupby(["company", "product"])
        data = {"date": [], "value": [], "product" : []}
        for _ in self.dates:
            for key, item in groupby:
                group = groupby.get_group(key)
                df = group[group["date"] == _]
                if len(df) != 0:
                    data["date"].append(_)
                    id = key[1] + " (" + key[0] + ")"
                    data["product"].append(id)
                    data["value"].append(df["value"].sum())
        df = pd.DataFrame(data)
        self.set_data(df)
        return df

    def get_type_df(self):
        groupby = self.data.groupby(["type"])
        data = {"value": [], "type": []}
        date = self.dates[-1]
        for key, item in groupby:
            group = groupby.get_group(key)
            df = group[group["date"] == date]
            if len(df) != 0:
                data["value"].append(df["value"].sum())
                data["type"].append(df["type"].values[0])
        return pd.DataFrame(data)


        
    def select_data_by_date(self, index, data):
        date = self.dates[index]
        return data[data["date"] == date]


    def set_data(self, dataframe):
        current_month = self.dates[-1]
        current_total = dataframe[dataframe["date"] == current_month]["value"].sum()
        last_month = self.dates[-2]
        last_total = dataframe[dataframe["date"] == last_month]["value"].sum()
        first_month = self.dates[0]
        first_total = dataframe[dataframe["date"] == first_month]["value"].sum()
        data = Data(current_month, current_total, last_month, last_total, first_month, first_total)
        self.data_structure = data



class DataFormatter:
    def __init__(self, currency = "€") -> None:
        self.currency = currency

    @staticmethod
    def get_evolution_description(string, start_value) -> str:
        return string + " (" + start_value + ")"

    @staticmethod 
    def get_evolution_percent(start_value, end_value) -> str:
        return "{:.2f}".format((end_value - start_value) / start_value * 100) + " %"

    def get_evolution_float(self, start_value, end_value) -> str:
        return str(end_value - start_value) + " " + self.currency

    def get_current_total(self, value):
        return str(value) + self.currency


@dataclass
class Data:
    current_month: pd.DataFrame = None
    current_total: float = 0
    last_month: pd.DataFrame = None
    last_total: float = 0
    first_month: pd.DataFrame = None
    first_total: float = 0



def main():
    data = pd.read_csv("./data_sample.csv")
    data_handler = DataHandler(data)
    df = data_handler.get_overall_df()
    print(df)
    

if __name__ == "__main__":
    main()