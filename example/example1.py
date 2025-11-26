
from table2tex import Reader, ConverterType

# Exemplo de uso

reader = Reader()

conversor = reader.converter(ConverterType.CSV, 'assets/tabela.csv')

print(conversor.render())
