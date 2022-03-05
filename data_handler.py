import pandas as pd

class DataHandler:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.dates = self.data["date"].unique()
        self.groupby_companies_products = self.data.groupby(["company", "product"])
        self.index = self.generate_index()
        self.current_total = self.get_data(-1)["value"].sum()
        self.first_total = self.get_data(0)["value"].sum()
        self.delta_total = self.get_evolution(self.first_total, self.current_total)

    def generate_index(self):
        start_date = self.dates[0]
        end_date = self.dates[-1]
        index = pd.date_range(start=start_date, end=end_date, freq='M')
        return index

    def get_overall_df(self):
        groupby = self.groupby_companies_products
        data = {"date": [], "value": [], "product" : []}
        for _ in self.dates:
            for key, item in groupby:
                data["date"].append(_)
                id = key[1] + " (" + key[0] + ")"
                group = groupby.get_group(key)
                data["product"].append(id) 
                df = group[group["date"] == _]
                if len(df) == 0:
                    data["value"].append(0)
                else:
                    data["value"].append(df["value"].sum())
        return pd.DataFrame(data)
        

    def get_data(self, index):
        date = self.dates[index]
        return self.data[self.data["date"] == date]

    @staticmethod 
    def get_evolution(start_value, end_value):
        return "{:.2f}".format((end_value - start_value) / start_value * 100) + " %"


def main():
    data = pd.read_csv("./data_sample.csv")
    data_handler = DataHandler(data)
    df = data_handler.get_overall_df()
    print(df)
    

if __name__ == "__main__":
    main()