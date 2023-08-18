# import libraries
"""
You will find below some useful method for data manipulation, analysis, visualization, and report building python libraries.
There are also links to documentation of these libraries if you want to know more!

pandas: data manipulation and analysis
https://pandas.pydata.org/docs/reference/index.html

seaborn: data visualization
https://seaborn.pydata.org/api.html 

streamlit: build web apps
https://docs.streamlit.io/library/api-reference
"""

# import pandas as pd 
# import seaborn as sns
# import streamlit as st
# import matplotlib.pyplot as plt

# pandas
# read a file 
pd.read_csv('data.csv')

# extract rows with specific value in a column
df[df["Sex"] == "M"]

# find number of rows
len(df)

# min and max value of a column
df['Age'].min()
df['Age'].max()

# mean and standard deviation of a column
df['Age'].mean()
df['Age'].std()

# statistics of all columns and single column
df.describe()
df['Age'].describe()

# seaborn
# categorical plots
# https://seaborn.pydata.org/generated/seaborn.catplot.html

# bar plot
sns.catplot(data=df,x='Age',y='Sex',kind="bar")

# streamlit

# set title
st.title('Experimental subjects')

# create tabs
tab1, tab2, tab3 = st.tabs(tabs=['Data','Sex','Age'])
with tab1:
    # everything in tab1
with tab2:
    # everything in tab2
with tab3:
    # everything in tab3

# metric display
st.metric(label='Number of males',value=len(df[df["Sex"] == "M"]))

# display data
df
    # or
st.write(df)
    # or
st.dataframe(df)

# show plots
sns.catplot(data=df,x='Age',y='Sex',kind="bar")
st.write(plt)