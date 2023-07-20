import streamlit as st
import pandas as pd
import numpy as np

st.title(':red[Home Page]')

st.header(":violet[Text elements]")

st.markdown(body='**:orange[Markdown support] with st.markdown**',help='this is a tooltip. :green[Look!] you can use _italics_ and **bold** here as well!')
st.markdown(body='Here is latex formula $a+b^2=c$')

st.markdown(body='**:orange[Code] with st.code**')
st.code(body='print("Hello World")',language='python')

st.divider()

code = '''
a = 20
b = 25
c = a + b
'''
st.code(body=code, language='python',line_numbers=True)

code = '''def get_name(name):
    return name'''
st.code(body=code,language='python')

st.code(body='c=complex(a,b) #this is in matlab',language='matlab')
st.code(body='ls *.csv',language='bash')

st.write("---")

st.markdown(body='**:orange[Text] with st.text**')
st.text(body='This is a text with tooltip', help='here you go')
st.text(body='**bold** :green[color] **:green[bold color]** _:green[italicized color]_ **_:green[bold italicized color]_**',help='Notice text styling does not work')

"---"

st.markdown(body='**:orange[Text] with st.text**')

st.markdown(body='**:orange[Emoji support]** :sunglasses::+1::100:')

st.write('iBOTS team')
st.write(pd.DataFrame({'names':['Nicholas Del Grosso','Mohammad Bashiri','Sangeetha Nandakumar']}))

# magic command
df = pd.DataFrame({'names':['Nicholas Del Grosso','Mohammad Bashiri','Sangeetha Nandakumar']})
df

"---"

st.header(":violet[Data elements]")
st.markdown(body='**:orange[Dataframe] with st.dataframe**')

st.dataframe(data=df, width=None, height=None, use_container_width=False, hide_index=True, column_order=None, column_config=None)

st.markdown(body='**:orange[Data Editor] with st.data_editor**', help='Edit your data with this')
st.data_editor(data=df)