import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import time


st.title(':blue[Titanic dataset analysis]')

st.markdown(body='Loading titanic dataset 100 times')
with st.sidebar:
    with st.spinner('Loading'):
        for i in range(100):
            df = sns.load_dataset('titanic')
    

time.sleep(5)
i = 0
my_bar = st.progress(0, text='')
with st.sidebar:
    for i in range(100):
        df = sns.load_dataset('titanic')
        my_bar.progress(i + 1, text='#%d'%(i+1))
st.warning(f'You loaded same dataset for {i+1} times')
st.info('Done loading titanic dataset')
st.balloons()

with st.expander('Display data'):
    st.write(df)

st.success('Successfully setup the analysis project')    
"---"

st.markdown('Removing null values')
len_original = len(df)
df = df.dropna()
delta = len(df) - len_original
st.metric("Number of rows",value=len(df),delta=delta)

'''---'''
edit_true = st.checkbox(label='Do you want to edit data?')

if edit_true:
    col_config = {
        "sex":st.column_config.SelectboxColumn(label='Sex',options=['female','male']),
        "age":st.column_config.NumberColumn(label='Age',min_value=0.,max_value=120),
        "pclass":st.column_config.SelectboxColumn(label='Passenger class',options=[1,2,3]),
        "alone":st.column_config.CheckboxColumn(label='Survived')
    }


    df_edited = st.data_editor(
        df,
        column_config=col_config,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
    )

else:
    df_edited = df

'''---'''

option = st.radio(label='Analysis options',options=['sex','survived','class','embark'])

if option == 'sex':
    n_male = len(df[df.sex == 'male'])
    n_female = len(df[df.sex == 'female'])
    st.write(f'Number of male passengers: {n_male}')
    st.write(f'Number of female passengers: {n_female}')
elif option == 'survived':
    survived = df[df.survived == T]
    n_survived = len(survived)
    n_male_survived =len(survived[survived.sex == 'male'])
    n_female_survived =len(survived[survived.sex == 'female'])
    

st.markdown(body='Feedback')
with st.form("Feedback form"):
    st.write('Your rating')
    rating = st.slider("0 (bad) to 10 (excellent)",min_value=0,max_value=10,step=1)
    submitted = st.form_submit_button("Submit")