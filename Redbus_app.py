import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests  # For fetching HTML content from GitHub

# **Step 1: Fetch the data from GitHub**
@st.cache_data
def load_data_from_github():
    try:
        # Replace with your GitHub raw file URL
        url = "https://raw.githubusercontent.com/JeyabalGopalan/Redbus/main/RedBus_details.csv"
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        return pd.DataFrame()

# **Function to load HTML content from GitHub**
@st.cache_data
def load_html_from_github(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            st.error(f"Failed to fetch HTML file: {response.status_code}")
            return ""
    except Exception as e:
        st.error(f"Error fetching HTML: {e}")
        return ""

# **Step 2: Streamlit App**
st.set_page_config(
    layout='wide',
    page_title="Redbus",
    page_icon=":bus:"
)

r = st.sidebar.selectbox('Navigation', ['REDBUS_WEB_APPLICATION', 'PROJECT_OVERVIEW'])

if r == "REDBUS_WEB_APPLICATION":
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

        # Load data from GitHub
        data = load_data_from_github()

        if data.empty:
            st.warning("No data available. Please check the GitHub URL or data format.")
            st.stop()

        state = st.sidebar.selectbox('Select the state to travel', sorted(data['State'].unique()))
        route_names = data[data['State'] == state]['Route_Name'].unique().tolist()
        route = st.sidebar.selectbox('Select Route Name', route_names)
        category = st.sidebar.radio('Select Bus Type', data['Category'].unique())

        price_min, price_max = st.sidebar.slider(
            "Select Price Range",
            min_value=int(data['Price'].min()),
            max_value=int(data['Price'].max()),
            value=(0, 2000),
            step=100
        )

        min_rating, max_rating = st.sidebar.slider(
            "Select Rating Range",
            min_value=float(data['Star_Rating'].min()),
            max_value=float(data['Star_Rating'].max()),
            value=(2.0, 5.0),
            step=0.5
        )

        # Display filtered data
        st.write(f"### Available Routes in {state} for {route}")
        st.dataframe(data[(data['State'] == state) & (data['Route_Name'] == route)])

if r == "PROJECT_OVERVIEW":
    st.header("PROJECT_OVERVIEW")
    web2 = option_menu(
        menu_title=None,
        options=["Home", "Selenium", "Pandas", "Streamlit"],
        icons=["house", "info-circle"],
        orientation="horizontal"
    )

    # GitHub raw URLs for HTML files
    html_files = {
        "Selenium": "https://raw.githubusercontent.com/JeyabalGopalan/Redbus/main/RedBus_data_Scraping.html",
        "Pandas": "https://raw.githubusercontent.com/JeyabalGopalan/Redbus/main/Cleaning and Connection.html",
        "Streamlit": "https://raw.githubusercontent.com/JeyabalGopalan/Redbus/main/Streamlit_Sql.html"
    }

    if web2 == "Home":
        st.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
        st.subheader("Overview")
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

    elif web2 in html_files:
        html_url = html_files[web2]
        html_content = load_html_from_github(html_url)
        if html_content:
            st.components.v1.html(html_content, height=900, scrolling=True)
