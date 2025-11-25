# table2tex

Conversor de Tabelas .xlsx, .json e .csv em Tabelas .tex

## Requirements

1. Python 3
2. Pandas e OpenPyXl
3. Configurações do LaTeX

Configs:
```tex
```

## How to use

```python
from table2tex import Reader

reader = Reader()

dados = read_excel('tabela.xlsx')

conversor = reader.converter(type='xlsx', data=dados)
print(conversor.render())
```

### De um arquivo local .xlsx ou .json

```python

from table2tex import Reader

reader = Reader()

conversor = reader.converter(type='xlsx', filename='tabela.json')
print(conversor.render())
```

Resultado:
```tex
\begin{table}[h!]
\centering
\rowcolors{2}{gray!15}{white}
\scalebox{0.8}{%
\resizebox{\textwidth}{!}{%
\begin{tabular}{ccc}
\midrule
\textbf{nome} & 
\textbf{idade} & 
\textbf{cidade} \\
\midrule
João Silva & 28 & São Paulo \\
Maria Oliveira & 34 & Rio de Janeiro \\
Carlos Souza & 22 & Belo Horizonte \\
\midrule
\end{tabular}}}
\end{table}
```