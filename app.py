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

DOEL = ["Groepsvorming laatvlieger","Kraamperiode (avond)","Kraamperiode (ochtend)","Winterverblijfplaatsen","Paarverblijfplaatsen"]

GEBIED = ['P', 'O', 'Q', 'B', 'R', 'M', 'N', 'L']

WAARNEMERS = ['Luigi', 'Alko', 'Tobias', 'Sanders','Mats']

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
    waarnemer = st.multiselect('Waarnemer(s)',WAARNEMERS,key='waarnemer',placeholder="Kies voor een waarnemer...")
    
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

    tab1, tab2= st.tabs(["🔍", "🦸‍♂️"])


    chart = alt.Chart(df).mark_point(size=60
                                     
    ).encode(
        alt.X('datum:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None, 
              scale=alt.Scale(domain=['2024','2025']))
        ,
        alt.Y('gebied:N',
              axis=alt.Axis(grid=False,domain=False,ticks=True,),
              sort=alt.EncodingSortField(field="gebied",  order='ascending'),
              title="Gebied")
        ,
        stroke=alt.Color('doel'),
        fill=alt.Color('doel').title("Doel"),
        legend=alt.Legend(orient='none',legendX=130, legendY=-40,direction='horizontal',titleAnchor='middle')),
        tooltip=[
            alt.Tooltip("datum:T",title = "Datum"),
            alt.Tooltip("gebied:N",title ="Gebied"),
            alt.Tooltip("doel:N",title ="Doel"),
            alt.Tooltip("waarnemer:N",title ="Waarnemer(s)"),
        ],
    ).properties(
        width=450,
        height=300,
        title=alt.Title(
            text="",
            subtitle="",
            anchor='start'
        )
    ).configure_view(
    stroke=None
).interactive()

    with tab1:
        st.altair_chart(chart, theme=None, use_container_width=True)
        with st.expander("Planning"):
            st.image('images/Screenshot 2024-06-09 150207.png')
    
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
    
    name = st.selectbox('Waarnemer(s)',WAARNEMERS,key='name',placeholder="Kies voor een waarnemer...")
    rows=[]
    for row,col in df.iterrows():
        if name in col.waarnemer:
            rows.append(row)
        
        
    df_filtered = df.loc[rows]
    
    st.data_editor(
        df_filtered,
        hide_index=True,
        use_container_width = True
    )
    

    st.download_button(
        label="Download data as CSV",
        data=df_filtered.to_csv(),
        file_name='df.csv',
        mime='text/csv',
    )

    
