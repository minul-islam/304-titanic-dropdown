######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Marvel Movies'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
color4='#0000FF'
sourceurl = 'https://www.kaggle.com/datasets/minisam/marvel-movie-dataset'
githublink = 'https://github.com/minul-islam/304-titanic-dropdown'


###### Import a dataframe #######
df=pd.read_csv("assets/marvel_clean.csv")
df.rename(columns={"NorthAmerica":"NorthAmerica Sales", "Worldwide":"Worldwide Sales"}, inplace=False)
df['Distributor'][(df['Distributor']!='Walt Disney Studios Motion Pictures') & (df['Distributor']!='20th Century Fox') 
   & (df['Distributor']!='Sony Pictures')]='Other' 
variables_list=['Budget', 'NorthAmerica Sales', 'Worldwide Sales']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a variable for Distributor Performance:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['Distributor'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Walt Disney Studios Motion Pictures'].index,
        y=results.loc['Walt Disney Studios Motion Pictures'][continuous_var],
        name='Walt Disney',
        marker=dict(color=color1)
    )
    
    mydata2 = go.Bar(
        x=results.loc['20th Century Fox'].index,
        y=results.loc['20th Century Fox'][continuous_var],
        name='Fox',
        marker=dict(color=color2)
    )
    
    mydata3 = go.Bar(
        x=results.loc['Sony Pictures'].index,
        y=results.loc['Sony Pictures'][continuous_var],
        name='Sony Pictures',
        marker=dict(color=color3)
    )
    
    mydata4 = go.Bar(
        x=results.loc['Other'].index,
        y=results.loc['Other'][continuous_var],
        name='Other',
        marker=dict(color=color4)
    )

    mylayout = go.Layout(
        title='Marvel Movie by Distributors',
        xaxis = dict(title = 'Distributor'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3, mydata4], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
