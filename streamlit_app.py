import streamlit as st
from data_handler import DataHandler
from visualizer import Visualizer
import pandas as pd


# Set the configuration of the page
st.set_page_config(
    page_title="US Unemployment Per State",
    page_icon="10165469.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for the logo positioned on the sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        padding-top: 0px;
    }
    .sidebar .sidebar-content img {
        display: block;
        margin: 0 auto;
        width: 100px;
        height: auto;
    }
    /* Custom style for update menu item color */
    .rect.updatemenu-item-rect {
        fill: rgb(102, 109, 116) !important; /* Example: Tomato color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    try:
        # Sidebar title and logo
        st.sidebar.image("10165469.png", width=100)
        st.sidebar.title("Filter the Data")

        # Date range filter
        start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2000-01-01").date())
        end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2021-12-31").date())

        # State dropdown filter
        data_handler = DataHandler('data/Unemployment in America Per US State.csv')
        state_data = data_handler.load_data()
        states = state_data['State/Area'].unique().tolist()
        selected_states = st.sidebar.multiselect("Select states", states, default=states[:1])  # Keeps one state value always selected

        # Graph type selection
        graph_type = st.sidebar.selectbox("Select graph type", 
                                          ["Unemployment Rate by State Over Time", 
                                           "Unemployment Rate Trends Over Time by State", 
                                           "Employment vs. Unemployment (Sampled Data)",
                                           "Average Unemployment Indicator",
                                           "Total Unemployment in Major States Over Time"])

        sample_size = st.sidebar.slider("Sample Size (Employment vs Unemployment)", 1, 100, 10)

        # Filter data based on sidebar inputs
        filtered_state_data = data_handler.filter_data(start_date=start_date, end_date=end_date, states=selected_states)
        visualizer = Visualizer(filtered_state_data)

        ### Main content area ####
        st.title("US Unemployment Per State")

        # Display the plotted graphs
        if graph_type == "Unemployment Rate by State Over Time":
            fig1 = visualizer.plot_unemployment_rate_by_state()
            st.plotly_chart(fig1)
        elif graph_type == "Unemployment Rate Trends Over Time by State":
            fig2 = visualizer.plot_unemployment_rate_trends()
            st.plotly_chart(fig2)
        elif graph_type == "Employment vs. Unemployment (Sampled Data)":
            fig3 = visualizer.plot_employment_vs_unemployment(sample_size / 100)
            st.plotly_chart(fig3)
        elif graph_type == "Average Unemployment Indicator":
            fig4 = visualizer.plot_avg_unemployment_indicator()
            st.plotly_chart(fig4)
        elif graph_type == "Total Unemployment in Major States Over Time":
            fig5 = visualizer.plot_total_unemployment_over_time()
            st.plotly_chart(fig5)

    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
    except ValueError as e:
        st.error(f"Value error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
       
if __name__ == "__main__":
    main()