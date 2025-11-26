

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any
from pandas import DataFrame, read_excel, read_json, read_csv
from json import dumps
from io import StringIO

import functools
import warnings

def experimental(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"Esta versão do método '{func.__name__}' é experimental e pode ser alterado "
            "ou removido no futuro. Use por sua conta e risco.",
            FutureWarning,
            stacklevel=2
        )
        return func(*args, **kwargs)
    return wrapper

class ConverterType(Enum):
    JSON = 'json'
    XLSX = 'xlsx'
    CSV = 'csv'

class Converter(ABC):

    def __init__(self, filename: str = None, data: DataFrame = None) -> None:
        self.filename = filename
        self.data = data

        if self.filename is None and self.data is None:
            raise ValueError("É necessário fornecer um filename ou um DataFrame.")
        
        if self.filename is not None and self.data is not None:
            raise ValueError("Forneça apenas um entre filename ou DataFrame, não ambos.")

    @abstractmethod
    def render(self) -> str: ...

    def from_dataframe(self, df: DataFrame) -> None:
        n_columns = 'c' * len(df.columns)
        header = ' & \n'.join(['\\textbf{' + i + '}' for i in df.columns]) + ' \\\\'
        lines = []
        for i in df.values:
            line = " & ".join([str(j) if j else '--' for j in i]) + ' \\\\\n'
            lines.append(line)

        table_part1 = '''
\\begin{table}[h!]
\\centering
\\rowcolors{2}{gray!15}{white}
\\scalebox{0.8}{%
\\resizebox{\\textwidth}{!}{%
\\begin{tabular}{''' + n_columns + '''}
\\midrule
'''

        table_part2 = '''
\\midrule
\\end{tabular}}}
\\end{table}
'''
        values = ''.join(lines)
        values = values.rstrip('\n')
        header = header.replace('%', '\\%')
        values = values.replace('%', '\\%')

        return table_part1 + header + '\n\\midrule\n' + values + table_part2


class Reader:

    def converter(self, type: ConverterType, filename: str = None, data: List|Dict|List[Dict]|DataFrame = None) -> Converter:
        if type == ConverterType.JSON:
            return JsonConverter(filename, data)
        elif type == ConverterType.XLSX:
            return XlsxConverter(filename, data)
        elif type == ConverterType.CSV:
            return CsvConverter(filename, data)
        else:
            raise ValueError(f"Tipo de tabela '{type}' não suportado.")

class JsonConverter(Converter):
    
    def __init__(self, filename: str = None, data: List|Dict|List[Dict[str, Any]] = None) -> None:
        super().__init__(filename=filename, data=data)

    @experimental
    def render(self) -> str:
        if self.filename:
            return self.__render_from_file()
        return self.__render_from_json()

    def __render_from_file(self) -> str:
        df = read_json(self.filename)
        return self.from_dataframe(df)

    def __render_from_json(self) -> str:
        df = read_json(StringIO(dumps(self.data)), orient = 'records')
        return self.from_dataframe(df)

class CsvConverter(Converter):
    
    def __init__(self, filename: str = None, data: DataFrame = None) -> None:
        super().__init__(filename=filename, data=data)
        
    def render(self) -> str:
        if self.filename:
            return self.__render_from_file()
        return self.from_dataframe(self.data)

    def __render_from_file(self) -> str:
        df = read_csv(self.filename, sep=';')
        return self.from_dataframe(df)

class XlsxConverter(Converter):
    
    def __init__(self, filename: str = None, data: DataFrame = None) -> None:
        super().__init__(filename=filename, data=data)
        
    def render(self) -> str:
        if self.filename:
            return self.__render_from_file()
        return self.from_dataframe(self.data)

    def __render_from_file(self) -> str:
        df = read_excel(self.filename)
        return self.from_dataframe(df)
        