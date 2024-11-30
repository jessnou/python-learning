import pandas as pd

url = 'https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv'
df  = pd.read_csv(url, skiprows = 1)

df2 = df.iloc[:-1, [0,1,13]]
df2.columns = ['Year', 'January', 'Annual_mean']

df2['Year'] = df2['Year'].astype(int)
df2['January'] = pd.to_numeric(df2['January'], errors='coerce')
df2['Annual_mean'] = pd.to_numeric(df2['Annual_mean'], errors='coerce')

import plotly.graph_objs as go
import pandas as pd

x = df2['Year']
y = df2['January']
z = df2['Annual_mean']

# Создание 3D графика
fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=z,  # Цвет зависит от z
        colorscale='Viridis',
        opacity=0.8
    )
)])

fig.update_layout(
    title='3D График температуры',
    scene=dict(
        xaxis_title='Год',
        yaxis_title='Январь',
        zaxis_title='Среднее отклонение'
    )
)

# Отображение
fig.show()
