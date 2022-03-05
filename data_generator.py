import pandas as pd
import datetime as dt
import numpy as np
from dateutil.relativedelta import relativedelta

filepath = "./data_sample.csv"

def generate_dates():
    dates = []
    today = dt.date.today()
    for i in range(100):
        random_day = today - relativedelta(months=np.random.randint(0, 20))
        dates.append(random_day)
    return sorted(dates)

def generate_companies():
    company_names = ["Yes", "No", "Maybe"]
    companies = [company_names[np.random.randint(0, len(company_names))] for i in range(100)]
    return companies

def generate_products():
    product_names = ["Plan A", "Plan B", "Plan C", "Plan X"]
    products = [product_names[np.random.randint(0, len(product_names))] for i in range(100)]
    return products

def generate_types():
    type_names = ["Type A", "Type B", "Type C", "Type X", "Type Y", "Type Z"]
    types = [type_names[np.random.randint(0, len(type_names))] for i in range(100)]
    return types

def generate_values():
    values = [np.random.randint(0, 20000) for i in range(100)]
    return values

def generate_comments():
    comments = ["" for i in range(100)]
    return comments

def main():
    columns = ["date", "company", "product", "type", "value", "comment"]
    dates = generate_dates()
    companies = generate_companies()
    products = generate_products()
    types = generate_types()
    values = generate_values()
    comments = generate_comments()
    data = pd.DataFrame(list(zip(dates, companies, products, types, values, comments)), columns=columns)
    data.to_csv(filepath, index=False)

if __name__ == "__main__":
    main()