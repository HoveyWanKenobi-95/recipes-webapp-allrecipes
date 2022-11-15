import streamlit as st
import pandas as pd

st.title('Find Recipes that use your ingredients')

data = pd.read_parquet('AllRecipes_DB.parquet')

list_of_clean_ingredients = pd.read_csv('distinct_ingredients.csv')['ingredients']

ratings_cutoff = st.slider('Minimum Rating',min_value=0.0,max_value=5.0, value=4.0, step=0.5)
prep_time_cutoff = st.slider('Maximum Prep Time', min_value = data.prep_time.min(), max_value =  data.prep_time.max())
total_time_cutoff = st.slider('Maximum Total Time', min_value = data.total_time.min(), max_value =  data.total_time.max())
ingredients_list = st.multiselect('Ingredients you have', options = list_of_clean_ingredients)

if st.button('Get the Recipes'):
    ingredients_mask = data.ingredients_cln.apply(lambda x: set(ingredients_list) <= set(x))
    st.dataframe(
        data[((ingredients_mask)&
          (data.prep_time <= prep_time_cutoff)&
          (data.total_time <= total_time_cutoff)&
          (data.ratings>= ratings_cutoff))][['title','ratings','prep_time','total_time','canonical_url']]
    )
else:
    pass
