import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd

import datetime

from deta import Deta

from collections import Counter

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

def get_elements(l):
    ret = []
    for elem in l:
        if type(elem) == list:
            ret.extend(get_elements(elem))
        else:
            ret.append(elem)
    return ret
        
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

        if len(waarnemer) == 0:
            st.write("chose a waarnamer")
            st.stop()
    
        insert_input(date,area,start_hour,waarnemer,finish_hour,report)
        st.write(f"Done!")
    
if selected == '📊':

    

    with st.popover("Table"):
  
        db_content = load_dataset()
        df = pd.DataFrame(db_content)
        df
    
        st.download_button(
            label="Download data as CSV",
            data=df.to_csv(),
            file_name='large_df.csv',
            mime='text/csv',
        )

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
        ("April 15, 2024", "groepsvorming en zwermen laatvlieger"),
        ("May 15, 2024", "kraamperiode (1e avond)"),
        ("June 15, 2024", "kraamperiode (2e avond)"),
        ("May 15, 2024", "kraamperiode (1e ochtend)"),
        ("June 1, 2024", "kraamperiode (2e en 3e ochtend)"),
        ("July 1, 2024", "kraamperiode (4e ochtend)"),
        ("July 15, 2024", "eind kraamperiode"),
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

    "---"
    
    waarnemer = df.waarnemer.to_list()
    data = Counter(get_elements(waarnemer))
    
    data_df = pd.DataFrame.from_dict(data, orient='index').rename(columns={0:"antaal"})
    
    st.data_editor(
        data_df,
        column_config={
                "antaal": st.column_config.ProgressColumn(
                    "Antaal",
                    format='%.4g',
                    help="Number of surveys",
                    min_value=0,
                    max_value=data_df.antaal.max(),
                ),
            },
        hide_index=False,
        use_container_width = True
    )
