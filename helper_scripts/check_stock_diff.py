import pandas as pd


def stock_diff(previous_day, current_day):
    old_data = pd.read_excel(previous_day)
    new_data = pd.read_excel(current_day)

    diffences = pd.concat([old_data, new_data]).drop_duplicates(keep=False)
    diffences = diffences.sort_values(by=["Customer Part #", "Calendar Day"])

    return diffences
