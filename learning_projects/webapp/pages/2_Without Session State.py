import streamlit as st

st.title(':blue[Visualizations]')

import streamlit as st
import seaborn as sns
import pandas as pd

def load_data():
    # Load the Iris dataset
    iris = sns.load_dataset('iris')
    return iris

def without_using_session_state():
    data = load_data()

    st.title('Interactive Data Visualization')

    col1, col2 = st.columns(2,gap='large')

    # Select features to plot
    with col1:
        st.subheader("Select Features to Plot")
        available_features = data.columns[:-1]
        selected_features = st.multiselect("Select features:", available_features)

    with col2:
        # Plot the data
        if selected_features:
            st.subheader("Scatter Plot")
            sns_plot = sns.pairplot(data=data, hue='species', vars=selected_features)
            st.pyplot(sns_plot)



def main():
    without_using_session_state()

    
if __name__ == '__main__':
    main()
