import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast
import seaborn as sns

st.set_page_config(page_title="Plotting Demo")
st.title("Analytics")

st.header('Sector Price per Sqft Geomap')

new_df = pd.read_csv('datasets/data_viz1.csv')
group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitute','longitude']]

fig = px.scatter_map(group_df, lat="latitute", lon="longitude", color="price_per_sqft", size="built_up_area",
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10, map_style="open-street-map", hover_name=group_df.index,width=1200,height=700)


st.plotly_chart(fig)


feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# st.header('Features Wordcloud')
# wordcloud = WordCloud(width = 800, height = 800,
#                       background_color ='white',
#                       stopwords = set(['s']),  # Any stopwords you'd like to exclude
#                       min_font_size = 10).generate(feature_text)
#
# plt.figure(figsize = (8, 8), facecolor = None)
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.tight_layout(pad = 0)
# st.pyplot(plt.gcf())

st.header('Features Wordcloud')

wordcloud_df = pd.read_csv('datasets/wordcloud_df.csv')

sector = st.selectbox('Choose Sector',sorted(list(wordcloud_df['sector'].unique())))

main = wordcloud_df[wordcloud_df['sector'] == sector]['features'].iloc[0]
main = ast.literal_eval(main)
feature_text = ' '.join(main)

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='white',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot(plt.gcf())

st.header('Area vs Price')

property_type = st.selectbox('Select Property Type',['flat','house'])

if property_type == 'flat':
    fig1 = px.scatter(new_df[new_df['property_type']=='flat'], x="built_up_area", y="price", color="bedRoom", title="Area vs Price")
    st.plotly_chart(fig1,use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom",title="Area vs Price")
    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_option = sorted(list(new_df['sector'].unique()))
sector_option.insert(0,'overall')

selected_sector = st.selectbox('Choose Sector',sector_option)

if selected_sector == 'overall':
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

temp_df = new_df[new_df['bedRoom'] <= 4]
fig3 = px.box(temp_df, x='bedRoom', y='price', title='BHK Price Range')
st.plotly_chart(fig3, use_container_width=True)

st.header('Side by Side Distplot for property type')

fig4 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig4)
