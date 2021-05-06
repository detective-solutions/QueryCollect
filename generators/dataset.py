# import standard modules
import os
import string
import random

# import third party modules
import numpy as np
import pandas as pd

# import project related modules


class DataSetGenerator:
    """
    class that generates a dataset from a given pre set of values.

    example get data set with two columns of numerical values
    dsg = DataSetGenerator()
    data = dsg.generate(
        schema = [{"type": float}, {"type": str, "split": False}],
    )

    generate is the main function to use.

    """

    def __init__(self):

        # set a pre set of values to choose from when creating a new dataset
        self.data_path = "./server/static/data/names.csv"
        self.names = pd.read_csv(self.data_path, header=None).loc[:, 0].tolist()

        self.dtypes = {
            "<class 'str'>": ["", "Txt"],
            "<class 'int'>": ["", "Lat", "Lon", "Size", "HS", "Id", "Total", "Dim", "Distance", "Duration"],
            "<class 'float'>": ["", "Pct", "Weight", "Kg", "Ton", "Price", "Brutto", "Netto", "Estimate"]
        }

        self.word_map = [
            "Project", "Address", "Plant", "Screen",
            "Package", "Response", "Tech", "Technology", "Preview", "Connection"
        ]

        self.name_column_word_map = [
            "Name", "Customer", "Contact", "Consumer", "Manager", "Responsible", "Prospect"
        ]

        self.numbers = [""] + [str(x) for x in range(0, 10)]

    @classmethod
    def word_style(cls, word: str, style: int) -> str:
        """
        function returns in incoming word / string as lower, upper or as is string based on the selected style

        :param word: string to be modified
        :param style: integer between 0 - 2 (0: as is, 1: lower string, 2: upper string)
        :return: modified input word with selected style
        """
        if style == 0:
            return word
        elif style == 1:
            return word.lower()
        elif style == 2:
            return word.upper()

    def column_name_clean(self, column_name: str, d_type: str, names: bool = False) -> str:
        """
        function that removes leading digits from a column name.
        :param column_name: string input and column name to be cleaned
        :param d_type: what kind of values the column will hold - must be string and in pandas syntax e.g. <class 'str'>
        :param names: indicator whether the column holds name strings
        :return: a cleaned column or a new one in case the old one could not be cleaned (e.g. only digits)
        """

        try:
            if column_name != "":
                # remove numbers at the beginning of the column name
                # since most databases do not allow such column names
                while (len(column_name) > 0) & (column_name[0].isnumeric()):
                    column_name = column_name[1:]

                # check if the column name is an empty string and if so, run column name_generator
                if column_name == "":
                    return self.column_name_generator(d_type, names=names)

                else:
                    return column_name
            else:
                return self.column_name_generator(d_type, names=names)
        except IndexError:
            return self.column_name_generator(d_type, names=names)

    def column_name_generator(self, d_type: str, names: bool = False) -> str:
        """
        function that creates random column names for a given data type.

        :param d_type: pandas syntax like data type e.g. <class 'str'>
        :param names: indicator whether the column should contain name like values
        :return: str: random column name
        """

        # set some initial values randomly picked
        w_style = lambda: random.choice([0, 1, 2])
        concat_style = random.choice(["_", ""])
        column_length = random.choice(list(range(1, 2)))

        if names:
            words = random.choice(self.word_map) + random.choice(self.name_column_word_map)
        else:
            words = random.choices(self.word_map + self.numbers, k=column_length)

        # generate actual column name
        if type(words) == str:
            words = [words]

        column_name = f"{concat_style}".join(
            self.word_style(word, w_style()) for word in words
        ) + random.choice(self.dtypes[d_type])

        return self.column_name_clean(column_name, d_type=d_type, names=names)

    @classmethod
    def get_random_strings(cls, size: int = 5, split: bool = False) -> list:
        """
        function to create a list of random string values

        :param size: length of output list
        :param split: defines if the strings in the list should be splittable by a string like _
        :return: list with random string values
        """

        # ascii_letters, digits, punctuation whitespace
        lengths = list(range(2, 5))
        sections = 2 if split is True else 1
        letters = string.ascii_letters
        concat_value = random.choice(string.punctuation)

        # list to be outputted
        result_values = list()

        # create a little helper function to keep the other list comp. cleaner
        value = lambda: "".join(x for x in random.choices(list(letters), k=random.choice(lengths)))

        # create N values for the output list
        for _ in range(size):
            values = [value() for _ in range(1, sections + 1)]
            result_string = f"{concat_value}".join(v for v in values)
            result_values.append(result_string)

        return result_values

    def get_name_strings(self, size: int = 5, split: bool = False) -> list:
        """
        function to create a list of random string values containing names

        :param size: length of output list
        :param split: defines if the strings in the list should be splittable by a string like _
        :return: list with random string values
        """

        # define how many names one string holds and how they are concatenated
        sections = random.choice([2, 3]) if split else 1
        concat_value = random.choice(string.punctuation) if split else " "

        # output list
        result_values = list()

        # create N values for the output list
        for i in range(size):
            value = f"{concat_value}".join(x for x in random.choices(self.names, k=sections))
            result_values.append(value)

        return result_values

    def generate_string_column(self, size: int, split: bool = False, names: bool = False, duplicates: bool = True) -> list:
        """
        function that creates a list of random string values based on the given conditions

        :param size: size of the list array / amount of random string values
        :param split: indicator if a string value in the output list is intended to be split by a delimiter
        :param names: indicator if the random string values should be names
        :param duplicates: indicator if the list should contain duplicates
        :return: list array with random string values
        """
        if names:
            values = self.get_name_strings(size=size, split=split)
        else:
            values = self.get_random_strings(size=size, split=split)

        if duplicates:
            # pick a random index and replace another index with the value of the selected index
            indexes = list(range(size))
            to_copy_index = random.choice(indexes)
            to_copy_value = values[to_copy_index]
            indexes.remove(to_copy_index)
            to_replace = random.choices(indexes, k=random.choice([1, 2]))

            for i in to_replace:
                values[i] = to_copy_value

        return values

    @classmethod
    def generate_int_column(cls, size: int, *args, **kwargs) -> np.array:
        """
        create an array of integer values

        :param size: dimension of the array
        :param args: other arguments - not considered
        :param kwargs: other keyword arguments - not considered
        :return: numpy array of integer values between 0 and 100
        """
        return np.random.randint(100, size=size)

    @classmethod
    def generate_float_column(cls, size: int, *args, **kwargs) -> np.array:
        """
        create an array of float values

        :param size: dimension of the array
        :param args: other arguments - not considered
        :param kwargs: other keyword arguments - not considered
        :return: numpy array of float values between 0 and 100
        """
        return np.round(np.random.randn(size), 2)

    def generate(self, schema: list) -> pd.DataFrame:
        """
        main function to create a random dataset. It will create columns with random values based on the provided
        schema.
        :param schema: list of dicts e.g [{"type": float}]. For more information check the help function on the class
        :return: pandas dataframe according to the defined schema
        """

        # set output dict and create function mapping for data types
        data = dict()
        values = {
            "<class 'str'>": self.generate_string_column,
            "<class 'int'>": self.generate_int_column,
            "<class 'float'>": self.generate_float_column
        }

        # create a column for each column to be defined by the schema
        for column in schema:

            dtp = str(column["type"])
            name_column = column.get("names", False)
            to_split = column.get("split", False)
            duplicates = column.get("duplicates", False)
            column_name = self.column_name_generator(d_type=dtp, names=name_column)
            data[column_name] = values[dtp](5, split=to_split, names=name_column, duplicates=duplicates)

        return pd.DataFrame(data)