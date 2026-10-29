import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="Recommend Appartments")

df = pd.read_csv('datasets/appartments.csv')
location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))

cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

def recommend_properties_with_scores(property_name, top_n=5):

    cosine_sim_matrix = 0.5*cosine_sim1 + 0.8*cosine_sim2 + 1*cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df

st.title('Select Location and Radius')

selected_location = st.selectbox('Location',sorted(location_df.columns.to_list()))
radius = st.number_input('Radius in Kms',step = 1)

if st.button('Search'):
    result = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

    appartment=[]
    distance=[]
    for x,y in result.items():
        appartment.append(x)
        distance.append(str(round(y/1000))+" Km")
        # st.text(x+" "+str(round(y/1000))+" Km")

    st.session_state['appartment'] = appartment
    st.session_state['distance'] = distance

if 'appartment' in st.session_state and st.session_state['appartment']:

    if 'selected_appartment' not in st.session_state:
        selected_appartment = st.radio(
            "Select anyone for recommendation",
            st.session_state['appartment'],
            captions=st.session_state['distance'],
            key='selected_appartment')
    else:
        selected_appartment = st.session_state['selected_appartment']

    st.subheader(selected_appartment)
    st.markdown(f"Link : {df[df['PropertyName']==selected_appartment]['Link'].values[0]}")

    st.text('Recommended Properties 👇')
    recommendations_df = recommend_properties_with_scores(selected_appartment)
    recommendations_df['Link'] = recommendations_df['PropertyName'].map(df.set_index('PropertyName')['Link'])
    recommendations_df.drop(columns=['SimilarityScore'], inplace=True)
    st.dataframe(recommendations_df,column_config={"Link": st.column_config.LinkColumn("")})


