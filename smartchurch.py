import mysql.connector
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as ply


mydb = mysql.connector.connect(
    host="192.254.190.238",
    user="smartsel_lina",
    passwd="*********",
    database="smartsel_chapps"
)

mycursor = mydb.cursor()
mycursor.execute('SELECT D.ddesc,  SUM(M.male) AS male, SUM(M.female) AS female, SUM(M.children) AS children, '
                 'SUM(M.new_convert) AS new_convert, SUM(M.first_timer) AS first_timer, SUM(M.testimonies) AS '
                 'testimonies,  SUM(M.total_attendance) AS total_attendance FROM tblcenter AS C LEFT JOIN tblmeeting '
                 'AS M ON M.center_code = C.cell_code LEFT JOIN tbldistrict AS D ON D.dcode = C.district_code  GROUP '
                 'BY dcode, ddesc ORDER BY D.dcode');
rows = mycursor.fetchall()
df = pd.DataFrame([[ij for ij in i] for i in rows])
df.rename(columns={0: 'district', 1: 'males', 2: 'females', 3:'children', 4:'new_converts', 5:'first_timers'}, inplace=True);


trace0 = go.Bar(
    x= df['district'].tolist(),
    y=df['females'].tolist(),
    name='females',
    marker=dict(
    color='rgb(49,130,189)',
    )
)

trace1 = go.Bar(
    x= df['district'].tolist(),
    y=df['males'].tolist(),
    name='males',
    marker=dict(
        color='rgb(204,204,204)',
    )
)
trace2 = go.Bar(
    x= df['district'].tolist(),
    y=df['children'].tolist(),
    name='children',
    marker=dict(
        color='rgb(222,45,38,0.8)',
    )
)

trace3 = go.Bar(
    x= df['district'].tolist(),
    y=df['new_converts'].tolist(),
    name='new converts',
    marker=dict(
        color='rgb(55, 83, 109)',
    )
)
trace4 = go.Bar(
    x= df['district'].tolist(),
    y=df['first_timers'].tolist(),
    name='first timers',
    marker=dict(
        color='rgb(0,0,0)',
    )
)

data = [trace0, trace1, trace2, trace3, trace4]
layout = go.Layout(
    xaxis=dict(tickangle=-45),
    barmode='group',
)

fig = go.Figure(data=data, layout=layout)
ply.plot(fig, filename='index.html')
