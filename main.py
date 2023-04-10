import json
import requests
import pandas as pd
from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/fastapi")
async def root():  # ASGI Async Server Gateway
    return {"message": "Hello world"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/data_openwo")
async def root():  # ASGI Async Server Gateway
    # return {"message": "Hello world"}
    def createResultDf(uniqueOffices, uniqueDates):
        df = pd.DataFrame(columns=['date', 'office', 'open_work_orders'])
        for i in uniqueDates:
            for j in uniqueOffices:
                new_row = {'date': i, 'office': j, 'open_work_orders': 0}
                df = df._append(new_row, ignore_index=True)
        return df

    url = "https://app.propertyware.com/pw/00a/3195535367/JSON?8reobgj"
    response = requests.get(url)
    data = json.loads(response.text)

    df = pd.DataFrame(data['records'])

    labels = [item['label'].replace(' ', '_').lower()
            for item in data['columns']]
    df.columns = labels

    uniqueOffices = df['office'].unique()
    uniqueOffices = [
        elemento for elemento in uniqueOffices if elemento not in ["SanJose", "*"]]
    uniqueDates = df['start_date'].unique()

    df_filtered = df.query('date_completed == ""')
    #delete after
    df_filtered = df_filtered.head(20)
    df_results = createResultDf(uniqueOffices, uniqueDates)
    cont = 0
    for index, row in df_filtered.iterrows():
        for index1, row1 in df_results.iterrows():
            if row1['office'].replace(" ", "") == row['office'].replace(" ", "") and row['start_date'] <= row1['date']:
                df_results['open_work_orders'][index1] += 1
            cont += 1
    #data_json = df_results.to_json()
    #print(df_results['open_work_orders'].sum())
    return df_results
