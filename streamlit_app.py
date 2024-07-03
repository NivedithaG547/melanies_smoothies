# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize your smoothie! 🥤")
st.write(
    """Choose the fruits you want to add in Smoothie!
    """
)


# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Pomogranate"))

# st.write("Your Favourite fruit is", option)


name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your smoothie will be", name_on_order)

#session = get_active_session()

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredient_list=st.multiselect('You can choose upto 5:',my_dataframe
)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)

    ingredients_string=''
    for fruit_chosen in ingredient_list:
        
        ingredients_string+=fruit_chosen + ' '
        st.subheader(fruit_chosen+ 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' , '""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)

    time_to_insert=st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}!", icon="✅")

#New Section to display fruityvice nutrition information
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
#fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
