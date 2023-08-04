from kaggle_connection import KaggleDatasetConnection
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Streamlit-Kaggle Connection Demo App", layout="wide")
with st.sidebar:
    st.subheader(":blue[Streamlit CONNECTION HACKATHON]")
    st.image("https://global.discourse-cdn.com/business7/uploads/streamlit/optimized/3X/d/6/d6e06e08c5eae258e58f8e71e9bb0db8c77a9db1_2_1000x1000.jpeg")
    st.info("1. Start with search for dataset in kaggle (e.g enter 'Houses' ), then click Search button")
    st.info("2. After clicking Search button , many datasets will appear ")
    st.info("3. Copy the reference of a dataset that you want")
    st.info("4. Paste the reference in auther input and click view, you will see the 20 first rows")
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown(
        "<a href='https://github.com/MohamedLouttHB/RSA_App'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/2048px-Octicons-mark-github.svg.png' height='30' width='30'></a> [ source code ](https://github.com/MohamedLouttHB/RSA_App)",
        unsafe_allow_html=True)

    st.markdown(
        "<a href= 'https://twitter.com/medloutt'><img src='https://seeklogo.com/images/T/twitter-x-logo-0339F999CF-seeklogo.com.png?v=638258000530000000' height='30' width='30'> Twitter </a> ",
        unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    st.write('**_:blue[Made by]_ :violet[Mohamed Loutt Horma Babana]**')

st.image('https://i.postimg.cc/PfVwHZ2Z/kaggle-streamlit-header.png', width=500)

st.title("Streamlit-Kaggle Connector App", anchor=False)
st.subheader("Using ``st.experimental_connection``", anchor=False)
st.divider()


conn = st.experimental_connection("kaggle_datasets", type=KaggleDatasetConnection)

@st.cache_data
def search(ds):
    conn.conn.authenticate()
    data = []
    dataset_list = conn.conn.dataset_list(search=ds)
    # Extract relevant information from each DatasetItem and create a list of dictionaries
    data = []
    for dataset in dataset_list:
        data.append({
            'Reference': dataset.ref,
            'Title': dataset.title,
            'Owner': dataset.ownerRef,
            'Size': dataset.size,
            'Last Updated': dataset.lastUpdated,
        })

    # Create a DataFrame
    df = pd.DataFrame(data)
    return df

col1, col2 = st.columns(2)
with col1:
    #Search datasets
    search_ds = st.text_input("search dataset by keyword")

    go_ds = st.button('Search')
    try:

        if search_ds:
            if go_ds:
                dfs = search(search_ds)
            with st.expander("List of datasets found", expanded=True):
                # Set the height of the table to limit its display
                st.dataframe(dfs, height=400)

        else:
            if go_ds and not search_ds:
                st.warning('Enter keyword to search !')
    except Exception as e:
        pass
        #st.warning(f'Error : {e}')

with col2:
    view_ds = st.text_input('Enter the reference of a dataset to see it')
    load_ds = st.button('View')

    if view_ds:
        try:
            if load_ds:
                conn = st.experimental_connection("kaggle_datasets", type=KaggleDatasetConnection)
                df = conn.get(dataset_reference=view_ds, ttl=3600)
                st.write(df.head(20))
        except Exception as e:
            st.error("ERROR : Reference not valid !")

    else:
        if load_ds and not view_ds:
            st.warning('Enter the reference !')



#Hide streamlit logos
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)







