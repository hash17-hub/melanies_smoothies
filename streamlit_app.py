# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"My First Streamlit App :cup_with_straw: {st.__version__}")

name_on_order = st.text_input('Name on Smoothie')
#st.write('The name on your Smoothie will be', name_on_order)

from snowflake.snowpark.functions import col, when_matched

cnx = st.connection("snowflake")
session = cnx.session()

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_string = ''

ingredients_list = st.multiselect(
'Choose up to 5 ingredients:',my_dataframe, max_selections=5
)

if ingredients_list:    
    for fruit_shosen in ingredients_list:
        ingredients_string += fruit_shosen + ' '

time_to_insert = st.button('Submit Order')

stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
         values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

# st.write(stmt)
# st.stop()

if time_to_insert:
    session.sql(stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

# New section to display smoothies nutrition information
import requests
smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_with=True)

