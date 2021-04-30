# import standard modules
import random

# import third party modules


# import project related modules


class DataSetGenerator:
    """
    class that generates a dataset from a given pre set of values.
    The parameters allow to tune the dataset for a given purpose

    """

    def __init__(self):
        pass

    def word_style(self, word: str, style: int) -> str:
        if style == 0:
            return word
        elif style == 1:
            return word.lower()
        elif style == 2:
            return word.upper()

    def column_name_clean(self, column_name: str) -> str:

        if column_name != "":
            # remove numbers at the beginning of the column name
            # since most databases do not allow such column names
            while (len(column_name) > 0) & (column_name[0].isnumeric()):
                column_name = column_name[1:]

            # check if the column name is an empty string and if so, run column name_generator
            if column_name == "":
                return self.column_name_generator()

            else:
                return column_name
        else:
            return self.column_name_generator()

    def column_name_generator(self):

        word_map = [
            "Project", "Name", "Address", "Customer", "Plant", "Lat", "Lon", "Screen",
            "Package", "Size", "Distance", "Price", "Weight", "Wgt", "Pct", "Txt", "Response",
            "Netto", "Tech", "HS", "Dim"
        ]

        numbers = [""] + [str(x) for x in range(0, 10)]

        w_style = lambda: random.choice([0, 1, 2])
        concat_style = random.choice(["_", ""])
        column_length = random.choice(list(range(1, 4)))
        words = random.choices(word_map + numbers, k=column_length)

        # generate actual column name
        column_name = f"{concat_style}".join(
            self.word_style(word, w_style()) for word in words
        )

        return self.column_name_clean(column_name)


    def generate(self, k_columns: int = 2, duplicates: bool = False, split_column: bool = False):
