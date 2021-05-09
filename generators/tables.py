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
    """
    class creates an input table and an output table for pre defined query types based on randomly generated data sets

    -- see all available options:
        qt = QueryTable()
        qt.options()  - shows filter type with related number

    -- generate an input and related output dataset for a given query_type:
        qt = QueryTable()
        qt.query_task(1) - 0 - 11 is available

    """

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
    def rand_bool(cls) -> bool:
        """
        select randomly between True and False
        :return: bool True or False
        """
        return random.choice([False, True])
    
    @classmethod
    def rand_num(cls):
        """
        selects randomly between float and int type
        :return: type float or int
        """
        return random.choice([float, int])

    @classmethod
    def create_missing(cls, values: list) -> list:
        """
        function to create missing values in a given list

        :param values: list of values
        :return: input list with NaN at random locations
        """

        # get indexes to be replaces
        idx_to_replace = random.choices(list(range(5)), k=random.choice(list(range(1, 4))))

        # replace values at selected indexes
        for ix in idx_to_replace:
            values[ix] = np.nan

        return values

    def row_filter(self) -> tuple:
        """
        provides and example where the data set is filtered on one value
        :return tuple with input and output dataset as list of records
        """

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

        # create an output dataset
        output_data = input_data.loc[:, columns].rename(columns={column_to_select: new_name})

        return input_data.to_dict("records"), output_data.to_dict("records")

    def select_columns(self) -> tuple:
        """
        provides an example with a dataset to be reduced in column size
        :return tuple with input and output dataset as list of records
        """

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

        # create output dataset
        output_data = input_data.loc[:, columns_to_select]

        return input_data.to_dict("records"), output_data.to_dict("records")

    def rename_column(self) -> tuple:
        """
        provides an example with a dataset where a column is renamed
        :return tuple with input and output dataset as list of records
        """

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": self.rand_num()},
                {"type": self.rand_num()}
            ],
        )

        # get a list of all available columns
        columns = input_data.columns.tolist()

        # select a random column of both and select
        column_to_select = random.choice(columns)
        new_name = self.data_generator.column_name_generator(d_type="<class 'int'>")

        # keep the order of the input table by selection the columns in the right order
        input_data = input_data.loc[:, columns]

        # create a map with column namings and create the output dataset with the renamed column
        rename_map = dict(zip(columns, columns))
        rename_map[column_to_select] = new_name
        output_data = input_data.loc[:, columns].rename(columns=rename_map)

        # create a new order
        index_of_renamed = columns.index(column_to_select)
        columns[index_of_renamed] = new_name

        return input_data.to_dict("records"), output_data.loc[:, columns].to_dict("records")

    def row_count(self) -> tuple:
        """
        provides two data sets where the output dataset is an aggregated value count of one column
        from the input dataset
        :return tuple with input and output dataset as list of records
        """

        # generate a random dataset with two numerical and one string column
        input_data = self.data_generator.generate(
            schema=[
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
                {"type": str, "split": self.rand_bool(), "names": self.rand_bool()},
            ],
        )

        # get random entries to be duplicated, so some row counts are larger than one
        indexes = random.choices(list(range(5)), k=random.choice([1, 2]))
        not_selected = list(set(list(range(5))) - set(indexes))

        # duplicate rows in input dataset
        input_data = (input_data.iloc[not_selected]
                      .append(input_data.iloc[indexes].copy())
                      .append(input_data.iloc[indexes].copy())
                      ).reset_index(drop=True)

        # get random column to be counted in values
        column_to_count = random.choice(input_data.columns.tolist())

        # create the output dataset by counting the values of the randomly picked column
        output_data = input_data.loc[:, [column_to_count]][column_to_count].value_counts().reset_index()
        output_data.rename(columns={"index": column_to_count, column_to_count: "count"}, inplace=True)

        return input_data.to_dict("records"), output_data.to_dict("records")

    def split_column(self) -> tuple:
        """
        creates a dataset with a column to be split by a random delimiter and an output table doing so and expanding the
        input table
        :return tuple with input and output dataset as list of records
        """

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

        # split the picked columns and expand the series
        splits = input_data[column_name].str.split(split_value, n=-1, expand=True)

        # create a new column for each expand in splits
        output_data = input_data.copy()
        for ix in range(splits.shape[1]):
            output_data[f"{column_name}_{ix}"] = splits[ix]

        return input_data.to_dict("records"), output_data.to_dict("records")

    def group_data(self) -> tuple:
        """
        generate a random dataset with two numerical and one string column
        :return tuple with input and output dataset as list of records
        """

        string_schema = [
            {"type": str, "split": False, "names": self.rand_bool(), "duplicates": True}
            for _ in range(random.choice([1, 2]))
        ]

        numerical_schema = [
            {"type": int} for _ in range(random.choice([1, 2]))
        ]

        input_data = self.data_generator.generate(
            schema=string_schema + numerical_schema
        )

        # get the string column we will group by
        d_types = list(zip(input_data.columns.tolist(), input_data.dtypes.tolist()))
        string_columns = [x[0] for x in d_types if str(x[1]) == "object"]
        int_columns = list(set(input_data.columns.tolist()) - set(string_columns))

        # get randomly an action to be executed by the group by for each column one
        actions = random.choices(["max", "min", "sum"], k=len(int_columns))
        aggregates = dict(zip(int_columns, actions))

        # create a renaming for the output columns so the user can easily understand which action was taken
        renaming = dict()
        for i in range(len(int_columns)):
            int_column = int_columns[i]
            renaming[int_column] = f"{int_columns[i]}_{aggregates[int_columns[i]]}"

        # create the aggregation and the output table
        output_data = input_data.groupby(string_columns).agg(aggregates).reset_index()
        output_data = output_data.rename(columns=renaming)

        return input_data.to_dict("records"), output_data.to_dict("records")

    def sort_data(self) -> tuple:
        """
        function to create and random input table and sort it by a random column in desc or ascending order.
        :return tuple with input and output dataset as list of records
        """

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
        numerical_column = [x[0] for x in d_types if str(x[1]) in ("float64", "int32")][0]

        # create the output dataset
        output_data = input_data.copy()
        output_data = output_data.sort_values(by=numerical_column, ascending=self.rand_bool())

        return input_data.to_dict("records"), output_data.to_dict("records")

    def drop_columns(self) -> tuple:
        """
         function that creates an input and output dataset where the output dataset drops some columns randomly
         :return tuple with input and output dataset as list of records
        """

        # create baseline dataset
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

    def fill_missing_values(self) -> tuple:
        """
        creates an input and an output dataset where the input dataset contains some missing values which
        will be filled in the output dataset
        :return tuple with input and output dataset as list of records
        """

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

    def drop_duplicates(self) -> tuple:
        """
        creates an input and output dataset where the input dataset holds some duplicated rows which will be dropped
        in the output dataset
        :return tuple with input and output dataset as list of records
        """

        # create initial input dataset
        input_data = self.data_generator.generate(
            schema=[
                       {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}] + [
                       {"type": self.rand_num()} for _ in range(random.choice([1, 2]))
                   ],
        )

        # get random entries to be duplicated in the input dataset
        indexes = random.choices(list(range(5)), k=random.choice([1, 2]))
        not_selected = list(set(list(range(5))) - set(indexes))

        # create duplicates at the randomly selected indexes
        input_data = (input_data.iloc[not_selected]
                      .append(input_data.iloc[indexes].copy())
                      .append(input_data.iloc[indexes].copy())
                      ).reset_index(drop=True)

        # drop duplicates for an output dataset
        output_data = input_data.drop_duplicates()
        return input_data.to_dict("records"), output_data.to_dict("records")

    def drop_na(self):
        """
        provides an input and output dataset where the output dataset dropped all missing values
        :return tuple with input and output dataset as list of records
        """

        # create input dataset
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

    def calculate_column(self) -> tuple:
        """
        creates an input and an output dataset where the output dataset holds an additional column which is
        calculated version of two random columns from the input dataframe. It might be a add, subtract, multiply or
        divide of two numerical columns or a concat of two string columns

        :return tuple with input and output dataset as list of records
        """

        string_columns = [
            {"type": str, "split": False, "names": self.rand_bool(), "duplicates": False}
            for _ in range(random.choice([2, 3]))
        ]

        numerical_columns = [
            {"type": self.rand_num()} for _ in range(random.choice([2, 3]))
        ]

        # create a dataset with either string columns or numerical columns
        input_data = self.data_generator.generate(
            schema=random.choice([string_columns, numerical_columns])
        )

        # set possible operators to pick from
        operations = {
            "add": operator.add,
            "subtract": operator.sub,
            "multiply": operator.mul,
            "divide": operator.truediv
        }

        # list all data types of the columns to know which operation path to pick
        d_types = list(zip(input_data.columns.tolist(), input_data.dtypes.tolist()))

        # if all string columns than create a concat
        if all([str(x[1]) == "object" for x in d_types]):
            # only option for string is concat. substrings are not included yet
            concat_style = random.choice(["_", "-", " "])
            columns = random.sample(input_data.columns.tolist(), k=2)
            output_data = input_data.loc[:, columns]
            output_data["combination"] = output_data[columns[0]] + concat_style + output_data[columns[1]]

        else:
            # if numerical columns than sample - without replacement from the columns
            columns = random.sample(input_data.columns.tolist(), k=2)
            output_data = input_data.loc[:, columns]

            # choose a random operation and create a new column
            func = random.choice(["add", "subtract", "multiply", "divide"])
            new_column = f"{random.choice(columns)}_{func}"
            output_data[new_column] = operations[func](output_data[columns[0]], output_data[columns[1]])

        return input_data.to_dict("records"), output_data.to_dict("records")

    @classmethod
    def options(cls) -> None:
        """function prints all available q_types and their filter names"""

        options = {
            "row_filter": 0,
            "select_columns": 1,
            "rename_column": 2,
            "row_count": 3,
            "split_column": 4,
            "group_data": 5,
            "sort_data": 6,
            "drop_columns": 7,
            "fill_missing_values": 8,
            "drop_duplicates": 9,
            "drop_na": 10,
            "calculate_column": 11
        }

        for k, v in options.items():
            print(f"filter type '{k}' is query_type argument {v}")

    def query_task(self, q_type: int) -> tuple:
        """
        main function to create random input and output tables
        :param q_type: int defining which pre defined filter type will be created (0 - 11) for more information call options
        :return: tuple with lists of records for input, output
        """
        return self.query_type[q_type]()