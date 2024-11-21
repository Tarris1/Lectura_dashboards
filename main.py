import streamlit as st
import pandas as pd
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
import os
import numpy as np

def engine():
    load_dotenv()
    user = 'tasa99'
    password = os.getenv("pw")
    host = 'localhost'
    database = 'LECTURA'
    connection_string = f'postgresql://{user}:{password}@{host}/{database}'
    engine = create_engine(connection_string, connect_args={"options": "-c statement_timeout=100000"})
    return engine

def import_authors():
    query = '''SELECT * from AUTHORS;'''
    authors = pd.read_sql(text(query), con=engine()).replace(np.nan, None)
    return authors

def import_texts():
    query = '''SELECT * FROM TEXTS;'''
    texts = pd.read_sql(text(query), con=engine()).replace(np.nan,None)
    return texts

def graph_authors(data):
    columns = [{"value":"author_birth_country","label":"Birth Country"}
                , {"value":"author_birth_city", "label":"Birth City"}, {"value":"author_name_language","label":"Language"}
                ,{"value":"author_nationality", "label":"Nationality"}]
    col_selected = st.multiselect("Select *type* of data to visualize", [i["label"] for i in columns])
    query_value = [i["value"] for i in columns if i["label"]in col_selected]
    if len(col_selected)>0: 
        tabs = st.tabs(col_selected)
        for tab, query_value in zip(tabs, query_value):
            with tab:
                counts = data[query_value].value_counts()
                list_length = st.slider("Select the number of values to show", 1, 100, 10, key=query_value)
                st.table(counts.head(list_length))

def main():
    st.write('''# My First app
             hello *world!*''')
    authorcol, textcol = st.columns(2)
    with authorcol:
        data = import_authors()
        st.write(f'''{len(data)} authors have been found! Explore the authors below:''')
        graph_authors(data)
    with textcol:
        texts = import_texts()
        st.write(f'''{len(texts)} texts have been found! Explore the texts below:''')

if __name__ == "__main__":
    main()