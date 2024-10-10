import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="AI Visionaries",
    page_icon="🍁",
    layout="wide",
    initial_sidebar_state="expanded")

# CSS for hover effect
hover_css = """
<style>
h4 {
    font-size: 40px;
    color: skyblue;
    text-align: center;
    transition: color 0.3s ease-in-out, transform 0.3s ease-in-out;
}
h4:hover {
    color: red;
    transform: scale(1.1);
}
h1:hover {
    color: #D4AF37;
    transform: scale(1.1);
}
</style>
"""
st.markdown(hover_css, unsafe_allow_html=True)


##Setting Title
st.markdown(
    """
    <h1 style='text-align: center; color: #D4AF37;'>🍁: State/UT wise Sexual Assault Data Analysis (India)</h1>
    """, 
    unsafe_allow_html=True
)
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# add aheading image 
st.image("head_img1.jpg")
## add our logo 
st.sidebar.image("Ai_vis_01.jpg")
## create finters
st.sidebar.header("Apply filters: ")
## read the data 
## lode the crime against woman 2001 - 2014 data
df_state_UT= pd.read_csv('sex_data_01_15.csv')

# # rename some columns
df_state_UT.rename(columns={
 'Assault on women with intent to outrage her modesty':'Outraging_Modesty',
 'Insult to modesty of Women':'Insult_modesty',
 'Cruelty by Husband or his Relatives':'Husband_relatives',
},inplace=True)
# ## convert all state name to lower case
df_state_UT['STATE/UT'] = df_state_UT['STATE/UT'].str.title()

## put all Union Teritory into UT
df_state_UT['STATE/UT'] = df_state_UT['STATE/UT'].replace({
    'A & N Islands': 'UT',
    'Puducherry': 'UT',
    'Chandigarh': 'UT',
    'A&N Islands': 'UT',
    'Delhi Ut': 'UT',
    'Lakshadweep': 'UT',
    'Daman & Diu': 'UT',
    'D & N Haveli': 'UT',
    'D&N Haveli': 'UT',
    'Delhi':'UT'
})

## add a new column of total count of assult 
columns_to_sum = [
    'Rape', 
    'Kidnapping and Abduction', 
    'Dowry Deaths', 
    'Outraging_Modesty', 
    'Insult_modesty', 
    'Husband_relatives', 
    'Importation of Girls'
]
df_state_UT['Sexual_Assault'] = df_state_UT[columns_to_sum].sum(axis=1)

## multiselect 
def mul_select(title, op_list):
    selected = st.sidebar.multiselect(title,op_list)
    select_all = st.sidebar.checkbox("Select all",value=True,key=title)
    if select_all:
        selected_option = op_list
    else:
        selected_option = selected

    return selected_option


#select state in filter 
selected_state = mul_select("Select State",df_state_UT["STATE/UT"].unique())

#select year in filter 
selected_year = mul_select("Select Year",df_state_UT["Year"].unique())

# global filter data 
filter_df = df_state_UT[(df_state_UT["STATE/UT"].isin(selected_state)) & (df_state_UT["Year"].isin(selected_year))]

#### 1.......

st.markdown("<h4>Total Sexual Assault Cases</h4>", unsafe_allow_html=True)

col1 ,col2 , col3= st.columns(3)
with col2:
    st.metric(label="Total Sexual_Assault Cases",value=int(filter_df["Sexual_Assault"].sum()))

def get_tot_sx_assault (df_state_UT):
    Sex_ass = df_state_UT.groupby('Year')['Sexual_Assault'].sum()
    top_states = Sex_ass.sort_values(ascending=False).reset_index()
    return top_states

xx = get_tot_sx_assault(filter_df)

def plot_top_states_by_Sex_ass(xx):
    fig = px.bar(
        xx,
        x='Year',
        y='Sexual_Assault',
        labels={'Year': 'years', 'Sexual_Assault': 'Total Sexual_Assault'},
        color='Sexual_Assault',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    fig.update_layout(
        xaxis_title_font_size=15,
        yaxis_title_font_size=15,
        xaxis_tickangle=-45,
        xaxis_tickfont=dict(size=9, family='bold'),
        yaxis_tickfont=dict(size=9, family='bold'),
        xaxis_tickmode='linear',
        showlegend=False,
    )

    return fig 

st.plotly_chart(plot_top_states_by_Sex_ass(xx))

with st.expander("Download Total Sexual_Assault Cases Data"):
    st.write(xx.style.background_gradient(cmap="Blues"))
    csv = xx.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "state.csv", mime = "text/csv",
                    help = 'Click here to download the data as a CSV file') 

# 2.......
# st.title("TotalRape cases in India by states")
st.markdown("<h4 style='font-size: 40px; text-align: center;'>Total Rape cases in India by states</h4>", unsafe_allow_html=True)

