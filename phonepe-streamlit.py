
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

#pgsql connection
mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "Postsimrangre1",
                        database = "phonepe_data",
                        port = "5432"
                        )
cursor = mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))


# In[43]:


#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))


# In[44]:


#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands",
                                               "Transaction_count", "Percentage"))


# In[45]:


#map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

map_insurance= pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District",
                                               "Transaction_count", "Transaction_amount"))


# In[46]:


#map_transction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

map_transaction= pd.DataFrame(table5, columns=("States", "Years", "Quarter", "District",
                                               "Transaction_count", "Transaction_amount"))


# In[47]:


#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

map_user= pd.DataFrame(table6, columns=("States", "Years", "Quarter", "District",
                                               "RegisteredUser", "AppOpens"))


# In[48]:


#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))


# In[49]:


#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))


# In[50]:


#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

top_user= pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes",
                                               "RegisteredUsers"))

tacy=Aggre_insurance[Aggre_insurance["Years"]==2021]
tacy.reset_index(drop=True,inplace=True)
tacy["Years"].unique()
tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
tacyg.reset_index(inplace=True)


# In[90]:


def Transaction_amount_count_Y(df, year):
    tacy = df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace=True)
    tacy["Years"].unique()
    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width=600)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                    height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):
    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"QUARTER {quarter} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"QUARTER {quarter} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width=600)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="States", title=f"QUARTER {quarter} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="States", title=f"QUARTER {quarter} TRANSACTION COUNT", fitbounds="locations",
                                    height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Aggre_Tran_Transaction_type(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                            width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                            width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)

# Aggre_User_analysis_1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title=  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]

    auyqs.reset_index(drop=True, inplace=True)
    auyqs=auyqs.sort_values(by="Brands")

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000, markers=True)
    st.plotly_chart(fig_line_1)

    return aguyqs


#Map_insurance_district
def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "District", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "District", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

# top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= map_transaction[["District", "Transaction_amount"]]
    htd1= htd.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "District", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= map_transaction[["District", "Transaction_amount"]]
    htd1= htd.groupby("District")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "District", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= map_transaction[["District", "Transaction_amount"]]
    dt1= dt.groupby("District")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "District", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)





#Streamlit Part

conn = st.connection(
    "mydb",
    type="postgres",
    url="http://localhost:8501/"
)

st.set_page_config(layout= "wide")
st.title("PhonePe Pulse")

with st.sidebar:

    select= option_menu("Menu",["Home","Explore","Top Charts"],icons=["house-heart-fill","mouse-fill","graph-up"])

if select == "Home":

    st.image("pic1.png")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### Domain: Fintech")
        st.markdown(
            "### Technologies used: Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown(
            "### Overview: In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("pic2.png")

elif select == "Explore":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select the Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max())
            Transaction_amount_count_Y_Q(tac_Y, quarters)

        elif method == "Transaction Analysis":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max())
            Aggre_trans_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", Aggre_trans_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_trans_tac_Y, states)

        elif method == "User Analysis":

            col1, col2 = st.columns(2)
            with col1:

                years = st.slider("Select The Year", Aggre_user["Years"].min(), Aggre_user["Years"].max(),
                                  Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select The Quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(),
                                     Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    with tab2:
        method_2= st.radio("Select the Method",["Map Insurance","Map Transaction", "Map User"])

        if method_2 == "Map Insurance":

            col1, col2 = st.columns(2)
            with col1:

                years = st.slider("Select The Year_mi", map_insurance["Years"].min(), map_insurance["Years"].max(),
                                  map_insurance["Years"].min())
            map_insur_tac_Y = Transaction_amount_count_Y(map_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())

            Map_insur_District(map_insur_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select The Quarter_mi", map_insur_tac_Y["Quarter"].min(),
                                     map_insur_tac_Y["Quarter"].max(), map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", map_insur_tac_Y_Q["States"].unique())

            Map_insur_District(map_insur_tac_Y_Q, states)

        elif method_2 == "Map Transaction":

            col1, col2 = st.columns(2)
            with col1:

                years = st.slider("Select The Year", map_transaction["Years"].min(), map_transaction["Years"].max(),
                                  map_transaction["Years"].min())
            map_tran_tac_Y = Transaction_amount_count_Y(map_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mi", map_tran_tac_Y["States"].unique())

            Map_insur_District(map_tran_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select The Quarter_mt", map_tran_tac_Y["Quarter"].min(),
                                     map_tran_tac_Y["Quarter"].max(), map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", map_tran_tac_Y_Q["States"].unique())

            Map_insur_District(map_tran_tac_Y_Q, states)


        elif method_2 == "Map User":

            col1, col2 = st.columns(2)
            with col1:

                years = st.slider("Select The Year_mu", map_user["Years"].min(), map_user["Years"].max(),
                                  map_user["Years"].min())
            map_user_Y = map_user_plot_1(map_user, years)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select The Quarter_mu", map_user_Y["Quarter"].min(),
                                     map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mu", map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)

    with tab3:

        method_3 = st.radio("Select The Method", ["Top Insurance", "Top Transaction"])

        if method_3 == "Top Insurance":

            col1, col2 = st.columns(2)
            with col1:

                years = st.slider("Select The Year", top_insurance["Years"].min(), top_insurance["Years"].max(),
                                  top_insurance["Years"].min())
            top_insur_tac_Y = Transaction_amount_count_Y(top_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select The Quarter", top_insur_tac_Y["Quarter"].min(),
                                     top_insur_tac_Y["Quarter"].max(), top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)



        elif method_3 == "Top Transaction":

            col1, col2 = st.columns(2)
            with col1:

                years = st.slider("Select The Year", top_transaction["Years"].min(), top_transaction["Years"].max(),
                                  top_transaction["Years"].min())
            top_tran_tac_Y = Transaction_amount_count_Y(top_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select The Quarter", top_tran_tac_Y["Quarter"].min(),
                                     top_tran_tac_Y["Quarter"].max(), top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)



elif select == "Top Charts":

    ques = st.selectbox("**Select the Question**",
                        ('Top Brands Of Mobiles Used', 'States With Lowest Trasaction Amount',
                         'Districts With Highest Transaction Amount', 'Top 10 Districts With Lowest Transaction Amount',
                         'Top 10 States With AppOpens', 'Least 10 States With AppOpens',
                         'States With Lowest Trasaction Count',
                         'States With Highest Trasaction Count', 'States With Highest Trasaction Amount',
                         'Top 50 Districts With Lowest Transaction Amount'))

    if ques == "Top Brands Of Mobiles Used":
        ques1()

    elif ques == "States With Lowest Trasaction Amount":
        ques2()

    elif ques == "Districts With Highest Transaction Amount":
        ques3()

    elif ques == "Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques == "Top 10 States With AppOpens":
        ques5()

    elif ques == "Least 10 States With AppOpens":
        ques6()

    elif ques == "States With Lowest Trasaction Count":
        ques7()

    elif ques == "States With Highest Trasaction Count":
        ques8()

    elif ques == "States With Highest Trasaction Amount":
        ques9()

    elif ques == "Top 50 Districts With Lowest Transaction Amount":
        ques10()








