import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import altair as alt

import datetime

from deta import Deta

from collections import Counter

# --- CONFIGURATION ---
st.set_page_config(
    page_title="❌❌❌",
    page_icon="🦇",
    layout="wide",
    menu_items={
        'About': "https://www.ecoloogamsterdam.nl/"
    }
    
)

# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_amsterdam_bat")

# --- COSTANTS ---

DOEL = ["groepsvorming en zwermen laatvlieger","kraamperiode (1e avond)","kraamperiode (2e avond)","kraamperiode (1e ochtend)",
       "kraamperiode (2e en 3e ochtend)","kraamperiode (4e ochtend)","eind kraamperiode"]

GEBIED = ['P', 'O']

# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items

def insert_input(datum,gebied,doel,waarnemer):

  return db.put({"datum":str(datum),"gebied":gebied,"doel":doel,"waarnemer":waarnemer})

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
selected = option_menu(None, ['✍️','📊','📋'], 
                       icons=None,
                       default_index=0,
                       orientation="horizontal",
                       )

if selected == '✍️':
    datum = st.date_input("Datum", datetime.datetime.today())
    gebied = st.selectbox('Gebied',GEBIED,key='area',placeholder="Kies een gebied...",index=None)
    doel = st.selectbox('Doel',DOEL,key='doel',placeholder="Kies een doel...",index=None)
    waarnemer = st.multiselect('Waarnemer(s)',['Luigi', 'Alko', 'Tobias'],key='waarnemer',placeholder="Kies voor een waarnemer...")
    
    submitted = st.button("Gegevens invoegen")
    
    if submitted:

        if len(waarnemer) == 0 or gebied==None or doel==None:
            st.warning("Vul het formulier in, alstublieft")
            st.stop()
    
        insert_input(datum,gebied,doel,waarnemer)
        st.write(f"Done!")
    
if selected == '📊':

    db_content = load_dataset()
    df = pd.DataFrame(db_content)
    df['img'] = "data:image/jpeg;base64,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"

    tab1, tab2= st.tabs(["🔍", "🦸‍♂️"])


    chart = alt.Chart(df).mark_image(size=15,
        opacity=0.8,
        stroke='black',
        strokeWidth=1,
        strokeOpacity=0.4
    ).encode(
        alt.X('datum:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None, 
              scale=alt.Scale(domain=['2024','2025']))
        ,
        alt.Y('gebied:N',axis=alt.Axis(grid=False,domain=False,ticks=True,),sort=alt.EncodingSortField(field="gebied",  order='ascending'),title=None)
        ,
        url="img",
        tooltip=[
            alt.Tooltip("waarnemer:N"),
            alt.Tooltip("datum:T"),
            alt.Tooltip("gebied:N"),
            alt.Tooltip("doel:N"),
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
        ("April 15, 2024", "Groepsvorming en zwermen laatvlieger"),
        ("May 15, 2024", "Kraamperiode (1e avond en 1e ochtend)"),
        ("June 15, 2024", "Kraamperiode (2e avond)"),
        ("June 1, 2024", "Kraamperiode (2e en 3e ochtend)"),
        ("July 1, 2024", "Kraamperiode (4e ochtend)"),
        ("July 15, 2024", "Eind kraamperiode"),
    ]
    annotations_df = pd.DataFrame(ANNOTATIONS, columns=["datum", "doel"])
    annotations_df.datum = pd.to_datetime(annotations_df.datum)
    

    
    rule = alt.Chart(annotations_df).mark_rule(color="red").encode(
        x="datum:T",
        tooltip=["doel"],
        color=alt.Color('doel:N').legend(None),
        size=alt.value(2),
    ).interactive()
    
    
    
    chart = chart  + rule

    tab1.altair_chart(chart, theme=None, use_container_width=True)
    
    waarnemer = df.waarnemer.to_list()
    data = Counter(get_elements(waarnemer))
    
    data_df = pd.DataFrame.from_dict(data, orient='index').rename(columns={0:"antaal"})
    
    tab2.data_editor(
        data_df,
        column_config={
                "antaal": st.column_config.ProgressColumn(
                    "Aantal werkdagen",
                    format="%f",
                    min_value=0,
                    max_value=30,
                ),
            },
        hide_index=False,
        use_container_width = True
    )

if selected == '📋':

    db_content = load_dataset()
    df = pd.DataFrame(db_content)
    df.drop("key",axis=1,inplace=True)
    
    st.data_editor(
        df,
        hide_index=True,
        use_container_width = True
    )
    

    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(),
        file_name='df.csv',
        mime='text/csv',
    )

    