#creating columns 
col4, col5 , col6 = st.columns(3)
with col5:
    st.metric(label="Total Rape Cases",value=int(filter_df["Rape"].sum()))
# plot the total rape cases data using line plot
rape=filter_df.groupby('Year')['Rape'].sum().reset_index()

def plot_rapes(rape):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rape['Year'],
        y=rape['Rape'],
        mode='markers+lines',
        marker=dict(symbol='circle', color='red', size=6),
        line=dict(width=2),
        name='Total rapes'
    ))

    fig.update_layout(
        xaxis_title='Year',
        xaxis_title_font=dict(size=15),
        yaxis_title='Total cases',
        yaxis_title_font=dict(size=15),
        template='plotly_white'  
    )

    fig.update_layout(showlegend=True)

    return fig

st.plotly_chart(plot_rapes(rape))

with st.expander("Download Total Rape cases Data"):
    st.write(rape.style.background_gradient(cmap="Reds"))
    csv = rape.to_csv(index = False).encode('utf-8')
    st.download_button("Download Total Rape cases Data", data = csv, file_name = "state.csv", mime = "text/csv",
                    help = 'Click here to download the data as a CSV file') 

# 3.......
# title
st.markdown("<h4 style='font-size: 40px; text-align: center;'>Total Cases By other categories</h4>", unsafe_allow_html=True)

## Total Cases of Kidnapping and Insult Modesty (2001 - 2014)
kidnap=filter_df.groupby('Year')['Kidnapping and Abduction'].mean().reset_index()
insult=filter_df.groupby('Year')['Insult_modesty'].mean().reset_index()
outraging=filter_df.groupby('Year')['Outraging_Modesty'].mean().reset_index()
husband=filter_df.groupby('Year')['Husband_relatives'].mean().reset_index()

#creating 4 columns for kpis
x, y , z , a = st.columns(4)
with x:
    st.metric(label="Total Kidnapping and Abduction Cases",value=int(filter_df["Kidnapping and Abduction"].sum()))
with y:
    st.metric(label="Total Insult modesty to women Cases",value=int(filter_df["Insult_modesty"].sum()))
with z:
    st.metric(label="Total Outraging Modesty Cases",value=int(filter_df["Outraging_Modesty"].sum()))
with a:
    st.metric(label="Total Husband relatives Cases",value=int(filter_df["Husband_relatives"].sum()))


##plot the data from other categories
def plot_o_h_k_i(outraging, husband, kidnap,insult):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=outraging['Year'],
        y=outraging['Outraging_Modesty'],
        mode='markers+lines',
        marker=dict(symbol='star', color='orange', size=10),
        line=dict(width=2),
        name='Outraging Modesty'
    ))

    fig.add_trace(go.Scatter(
        x=husband['Year'],
        y=husband['Husband_relatives'],
        mode='markers+lines',
        marker=dict(symbol='star', color='purple', size=10),
        line=dict(width=2),
        name='Husband & relatives'
    ))

    fig.add_trace(go.Scatter(
        x=kidnap['Year'],
        y=kidnap['Kidnapping and Abduction'],
        mode='markers+lines',
        marker=dict(symbol='star', color='blue', size=10),
        line=dict(width=2),
        name='Kidnap & Abduction'
    ))

    fig.add_trace(go.Scatter(
        x=insult['Year'],
        y=insult['Insult_modesty'],
        mode='markers+lines',
        marker=dict(symbol='star', color='green', size=12),
        line=dict(width=2),
        name='Insult modesty'
    ))
    
    fig.update_layout(
        xaxis_title='Year',
        xaxis_title_font=dict(size=15),
        yaxis_title='Total cases',
        yaxis_title_font=dict(size=15),
        template='plotly_white'  
    )

    fig.update_layout(showlegend=True)

    return fig

st.plotly_chart(plot_o_h_k_i(outraging, husband, kidnap,insult))

chart1, chart2 = st.columns((2))

#States Having the Maximum Dowry Deaths
dowry_grouped=filter_df.groupby('STATE/UT')['Dowry Deaths'].sum().reset_index()
Dowry_states = dowry_grouped.sort_values(by='Dowry Deaths',ascending=False).head(10)

### pie plot 
def plot_dowry_deaths_pie(Dowry_states):
    fig = px.pie(
        Dowry_states,
        names='STATE/UT',
        values='Dowry Deaths',
        color='Dowry Deaths',
        color_discrete_sequence=px.colors.sequential.Magma
    )

    fig.update_layout(
        showlegend=True
    )
    return fig

with chart1:
    st.markdown("<h4 style='font-size: 40px; text-align: center;'>States with their Dowry Deaths</h4>", unsafe_allow_html=True)
    st.plotly_chart(plot_dowry_deaths_pie(Dowry_states))



