# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Remove the SelectBox
# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"))

# st.write("Your favorite fruit is:", option)

# Add a Name Box for Smoothie Orders
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Display the Fruit Options List in Your Streamlit in Snowflake (SiS) App. 
# If the line session = get_active_session() appears in your code two times, delete one of the lines.
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

# Add a Multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

# Our ingredients variable is an object or data type called a LIST. So it's a list in the traditional sense of the word, but it is also a datatype or object called a LIST. A LIST is different than a DATAFRAME which is also different from a STRING!
# Let's Get the Fruityvice Data to Show Data for the Fruits Chosen
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    # Create the INGREDIENTS_STRING Variable
    ingredients_string = ''
    
    # Add the FOR Block
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # A Strange-Looking Statement That Will Get Us the "Search On" Value
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        if search_on:
            # Use Our fruit_chosen Variable in the API Call
            st.subheader(fruit_chosen + ' Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
            fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
        else:
            st.error(f"No search value available for {fruit_chosen}")
        
            
        # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        # fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
        
    # Output the String 
    # st.write(ingredients_string)

    # Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+ name_on_order +"""')"""
    # st.write(my_insert_stmt)
    # for troubleshooting
    # st.stop()

    # Add a Submit Button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")

# Call the Fruityvice API from Our SniS App
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# Let's Expose the JSON Data Inside the Response Object
# st.text(fruityvice_response.json())
# Let's Put the JSON into a Dataframe
# fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
