code_reference = '''
import pandas as pd                     # https://pandas.pydata.org/docs/reference/index.html
df = pd.read_csv('filename') 
df['column_A'].min()  
df['column_A'].max() 
df['column_A'].mean() 
df['column_A'].std() 
df['column_A'].value_counts() 
df['column_A'].unique()

import streamlit as st                  # https://docs.streamlit.io/library/api-reference
st.title('Title')
st.subheader('Subheader') 
st.text('Text')
st.write('## Subheader')
st.write(data)
st.write(plot)
st.metric('Age',10)  
st.dataframe(data)
st.data_editor(data) 
st.bar_chart(data)
'''
