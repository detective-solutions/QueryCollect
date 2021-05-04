# import standard modules
import random
import string
import operator

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

    @classmethod
    def rand_bool(cls):
        return random.choice([False, True])
    
    @classmethod
    def rand_num(cls):
        return random.choice([float, int])

    @classmethod
    def create_missing(cls, values: list) -> list:
        idx_to_replace = random.choices(list(range(5)), k=random.choice(list(range(1, 4))))
        for ix in idx_to_replace:
            values[ix] = np.nan
        return values

    def row_filter(self):
        """provide and example where the data set is filtered on one or multiple values"""

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
                {"type": self.rand_num()},
                {"type": self.rand_num()}
            ],
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
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
                {"type": random.choice([float, int])}
            ],
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
                {"type": self.rand_num()},
                {"type": self.rand_num()}
            ],
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

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
            ],
        )

        # get random column
        column_to_count = random.choice(input_data.columns.tolist())
        output_data = input_data.loc[:, [column_to_count]][column_to_count].value_counts().reset_index()

        # TODO: Rename columns, order columns and duplicate rows so some counts are more than one

        return input_data.to_dict("records"), output_data.to_dict("records")

    def split_column(self):

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": str, "split": True, "names": self.rand_bool()},
            ],
        )

        # get the split value by counting by identifying the punctuation symbol - same for the entire column
        column_name = input_data.columns.tolist()[0]
        example = input_data[column_name].tolist()[0]
        split_value = [x for x in example if x in list(string.punctuation)][0]

        splits = input_data[column_name].str.split(split_value, n=-1, expand=True)
        output_data = input_data.copy()
        for ix in range(splits.shape[1]):
            output_data[f"{column_name}_{ix}"] = splits[ix]

        return input_data.to_dict("records"), output_data.to_dict("records")

    def group_data(self):

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": str, "split": False, "names": self.rand_bool(), "duplicates": True}
                for _ in range(random.choice([1, 2]))

            ] + [
                {"type": int}
                for _ in range(random.choice([1, 2]))
            ],
        )

        # get the string column we will group by
        d_types = list(zip(input_data.columns.tolist(), input_data.dtypes.tolist()))
        string_columns = [x[0] for x in d_types if str(x[1]) == "object"]
        int_columns = list(set(input_data.columns.tolist()) - set(string_columns))

        actions = random.choices(["max", "min", "sum"], k=len(int_columns))
        aggregates = dict(zip(int_columns, actions))

        renaming = dict()
        for i in range(len(int_columns)):
            int_column = int_columns[i]
            renaming[int_column] = f"{int_columns[i]}_{aggregates[int_columns[i]]}"

        output_data = input_data.groupby(string_columns).agg(aggregates).reset_index()
        output_data = output_data.rename(columns=renaming)

        return input_data.to_dict("records"), output_data.to_dict("records")

    def sort_data(self):

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                       {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}
                       for _ in range(random.choice([1, 2]))
                   ] + [
                       {"type": self.rand_num()}
                   ],
        )

        # get numerical column to sort by
        d_types = list(zip(input_data.columns.tolist(), input_data.dtypes.tolist()))
        numerical_column = [x[0] for x in d_types if str(x[1]) in ("float32", "int32")][0]

        output_data = input_data.copy()
        output_data = output_data.sort_values(by=numerical_column, ascending=self.rand_bool())

        return input_data.to_dict("records"), output_data.to_dict("records")

    def drop_columns(self):

        input_data = self.data_generator.generate(
            schema=[
                       {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}] + [
                       {"type": self.rand_num()} for _ in range(random.choice([1, 2]))
            ],
        )

        # get a random column to drop
        to_drop = random.choice(input_data.columns.tolist())
        output_data = input_data.drop(to_drop, axis=1)
        return input_data.to_dict("records"), output_data.to_dict("records")

    def fill_missing_values(self):

        input_data = self.data_generator.generate(
            schema=[
                       {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}] + [
                       {"type": self.rand_num()} for _ in range(random.choice([1, 2]))
                   ],
        )

        # select randomly a column to enter missing values
        na_column = random.choice(input_data.columns.tolist())
        input_data[na_column] = self.create_missing(input_data[na_column].tolist())

        # get the data type of the column
        d_type = str(input_data[na_column].dtype)

        # select a random fill value
        fill_values = {"float64": [.0], "int32": [0], "object": ["#", "no_value"]}
        output_data = input_data.fillna(random.choice(fill_values[d_type]))

        return input_data.to_dict("records"), output_data.to_dict("records")

    def drop_duplicates(self):
        input_data = self.data_generator.generate(
            schema=[
                       {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}] + [
                       {"type": self.rand_num()} for _ in range(random.choice([1, 2]))
                   ],
        )

        # get random entries
        indexes = random.choices(list(range(5)), k=random.choice([1, 2]))
        not_selected = list(set(list(range(5))) - set(indexes))

        input_data = (input_data.iloc[not_selected]
                      .append(input_data.iloc[indexes].copy())
                      .append(input_data.iloc[indexes].copy())
                      ).reset_index(drop=True)

        output_data = input_data.drop_duplicates()
        return input_data.to_dict("records"), output_data.to_dict("records")

    def drop_na(self):
        input_data = self.data_generator.generate(
            schema=[
                       {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}] + [
                       {"type": self.rand_num()} for _ in range(random.choice([1, 2]))
                   ],
        )

        # select randomly a column to enter missing values
        na_column = random.choice(input_data.columns.tolist())
        input_data[na_column] = self.create_missing(input_data[na_column].tolist())

        output_data = input_data.dropna()
        return input_data.to_dict("records"), output_data.to_dict("records")

    def calculate_column(self):

        string_columns = [
            {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}
            for _ in range(random.choice([2, 3]))
        ]

        numerical_columns = [
            {"type": self.rand_num()} for _ in range(random.choice([2, 3]))
        ]

        input_data = self.data_generator.generate(
            schema=random.choice([string_columns, numerical_columns])
        )

        operations = {
            "add": operator.add,
            "subtract": operator.sub,
            "multiply": operator.mul,
            "divide": operator.truediv
        }

        d_types = list(zip(input_data.columns.tolist(), input_data.dtypes.tolist()))

        if all([str(x[1]) == "object" for x in d_types]):
            # only option for string is concat. substrings are not included yet
            concat_style = random.choice(["_", "-", " "])
            columns = random.sample(input_data.columns.tolist(), k=2)
            output_data = input_data.loc[:, columns]
            output_data["combination"] = output_data[columns[0]] + concat_style + output_data[columns[1]]

        else:
            columns = random.sample(input_data.columns.tolist(), k=2)
            output_data = input_data.loc[:, columns]
            func = random.choice(["add", "subtract", "multiply", "divide"])
            new_column = f"{random.choice(columns)}_{func}"
            output_data[new_column] = operations[func](output_data[columns[0]], output_data[columns[1]])

        return input_data.to_dict("records"), output_data.to_dict("records")

    def query_task(self, q_type: int):
        print(q_type)
        return self.query_type[q_type]()