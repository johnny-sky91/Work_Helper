import pandas as pd


def set_second_row_as_headers(df):
    df.columns = df.iloc[0]
    df = df[2:]
    df.reset_index(drop=True, inplace=True)
    return df


class CheckDiffrences:
    def __init__(self, old_file_path: str, new_file_path: str, data_type: str):
        self.old_file_path = old_file_path
        self.new_file_path = new_file_path
        self.data_type = data_type
        self.raw_old_data = None
        self.raw_new_data = None
        self.old_data = None
        self.new_data = None
        self.diffences = None

    def _read_file(self):
        self.raw_old_data = pd.read_excel(self.old_file_path)
        self.raw_new_data = pd.read_excel(self.new_file_path)
        if self.data_type == "po":
            set_second_row_as_headers(df=self.raw_old_data)
            set_second_row_as_headers(df=self.raw_new_data)

    def _filter_data(self):
        if self.data_type == "stock":
            self.old_data = self.raw_old_data.drop(columns=["Calendar Day"])
            self.new_data = self.raw_new_data.drop(columns=["Calendar Day"])
        elif self.data_type == "po":
            self.old_data = self.raw_old_data[
                self.raw_old_data["Confirmation Type"] == "SSD"
            ]
            self.new_data = self.raw_new_data[
                self.raw_new_data["Confirmation Type"] == "SSD"
            ]
            ready_list = ["Customer Part #", "MAD Date", "SSD Qty", "Customer PO #"]
            self.old_data = self.old_data[ready_list]
            self.new_data = self.new_data[ready_list]

    def _get_diffrences(self):
        self.diffences = (
            pd.concat([self.old_data, self.new_data])
            .drop_duplicates(keep=False)
            .sort_index()
        )

    def __call__(self):
        self._read_file()
        self._filter_data()
        self._get_diffrences()
        return self.raw_old_data, self.raw_new_data, self.diffences