#
st.markdown("<h4 style='font-size: 40px; text-align: center;'>States by Importation of Girls</h4>", unsafe_allow_html=True)


col11 ,col12 , col13= st.columns(3)
with col12:
    st.metric(label="Total Importation of Girls",value=int(filter_df["Importation of Girls"].sum()))

#### # Top 10 States Having Importation of Girls
girl_import = filter_df.groupby('STATE/UT')['Importation of Girls'].sum().reset_index()
GI_states = girl_import.sort_values(by='Importation of Girls',ascending=False).head(20)

#plot
def plot_importation_of_girls_bar(GI_states):
 
    fig = px.bar(
        GI_states,
        x='STATE/UT',
        y='Importation of Girls',
        labels={'STATE/UT': 'State/UT', 'Importation of Girls': 'Number of Girls Imported'},
        color='Importation of Girls', 
        color_continuous_scale=px.colors.qualitative.Bold
    )

    fig.update_layout(
        xaxis_title_font_size=15,
        yaxis_title_font_size=15,
        xaxis_tickangle=-45,
        xaxis_tickfont=dict(size=10, family='bold'),
        yaxis_tickfont=dict(size=10, family='bold'),
    )
    return fig

st.plotly_chart(plot_importation_of_girls_bar(GI_states))


#### study details categorical data over state wise 
df = pd.read_csv('SWSA_99_13.csv')

#remove the cities 
df_state_wise = df[~df['STATE/UT'].isin(['Total States', 'A & N Islands',
       'D & N Haveli', 'Daman & DIU', 'Delhi', 'Lakshadeep',
       'Pondicherry', 'Total (UTs)', 'Total (All-India)', 'Ahmedabad',
       'Bangalore', 'Bhopal', 'Calcutta', 'Chennai', 'Coimbatore',
       'Hyderabad', 'Indore', 'Jaipur', 'Kanpur', 'Kochi', 'Lucknow',
       'Ludhiana', 'Madurai', 'Mumbai', 'Nagpur', 'Patna', 'Pune',
       'Surat', 'Vadodra', 'Varanasi', 'Vishakhapatnam'])]

#  Rename the columns
df_state_wise.rename(columns={ 'No. Of Cases In Which Offenders Were Known To The Victims':'known_to_victim',
 'No. Of Cases In Which Offenders Were Parents / Close Family Members':'close_to_family',
 'No. Of Cases In Which Offenders Were Relatives':'relatives',
 'No. Of Cases In Which Offenders Were Neighbours':'neighbours',
 'No. Of Cases In Which Offenders Were Other Known Persons':'known_person'
 },inplace=True)

# converting to integer type
columns = ['known_to_victim','close_to_family','relatives','neighbours','known_person']
for i in columns:
    df_state_wise[i] = pd.to_numeric(df_state_wise[i], errors='coerce').fillna(0).astype(int)

   ### plot
def total_cases_over_time(df):
    total_cases = df.groupby('YEAR')[['known_to_victim', 'close_to_family', 'relatives', 'neighbours', 'known_person']].sum().sum(axis=1).reset_index()
    total_cases.columns = ['YEAR', 'Total_Cases']
    return total_cases
total_cases_data = total_cases_over_time(df_state_wise)


def create_custom_pie_chart(data):
    fig = px.pie(
        data, 
        names='YEAR', 
        values='Total_Cases', 
        color_discrete_sequence=px.colors.sequential.Turbo, 
        hover_data=['Total_Cases'],
    )

    fig.update_traces(
        pull=[0.05]*len(data),  
    )

    fig.update_layout(
        legend=dict(x=1, y=1))
    
    return fig
with chart2:
    st.markdown("<h4 style='font-size: 40px; text-align: center;'>Total Number of Cases Over Time</h4>", unsafe_allow_html=True)
    st.plotly_chart(create_custom_pie_chart(total_cases_data))

## plot 3 of new df
st.markdown("<h4 style='font-size: 40px; text-align: center;'>Victims in between every category </h4>", unsafe_allow_html=True)

kp=df_state_wise.groupby('YEAR')['known_person'].sum().reset_index()
ktv=df_state_wise.groupby('YEAR')['known_to_victim'].sum().reset_index()
neh=df_state_wise.groupby('YEAR')['neighbours'].sum().reset_index()
fam=df_state_wise.groupby('YEAR')['close_to_family'].sum().reset_index()
rel=df_state_wise.groupby('YEAR')['relatives'].sum().reset_index()


col14, col15 , col16, col17, col18 = st.columns(5)
with col14:
    st.metric(label=" assult by known to person ",value=int(df_state_wise["known_person"].sum()))
with col15:
    st.metric(label=" assult by known_to_victim ",value=int(df_state_wise["known_to_victim"].sum()))
