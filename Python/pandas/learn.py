import pandas as pd

# a example of pd.merge
df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                    'data1': range(7)})
df2 = pd.DataFrame({'key': ['a', 'b', 'd'],
                    'data2': range(3)})
print(df1)
print(df2)
print(pd.merge(df1, df2))
# print(pd.merge(df1, df2, on='key'))