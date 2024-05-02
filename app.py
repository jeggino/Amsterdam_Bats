import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd

import datetime

from deta import Deta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="❌❌❌",
    page_icon="🦇",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "https://www.ecoloogamsterdam.nl/"
    }
    
)

# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_amsterdam_bat")

# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items

def insert_input(date,area,start_hour,waarnemer,finish_hour,report):

  return db.put({"date":str(date),"area":area,"waarnemer":waarnemer,"start_hour":start_hour,"finish_hour":finish_hour,"report":report})

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)
        
# --- APP ---
# horizontal menu
selected = option_menu(None, ['✍️','📊'], 
                       icons=None,
                       default_index=0,
                       orientation="horizontal",
                       )

if selected == '✍️':
    date = st.date_input("Date", datetime.datetime.today())
    area = st.multiselect('Chose an Area',['P', 'O'],key='area')
    waarnemer = st.multiselect('waarnemer(s)',['Luigi', 'Alko', 'Tobias'],key='waarnemer')
    start_hour = str(st.time_input('Start time', datetime.time(14, 45),step=300))
    finish_hour = str(st.time_input('Finish time', datetime.time(22, 00),step=300))
    report = st.text_area("")
    
    
    submitted = st.button("Insert survey")
    
    if submitted:
    
        insert_input(date,area,start_hour,waarnemer,finish_hour,report)
        st.write(f"Done!")
    
if selected == '📊':

    

    with st.popover("Table"):
  
        db_content = load_dataset()
        df = pd.DataFrame(db_content)
        # df['date'] = pd.to_datetime(df['date'])
        # df['week_of_year'] = df['date'].dt.isocalendar().week
        # df['day_of_the_week'] = df['date'].dt.day_name() 

        df
    
        st.download_button(
            label="Download data as CSV",
            data=df.to_csv(),
            file_name='large_df.csv',
            mime='text/csv',
        )

    
    # df_report = df.set_index('date')
    # df_report 

    date_2 = str(st.date_input("Date", key="second"))

    try:

        # report_write = df_report.loc[date_2,"report"]
        report_write = df[df["date"]==date_2]["report"]
        report_write[1]
      
        # REPORT
        with st.popover("Report"):
            st.markdown(report_write)

    except:
        st.warning("No data")
        st.stop()

