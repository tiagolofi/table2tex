
from table2tex import Reader

reader = Reader()

# conversor = reader.converter(type='xlsx', filename='jamile/agricultura/planilha_agro.xlsx')

conversor = reader.converter(type='json', filename='jamile/agricultura/cultura_temp.json')

print(conversor.render())