with col16:
    st.metric(label=" assult by neighbours cases ",value=int(df_state_wise["neighbours"].sum()))
with col17:
    st.metric(label=" assult by close to family ",value=int(df_state_wise["close_to_family"].sum()))    
with col18:
    st.metric(label=" assult by relatives ",value=int(df_state_wise["relatives"].sum()))

def plot_victim_trends(ktv, kp, neh, fam, rel):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ktv['YEAR'], y=ktv['known_to_victim'], 
        mode='lines+markers', marker=dict(symbol='circle', color='green'), 
        line=dict(color='green', width=1),
        name='known_victim'
    ))

    fig.add_trace(go.Scatter(
        x=kp['YEAR'], y=kp['known_person'], 
        mode='lines+markers', marker=dict(symbol='circle', color='blue'), 
        line=dict(color='blue', width=1),
        name='known_person'
    ))

    fig.add_trace(go.Scatter(
        x=neh['YEAR'], y=neh['neighbours'], 
        mode='lines+markers', marker=dict(symbol='circle', color='red'), 
        line=dict(color='red', width=1),
        name='neighbours'
    ))

    fig.add_trace(go.Scatter(
        x=fam['YEAR'], y=fam['close_to_family'], 
        mode='lines+markers', marker=dict(symbol='circle', color='white'), 
        line=dict(color='white', width=1),
        name='close_to_family'
    ))

    fig.add_trace(go.Scatter(
        x=rel['YEAR'], y=rel['relatives'], 
        mode='lines+markers', marker=dict(symbol='circle', color='purple'), 
        line=dict(color='purple', width=1),
        name='relatives'
    ))

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Victims',
        xaxis=dict(title_font=dict(size=15), showgrid=True),
        yaxis=dict(title_font=dict(size=15), showgrid=True),
        legend_title_text='Categories'
    )
    return fig 

st.plotly_chart(plot_victim_trends(ktv, kp, neh, fam, rel))



##4.......
#title
st.markdown("<h4 style='font-size: 40px; text-align: center;'>States by Total Rape Cases</h4>", unsafe_allow_html=True)
# Calculate the top 7 states with the most rape cases
def get_top_states_by_rape(df):
    top_states = df.groupby('STATE/UT')['Rape'].sum().reset_index()
    return top_states

top_states = get_top_states_by_rape(filter_df)

#  plot top 7 states by rape cases
def plot_top_states_by_rape(top_states):
    fig = px.bar(
        top_states,
        x='STATE/UT',
        y='Rape',
        labels={'STATE/UT': 'State Names', 'Rape': 'Total Rape Cases'},
        color='Rape',
        color_continuous_scale=px.colors.sequential.Cividis
    )
    fig.update_layout(
        xaxis_title_font_size=15,
        yaxis_title_font_size=15,
        xaxis_tickangle=-45,
        xaxis_tickfont=dict(size=9, family='bold'),
        yaxis_tickfont=dict(size=9, family='bold'),
        showlegend=False,
        font_color='white'
    )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    return fig

st.plotly_chart(plot_top_states_by_rape(top_states))


### plot 2 of df 2
st.markdown("<h4 style='font-size: 40px;'>Victims Between Known-to-Victim, Known Person, and Neighbours</h4>", unsafe_allow_html=True)

col19, col20 , col21 = st.columns(3)
with col19:
    st.metric(label="Total known_to_victim Cases",value=int(df_state_wise["known_to_victim"].sum()))
with col20:
    st.metric(label="Total known_person Cases",value=int(df_state_wise["known_person"].sum()))
with col21:
    st.metric(label="Total neighbours Cases",value=int(df_state_wise["neighbours"].sum()))

def plot_victims_grouped(df_state_wise):
    # Group data
    ktv = df_state_wise.groupby('YEAR')['known_to_victim'].mean().reset_index()
    kp = df_state_wise.groupby('YEAR')['known_person'].mean().reset_index()
    neh = df_state_wise.groupby('YEAR')['neighbours'].mean().reset_index()


    # Prepare the data
    years = ktv['YEAR']
    known_victim = ktv['known_to_victim']
    known_person = kp['known_person']
    neighbours = neh['neighbours']

    fig = go.Figure()

    fig.add_trace(go.Bar(x=years, y=known_victim, name='Known to Victim', marker_color='gray')) 
    fig.add_trace(go.Bar(x=years, y=known_person, name='Known Person', marker_color='seagreen')) 
    fig.add_trace(go.Bar(x=years, y=neighbours, name='Neighbours', marker_color='hotpink'))  

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of Victims',
        barmode='group', 
        xaxis_tickangle=-45, 
        legend_title_text='Categories',
        font=dict(color='white'),  
    )
    return fig

st.plotly_chart(plot_victims_grouped(df_state_wise))

