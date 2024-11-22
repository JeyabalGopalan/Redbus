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

r = st.sidebar.selectbox('Navigation', ['REDBUS_WEB_APPLICATION', 'PROJECT_OVERVIEW'])

if r== "REDBUS_WEB_APPLICATION":
    # Option menu for navigation


    web1 = option_menu(
        menu_title="REDBUS_WEB_APPLICATION",
        options=["Home", "Book Tickets"],
        icons=["house", "info-circle"],
        orientation="horizontal"
    )

    if web1 == "Home":
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

    elif web1 == "Book Tickets":
        st.write('## Book Tickets')

        # Sidebar: Select State
        state = st.sidebar.selectbox('Select the state to travel', [
            'Telangana', 'Kerala', 'Andhra', 'Kadamba', 'Rajasthan',
            'South Bengal', 'Himachal', 'Assam', 'Jammu',
            'West Bengal', 'Bihar'
        ], index=2)

        # Sidebar: Select Price Range
        price_min, price_max = st.sidebar.slider(
            "Select Price Range",
            min_value=0,
            max_value=5000,
            value=(500, 4000),  # Default range
            step=100
        )

        # Sidebar: Sort by Price
        fare_order = st.sidebar.radio('Sort by Price', ['Low to High', 'High to Low'])

        # Sidebar: Sort by Rating
        rating = st.sidebar.radio('Sort by Rating', ['1-2', '2-3', '3-4', '4-5'], index=2)
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

if r== "PROJECT_OVERVIEW":

    st.header("PROJECT_OVERVIEW")
    # Create menu
    web2 = option_menu(
        menu_title=None,
        options=["Home", "Selenium", "Pandas", "Streamlit"],
        icons=["house", "info-circle"],
        orientation="horizontal"
    )

    # Home Page
    if web2 == "Home":
        st.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
        st.subheader("OverView")
        st.write(
            "The Redbus Data Scraping and Filtering with Streamlit Application aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
        st.subheader("Approach:")
        st.markdown(
            "Data Scraping: Use Selenium to automate the extraction of Redbus data including routes, schedules, prices, and seat availability.")
        st.markdown("Data Storage: Store the scraped data in a SQL database")
        st.markdown(
            "Streamlit Application: Develop a Streamlit application to display and filter the scraped data and Implement various filters such as bustype, route, price range, star rating, availability ")
        st.markdown(
            "Data Analysis/Filtering using Streamlit: Use SQL queries to retrieve and filter data based on user inputs and Use Streamlit to allow users to interact with and filter the data through the application.")
        st.subheader("Technical Tags:")
        st.markdown("Web Scraping, Selenium, Streamlit, SQL, Data Analysis, Python, Interactive Application")
        st.subheader("Project Devloped by : Jeyabal G ")
    # Selenium Page
    if web2 == "Selenium":
        st.write(
            "Web Scraping with Selenium allows you to gather all the required data using Selenium Webdriver Browser Automation. Selenium crawls the target URL webpage and gathers data at scale. This article demonstrates how to do web scraping using Selenium.")

        # Load and display HTML content in an iframe
        file_path = "C:/Users/jeyaj/Downloads/GUVI/RedBus Project/RedBus_data_Scraping.html"
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        st.components.v1.html(html_content, height=900, scrolling=True)

    # Pandas Page
    if web2 == "Pandas":
        st.write(
            "Python Pandas Data Cleaning includes identifying and correcting mistakes in the dataset, addressing outliers, and filling in missing values. The methods for data cleaning in Python data science may vary depending on the dataset.")

        # Load and display HTML content in an iframe
        file_path = "C:/Users/jeyaj/Downloads/GUVI/RedBus Project/Cleaning and Connection.html"
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        st.components.v1.html(html_content, height=900, scrolling=True)

    # Streamlit Page
    if web2 == "Streamlit":
        st.write(
            "Streamlit is a free and open-source framework to rapidly build and share beautiful machine learning and data science web apps. It is a Python-based library specifically designed for machine learning engineers.")

        st.header(" ")
        web3 = option_menu(
            menu_title=None,
            options=["Python", "SQL"],
            orientation="horizontal"
        )
        # Python Tab
        if web3 == "Python":
            st.markdown(
                """
                <div style="text-align: center;">
                    <p>RedBus Web Application Developed Using Local Database</p>
                    <a href="http://192.168.135.173:8503" target="_blank" style="text-decoration: none; color:Blue; font-size: 20px;">
                        Click Here to view app
                    </a>
                </div>
                """, unsafe_allow_html=True
            )

            # Load and display HTML content in an iframe
            file_path = "C:/Users/jeyaj/Downloads/GUVI/RedBus Project/Streamlit_python.html"
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            st.components.v1.html(html_content, height=900, scrolling=True)

        # SQL Tab
        else:
            st.markdown(
                """
                <div style="text-align: center;">
                    <p>RedBus Web Application Developed Using My-Sql Database</p>
                    <a href="http://192.168.135.173:8502" target="_blank" style="text-decoration: none; color: Red; font-size: 20px;">
                        Click Here to view app
                    </a>
                </div>
                """, unsafe_allow_html=True
            )

            # Load and display HTML content in an iframe
            file_path = "C:/Users/jeyaj/Downloads/GUVI/RedBus Project/Streamlit_Sql.html"
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            st.components.v1.html(html_content, height=900, scrolling=True)
