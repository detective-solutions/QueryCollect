# import standard modules
import random

# import third party modules
import numpy as np
import pandas as pd

# import project related modules
from generators.dataset import DataSetGenerator


class QueryTable:

    def __init__(self):
        self.data_generator = DataSetGenerator()
        self.query_type = {
            0: self.row_filter,
            1: self.select_columns,
            2: self.rename_column,
            3: self.row_count,
            4: self.split_column,
            5: self.group_data,
            6: self.sort_data,
            7: self.drop_columns,
            8: self.fill_missing_values,
            9: self.drop_duplicates,
            10: self.drop_na,
            11: self.calculate_column
        }

    def row_filter(self):
        """provide and example where the data set is filtered on one or multiple values"""

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": str, "split": random.choice([True, False]), "names": random.choice([True, False])},
                {"type": random.choice([float, int])},
                {"type": random.choice([float, int])}
            ],
            duplicates=False
        )

        # select a random column of both and select
        columns = input_data.columns.tolist()
        column_to_select = random.choice(columns)
        new_name = self.data_generator.column_name_generator(d_type="<class 'int'>")

        output_data = input_data.loc[:, columns].rename(columns={column_to_select: new_name})
        return input_data.to_dict("records"), output_data.to_dict("records")

    def select_columns(self):
        """provides an example with a dataset to be reduced in column size"""

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": random.choice([float, int])},
                {"type": str, "split": random.choice([True, False]), "names": random.choice([True, False])},
                {"type": random.choice([float, int])}
            ],
            duplicates=False
        )

        # select a random column of both and select
        k = random.choice([1, 2])
        columns_to_select = random.choices(input_data.columns.tolist(), k=k)
        output_data = input_data.loc[:, columns_to_select]
        return input_data.to_dict("records"), output_data.to_dict("records")

    def rename_column(self):
        """provides an example with a dataset to be renamed"""

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": random.choice([float, int])},
                {"type": random.choice([float, int])}
            ],
            duplicates=False
        )

        columns = input_data.columns.tolist()

        # select a random column of both and select
        column_to_select = random.choice(columns)
        new_name = self.data_generator.column_name_generator(d_type="<class 'int'>")

        # keep the order of the input table by selection the columns in the right order
        input_data = input_data.loc[:, columns]

        rename_map = dict(zip(columns, columns))
        rename_map[column_to_select] = new_name

        output_data = input_data.loc[:, columns].rename(columns=rename_map)
        return input_data.to_dict("records"), output_data.to_dict("records")

    def row_count(self):
        pass

    def split_column(self):
        pass

    def group_data(self):
        pass

    def sort_data(self):
        pass

    def drop_columns(self):
        pass

    def fill_missing_values(self):
        pass

    def drop_duplicates(self):
        pass

    def drop_na(self):
        pass

    def calculate_column(self):
        pass

    def query_task(self, q_type: int):
        return self.query_type[q_type]()
