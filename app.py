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
    area = st.selectbox('Chose an Area',['P', 'O'],key='area')
    waarnemer = st.multiselect('waarnemer(s)',['Luigi', 'Alko', 'Tobias'],key='waarnemer')
    start_hour = str(st.time_input('Start time', datetime.time(14, 45),step=300))
    finish_hour = str(st.time_input('Finish time', datetime.time(22, 00),step=300))
    report = st.text_area("")

    
    
    
    submitted = st.button("Insert survey")
    
    if submitted:

        if waarnemer == None:
            st.write("chose a waarnamer")
            st.stop()
    
        insert_input(date,area,start_hour,waarnemer,finish_hour,report)
        st.write(f"Done!")
    
if selected == '📊':

    

    with st.popover("Table"):
  
        db_content = load_dataset()
        df = pd.DataFrame(db_content)
        # df["date_added"] = pd.to_datetime(df['date_added'],format="%B %d, %Y")
        # df['date'] = pd.to_datetime(df['date'],format="%Y-%B-%d")
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
    import altair as alt


    chart = alt.Chart(df).mark_circle(size=30,
        opacity=0.8,
        stroke='black',
        strokeWidth=1,
        strokeOpacity=0.4
    ).encode(
        alt.X('date:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None, 
              scale=alt.Scale(domain=['2024','2025']))
        ,
        alt.Y('area:N',axis=alt.Axis(grid=False,domain=False,ticks=True,),sort=alt.EncodingSortField(field="area",  order='ascending'),title=None)
        ,
        
        tooltip=[
            alt.Tooltip("waarnemer:N"),
            alt.Tooltip("date:T"),
            alt.Tooltip("area:N"),

        ],
    ).properties(
        width=450,
        height=300,
        title=alt.Title(
            text="",
            subtitle="",
            anchor='start'
        )
    )
    
    # Add annotations
    ANNOTATIONS = [
        ("Mar 01, 2016", "Pretty good day for GOOG"),
        ("Dec 01, 2017", "Something's going wrong for GOOG & AAPL"),
        ("Nov 01, 2018", "Market starts again thanks to..."),
        ("Dec 01, 2019", "Small crash for GOOG after..."),
    ]
    annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
    annotations_df.date = pd.to_datetime(annotations_df.date)
    

    
    rule = alt.Chart(annotations_df).mark_rule(color="red").encode(
        x="date:T",
        tooltip=["event"],
        color=alt.Color('event:N').legend(None),
        size=alt.value(2),
    ).interactive()
    
    
    
    chart = chart  + rule

    st.altair_chart(chart, theme=None, use_container_width=True)
        
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

