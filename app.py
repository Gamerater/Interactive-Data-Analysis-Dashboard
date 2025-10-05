import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import StringIO

def main():
    """
    Main function to run the Streamlit data analysis dashboard.
    """
    st.set_page_config(layout="wide", page_title="Interactive Data Analysis Dashboard")

    st.title("📊 Interactive Data Analysis Dashboard")
    st.write("Upload your CSV or Excel file to begin exploring your data.")

    # --- Sidebar for File Upload and Options ---
    with st.sidebar:
        st.header("1. Upload Your Data")
        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

        if uploaded_file:
            st.success("File uploaded successfully!")
        else:
            st.info("Awaiting file upload.")
            st.stop()

    # --- Data Loading and Caching ---
    @st.cache_data
    def load_data(file):
        """
        Load data from the uploaded file.
        For Excel, it loads all sheets into a dictionary of DataFrames.
        """
        try:
            if file.name.endswith('.csv'):
                return pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                return pd.read_excel(file, sheet_name=None, engine='openpyxl')
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None

    file_data = load_data(uploaded_file)

    if file_data is None:
        st.stop()

    # --- Sheet Selection for Excel Files ---
    df = None
    if isinstance(file_data, dict):
        with st.sidebar:
            sheet_name = st.selectbox("Select a sheet", file_data.keys())
            df = file_data[sheet_name]
    else:
        df = file_data

    # Create a copy for processing to keep the original data intact
    df_processed = df.copy()

    # --- Data Cleaning and Preprocessing in Sidebar ---
    with st.sidebar:
        st.header("2. Data Cleaning & Preprocessing")

        # Handling Missing Values
        st.subheader("Handle Missing Values")
        missing_value_strategy = st.radio(
            "Select strategy",
            ('None', 'Drop Rows with Missing Values', 'Fill with Mean/Median/Mode')
        )

        if missing_value_strategy == 'Drop Rows with Missing Values':
            df_processed.dropna(inplace=True)
            st.write(f"Data shape after dropping missing values: {df_processed.shape}")
        elif missing_value_strategy == 'Fill with Mean/Median/Mode':
            for col in df_processed.columns:
                if df_processed[col].isnull().any():
                    if pd.api.types.is_numeric_dtype(df_processed[col]):
                        fill_value = df_processed[col].mean()
                        # FIX: Replaced inplace=True with direct assignment to avoid FutureWarning
                        df_processed[col] = df_processed[col].fillna(fill_value)
                    else:
                        fill_value = df_processed[col].mode()[0]
                        # FIX: Replaced inplace=True with direct assignment to avoid FutureWarning
                        df_processed[col] = df_processed[col].fillna(fill_value)
            st.write("Missing values have been filled.")

        # Dropping Columns
        st.subheader("Drop Columns")
        columns_to_drop = st.multiselect(
            "Select columns to drop",
            options=df_processed.columns.tolist()
        )
        if columns_to_drop:
            # FIX: Changed to df_processed = ... to ensure the main dataframe is modified
            df_processed = df_processed.drop(columns=columns_to_drop)
            st.write(f"Dropped columns: {', '.join(columns_to_drop)}")
            st.write(f"Data shape after dropping columns: {df_processed.shape}")


    # --- Main Panel for Data Exploration and Visualization ---
    st.header("Data Exploration")

    def to_display_df(df_to_convert):
        """
        FIX: Converts object columns to strings to prevent pyarrow serialization errors
        when using st.dataframe.
        """
        display_df = df_to_convert.copy()
        for col in display_df.columns:
            if display_df[col].dtype == 'object':
                display_df[col] = display_df[col].astype(str)
        return display_df

    # Display basic info in expanders
    with st.expander("Show Raw Data Preview (First 5 Rows)"):
        st.dataframe(to_display_df(df.head()))

    with st.expander("Show Processed Data Preview (First 5 Rows)"):
        st.dataframe(to_display_df(df_processed.head()))

    with st.expander("Show Data Summary"):
        st.write("Shape of Processed DataFrame:", df_processed.shape)
        
        # Use a StringIO buffer to capture the output of df.info()
        buffer = StringIO()
        df_processed.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        
        st.write("Descriptive Statistics:")
        st.write(df_processed.describe())

    with st.expander("Show Missing Value Counts"):
        st.write(df_processed.isnull().sum())

    # --- Data Visualization Section ---
    st.header("Data Visualization")

    # Select plot type
    plot_type = st.selectbox(
        "Select a type of plot",
        [
            "Histogram", "Box Plot", "Scatter Plot",
            "Bar Chart", "Correlation Heatmap"
        ]
    )

    numeric_columns = df_processed.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df_processed.select_dtypes(include=['object', 'category']).columns.tolist()

    # --- Plotting Logic ---
    if plot_type == "Histogram":
        st.subheader("Histogram")
        column = st.selectbox("Select a numerical column", numeric_columns)
        if column:
            bins = st.slider("Number of bins", min_value=5, max_value=100, value=20)
            fig, ax = plt.subplots()
            sns.histplot(df_processed[column], bins=bins, kde=True, ax=ax)
            ax.set_title(f'Histogram of {column}')
            st.pyplot(fig)

    elif plot_type == "Box Plot":
        st.subheader("Box Plot")
        column = st.selectbox("Select a numerical column", numeric_columns)
        if column:
            fig, ax = plt.subplots()
            sns.boxplot(y=df_processed[column], ax=ax)
            ax.set_title(f'Box Plot of {column}')
            st.pyplot(fig)

    elif plot_type == "Scatter Plot":
        st.subheader("Scatter Plot")
        x_axis = st.selectbox("Select the X-axis (numerical)", numeric_columns, index=0 if numeric_columns else -1)
        y_axis_options = [col for col in numeric_columns if col != x_axis]
        y_axis = st.selectbox("Select the Y-axis (numerical)", y_axis_options)
        
        if x_axis and y_axis:
            hue = st.selectbox("Select column for color (categorical, optional)", [None] + categorical_columns)
            hue_data = df_processed[hue] if hue else None
            fig, ax = plt.subplots()
            sns.scatterplot(x=df_processed[x_axis], y=df_processed[y_axis], hue=hue_data, ax=ax)
            ax.set_title(f'Scatter Plot of {x_axis} vs {y_axis}')
            st.pyplot(fig)

    elif plot_type == "Bar Chart":
        st.subheader("Bar Chart")
        cat_column = st.selectbox("Select a categorical column", categorical_columns)
        num_column = st.selectbox("Select a numerical column for the value", numeric_columns)
        if cat_column and num_column:
            fig, ax = plt.subplots()
            agg_data = df_processed.groupby(cat_column)[num_column].mean().sort_values(ascending=False)
            agg_data.plot(kind='bar', ax=ax)
            ax.set_title(f'Average {num_column} by {cat_column}')
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

    elif plot_type == "Correlation Heatmap":
        st.subheader("Correlation Heatmap")
        if not numeric_columns:
            st.warning("No numerical columns available to create a heatmap.")
        else:
            corr_matrix = df_processed[numeric_columns].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            ax.set_title("Correlation Matrix of Numerical Columns")
            st.pyplot(fig)

    # --- Export Summary Report ---
    st.header("Export Summary Report")
    st.write("Download a text file with a summary of the processed data.")

    def generate_summary(dataframe):
        """
        Generates a text-based summary of the DataFrame.
        """
        buffer = StringIO()
        buffer.write("Data Analysis Summary Report\n")
        buffer.write("="*30 + "\n\n")
        buffer.write("1. Data Shape\n")
        buffer.write(f"Number of Rows: {dataframe.shape[0]}\n")
        buffer.write(f"Number of Columns: {dataframe.shape[1]}\n\n")
        buffer.write("2. Data Info\n")
        dataframe.info(buf=buffer)
        buffer.write("\n\n3. Descriptive Statistics\n")
        buffer.write(dataframe.describe().to_string())
        buffer.write("\n\n4. Missing Values Count\n")
        buffer.write(dataframe.isnull().sum().to_string())
        return buffer.getvalue()

    summary_text = generate_summary(df_processed)
    st.download_button(
        label="Download Summary Report",
        data=summary_text,
        file_name="data_summary.txt",
        mime="text/plain"
    )

if __name__ == '__main__':
    main()