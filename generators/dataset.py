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
    The parameters allow to tune the dataset for a given purpose

    example get data set with two columns of numerical values
    dsg = DataSetGenerator()
    data = dsg.generate(
        schema = [{"type": float}, {"type": str, "split": False}],
        duplicates = False
    )

    """

    def __init__(self):
        self.data_path = "../server/static/data/names.csv"
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
        if style == 0:
            return word
        elif style == 1:
            return word.lower()
        elif style == 2:
            return word.upper()

    def column_name_clean(self, column_name: str, d_type: str, names: bool = False) -> str:
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

    def column_name_generator(self, d_type: str, names: bool = False):

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
    def get_random_strings(cls, size: int = 5, split: bool = False):
        # ascii_letters, digits, punctuation whitespace
        lengths = list(range(2, 5))
        sections = 2 if split else 1
        letters = string.ascii_letters + string.digits
        concat_value = random.choice(string.punctuation)
        result_values = list()

        for _ in range(size):
            result_string = ""
            for s in range(sections):
                value = "".join(random.choice(letters) for i in range(random.choice(lengths)))
                if (s < sections-1):
                    value += concat_value
                result_string += value

            result_values.append(result_string)

        return result_values

    def get_name_strings(self, size: int = 5, split: bool = False):
        sections = 2 if split else 1
        concat_value = random.choice(string.punctuation) if split else " "
        result_values = list()
        for i in range(size):
            value = f"{concat_value}".join(x for x in random.choices(self.names, k=sections))
            result_values.append(value)

        return result_values

    def generate_string_column(self, size: int, split: bool = False, names: bool = False):
        if names:
            return self.get_name_strings(size=size, split=split)
        else:
            return self.get_random_strings(size=size, split=split)

    @classmethod
    def generate_int_column(cls, size: int, *args, **kwargs):
        return np.random.randint(100, size=size)

    @classmethod
    def generate_float_column(cls, size: int, *args, **kwargs):
        return np.round(np.random.randn(size), 2)

    def generate(self, schema, duplicates: bool = False) -> pd.DataFrame:

        data = dict()
        values = {
            "<class 'str'>": self.generate_string_column,
            "<class 'int'>": self.generate_int_column,
            "<class 'float'>": self.generate_float_column
        }

        for column in schema:

            dtp = str(column["type"])
            name_column = column.get("names", False)
            to_split = column.get("names", False)
            column_name = self.column_name_generator(d_type=dtp, names=name_column)
            data[column_name] = values[dtp](5, split=to_split, names=name_column)

        return pd.DataFrame(data)