
from table2tex import Reader
from pandas import DataFrame, read_excel

reader = Reader()

dados = read_excel('tabela.xlsx')

conversor = reader.converter(type='json', filename='tabela.json')
print(conversor.render())