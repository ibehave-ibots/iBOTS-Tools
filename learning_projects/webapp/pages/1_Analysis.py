import streamlit as st
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
import seaborn as sns
import time

def prep_page():
    with st.sidebar:
        with st.spinner('Loading'):
            for i in range(10000):
                pass

@st.cache_data
def load_dataset():
    i = 0
    my_bar = st.progress(0, text='')
    with st.sidebar:
        for i in range(100):
            df = sns.load_dataset('titanic')
            my_bar.progress(i + 1, text='#%d'%(i+1))
    st.warning(f'You loaded same dataset for {i+1} times')
    st.info('Done loading titanic dataset')
    return df

def call_titanic():
    st.title(':blue[Titanic database Analysis]')
    st.markdown(body='Loading titanic dataset 100 times')
    df = load_dataset()
    # st.balloons()

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

    option = st.radio(label='Analysis options',options=['Sex','Survived','Class','Age','Clear'])

    if option == 'Sex':
        n_male = len(df[df.sex == 'male'])
        n_female = len(df[df.sex == 'female'])
        col1,col2=st.columns(2)
        col1.metric('Number of male passengers',value=n_male)
        col2.metric('Number of female passengers',value=n_female)
    elif option == 'Survived':
        survived = df[df.survived == 1]
        n_survived = len(survived)
        n_male_survived =len(survived[survived.sex == 'male'])
        n_female_survived =len(survived[survived.sex == 'female'])
        col1,col2,col3 = st.columns(3)
        col1.metric("Survived",value=n_survived)
        col2.metric("Number of male survivors",value=n_male_survived)
        col3.metric("Number of female survivors",value=n_female_survived)
    elif option == 'Class':
        st.bar_chart(data=df,x='class',y='survived')
    elif option == 'Age':
        st.line_chart(data=df,x='age',y='fare')
    else:
        pass

def call_general():
    with st.form("Run analysis"):
        st.title(':blue[Iris database Analysis]')
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        with st.expander('Display data'):
            st.write(df)
        option = st.radio(label='Statistics',options=['Sepal length','Sepal width','Petal length','Petal width','Clear'])

        col1,col2,col3 = st.columns(3)

        if option == 'Sepal length':
            col1.metric("Mean (cm)",np.round(df['sepal length (cm)'].mean(),1))
            col2.metric("std (cm)",np.round(df['sepal length (cm)'].std(),1))

        elif option == 'Sepal width':
            col1.metric("Mean (cm)",np.round(df['sepal width (cm)'].mean(),1))
            col2.metric("std (cm)",np.round(df['sepal width (cm)'].std(),1))

        elif option == 'Petal length':
            col1.metric("Mean (cm)",np.round(df['petal length (cm)'].mean(),1))
            col2.metric("std (cm)",np.round(df['petal length (cm)'].std(),1))

        elif option == 'Petal width':
            col1.metric("Mean (cm)",np.round(df['petal width (cm)'].mean(),1))
            col2.metric("std (cm)",np.round(df['petal width (cm)'].std(),1))

        else:
            pass

            

        st.form_submit_button()    

def main():
    home,titanic, general = st.tabs(tabs=['Home','Titanic','General'])
    prep_page()

    with home:
        st.title(':blue[Analysis]')
        st.write('Here are two other tabs')
        st.write('Go to :green[Titanic] to checkout some analysis on Titanic dataset')
        st.write('Go to :green[General] tab for random fun')

    with titanic:
        call_titanic()

    with general:
        call_general()

    # st.snow()    

    # st.markdown(body='Feedback')
    # with st.form("Feedback form"):
    #     st.write('Your rating')
    #     rating = st.slider("0 (bad) to 10 (excellent)",min_value=0,max_value=10,step=1)
    #     submitted = st.form_submit_button("Submit")

if __name__ == '__main__':
    main()        