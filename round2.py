code_reference = '''
# pandas https://pandas.pydata.org/docs/reference/index.html
df = pd.read_csv('filename') 
df[df['column_A'] == n] 
len(df) 
df['column_A'].min()  
df['column_A'].max() 
df['column_A'].mean() 
df['column_A'].std() 
df.describe() 
df['column_A'].describe() 
df['column_A'].value_counts() 
df.astype({'column_A': "category"}) 

# seaborn https://seaborn.pydata.org/generated/seaborn.catplot.html
sns.catplot(data=df,x='column_A',y='column_B',kind="bar") 
sns.catplot(data=df,x='column_A',y='column_B',kind="bar",hue=column_C)    
sns.catplot(data=df,x='column_A',y='column_B',kind="box") 
sns.catplot(data=df,x='column_A',y='column_B',kind="violin") 
sns.catplot(data=df,x='column_A',y='column_B',kind="point") 

# streamlit https://docs.streamlit.io/library/api-reference
st.title(your_title) 
st.metric(label='metric label',value=value_to_display) 
df 
st.write(df) 
st.dataframe(df) 

# create and show plot
sns.catplot(data=df,x='column_A',y='column_B',kind="bar")
st.write(plt)

tab1, tab2 = st.tabs(tabs=['tab1_name', 'tab2_name']) 
with tab1: 
    st.text('I am in tab 1')
with tab2: 
    st.text('I am in tab 2')        
'''