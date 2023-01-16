import os,pandas as pd
from collections import defaultdict
from dash import Dash,dcc, html, Input, Output
import plotly.express as px

class Weather:
    def __init__(self):
        # self.data=pd.read_csv(os.path.join('','Datasets','city_temperature.csv'),header=0)
        # self.data.drop(columns=['State'],inplace=True)
        # print(self.data.describe(),end='\n\n')
        # self.group_by_country=self.data.groupby(['Country','City','Month'],as_index=False,sort=False)
        # print(self.group_by_country.first())
        self.data=defaultdict(list)
        self.cities=set()
        self.years=set()
        self.countries=set()
        self.months=set()
        self.desc=list()

        with open(os.path.join('','Datasets','city_temperature.csv'),'r') as RF:
            for i,line in enumerate(RF):
                if i==0:
                    self.desc=line.split(',')
                    continue
                country_data=[word.strip() for word in line.split(',')]
                self.data[(country_data[1],country_data[3],int(country_data[4]),country_data[6])].append(float(country_data[7]))
                self.countries.add(country_data[1])
                self.cities.add(country_data[3])
                self.months.add(int(country_data[4]))
                self.years.add(country_data[6])
        print(self.countries,end='\n\n')
        print(self.cities,end='\n\n')
        print(self.months,end='\n\n')
        print(self.years,end='\n\n')

        print('Insights')
        print('*'*20)
        print(f'Number of cities:{len(self.cities)}')
        print(f'Total years recorded:{len(self.years)}')
        print(f'Number of countries:{len(self.countries)}')
        country,city,month,year=[x.strip() for x in "Algeria,Algiers,1,1995".split(',')]
        month=int(month)
        print(f'TestCasses:{self.search(country,city,month,year)}')

    def search_by_country(self,search_country):
        if search_country not in self.countries:
            raise ValueError(f"Country:{search_country} not found")
        
        return {
            (city,month,year):temperatures
            for (country,city,month,year),temperatures in self.data.items()
            if country==search_country 
        }
    
    def search_by_city(self,search_city):
        if search_city not in self.countries:
            raise ValueError(f"Country:{search_city} not found")
        
        return {
            (month,year):temperatures
            for (_,city,month,year),temperatures in self.data.items()
            if city==search_city 
        }
    
    def search(self,country,city,month,year):
        if country not in self.countries or city not in self.cities or month not in self.months or year not in self.years:
            raise ValueError(f"Bad Configurations:{country}  {city}  {month}  {year}")
        
        return self.data[(country,city,month,year)]
    

def mainloop(weather):
    app = Dash(__name__)
    app.layout = html.Div([
        html.H4('Temperatures Application'),
        html.P("Select configuration"),
        dcc.Dropdown(
            id="id_selector",
            options=[f"{country},{city},{month},{year}" for (country,city,month,year) in weather.data.keys()],
            value="Algeria,Algiers,1,1995",
            clearable=False
        ),
        dcc.Graph(id='temparature_figure')
    ])

    @app.callback(
        Output('temparature_figure', 'figure'),
        Input('id_selector', 'value'))
    def update_line_chart(conf_val):
        country,city,month,year=[x.strip() for x in conf_val.split(',')]
        month=int(month)
        temperatures=weather.search(country,city,month,year)
        df=pd.DataFrame()
        df['Date']=[f'D{i+1}' for i in range(len(temperatures))]
        df['Temperature']=temperatures
        print(df)
        fig = px.line(df,x="Date",y="Temperature",title=f'{country}-{city}-{month}-{year}')
        return fig

    app.run_server(debug=True)

if __name__=='__main__':
    weather=Weather()
    mainloop(weather)

    