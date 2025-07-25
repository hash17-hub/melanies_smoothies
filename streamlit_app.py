# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"My First Streamlit App :cup_with_straw: {st.__version__}")

name_on_order = st.text_input('Name on Smoothie')
#st.write('The name on your Smoothie will be', name_on_order)

from snowflake.snowpark.functions import col, when_matched

cnx = st.connection("snowflake")
session = cnx.session()

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()                                                                      

ingredients_list = st.multiselect(
'Choose up to 5 ingredients:',my_dataframe, max_selections=5
)

ingredients_string = ''

if ingredients_list:    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')

        # This results in 504 Gateway Timeout ERROR (504)
        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)        
        
        # this works fine; but it can't find some fruits (i.e. found Watermelon, but not-found on Figs)
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)        
        sf_df = st.dataframe(data=smoothiefroot_response.json())

time_to_insert = st.button('Submit Order')

stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
         values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

if time_to_insert:
    session.sql(stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

# New section to display smoothies nutrition information

# smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
# sf_df = st.dataframe(data=smoothiefroot_response.json())

