

git add requirements.txt
git commit -m "Add streamlit-option-menu to requirements.txt"
git push




import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd


# **Step 1: Create a connection to the MySQL database**
def create_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Mysql@17072000',
        database='Overall_Bus_details'
    )


# **Step 2: Fetch data using SQL query**
def fetch_filtered_data(state, price_min, price_max, min_rating, max_rating, fare_order):
    connection = create_connection()

    # Build the SQL query dynamically
    query = """
        SELECT * 
        FROM Bus_details
        WHERE State = %s
          AND Price BETWEEN %s AND %s
          AND Star_Rating BETWEEN %s AND %s
        ORDER BY Price {}
    """.format("ASC" if fare_order == "Low to High" else "DESC")

    # Execute the query
    params = (state, price_min, price_max, min_rating, max_rating)
    df = pd.read_sql(query, connection, params=params)

    connection.close()
    return df


# **Step 3: Streamlit App**
# Load the app page configuration
st.set_page_config(
    layout='wide',
    page_title="Redbus",
    page_icon=":material/edit:"
)

# Option menu for navigation
web = option_menu(
    menu_title='Red_Bus Online Portal',
    options=["Home", "Book Tickets"],
    icons=["house", "info-circle"],
    orientation="horizontal"
)

if web == "Home":
    st.write('Welcome to the Home Page')
    st.video("https://youtu.be/AukajR9i_14?feature=shared")
    st.markdown(
        """
        <div style="text-align: center;">
            <a href="https://www.redbus.in/" target="_blank" style="text-decoration: none; color: Red; font-size: 20px;">
                RedBus
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif web == "Book Tickets":
    st.write('## Book Tickets')

    # Sidebar: Select State
    state = st.sidebar.selectbox('Select the state to travel', [
        'Telangana', 'Kerala', 'Andhra', 'Kadamba', 'Rajasthan',
        'South Bengal', 'Himachal', 'Assam', 'Jammu',
        'West Bengal', 'Bihar'
    ])

    # Sidebar: Select Price Range
    price_min, price_max = st.sidebar.slider(
        "Select Price Range",
        min_value=0,
        max_value=5000,
        value=(500, 2000),  # Default range
        step=100
    )

    # Sidebar: Sort by Price
    fare_order = st.sidebar.radio('Sort by Price', ['Low to High', 'High to Low'])

    # Sidebar: Sort by Rating
    rating = st.sidebar.radio('Sort by Rating', ['1-2', '2-3', '3-4', '4-5'])
    min_rating, max_rating = map(float, rating.split('-'))  # Parse rating range

    # Fetch filtered data from MySQL
    filtered_data = fetch_filtered_data(
        state=state,
        price_min=price_min,
        price_max=price_max,
        min_rating=min_rating,
        max_rating=max_rating,
        fare_order=fare_order
    )

    # Display the filtered and sorted data
    st.write(f"### Available Routes in {state}")
    st.dataframe(filtered_data)
