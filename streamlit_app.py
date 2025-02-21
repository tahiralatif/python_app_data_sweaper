
# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our App
st.set_page_config(page_title="📂 Data Sweeper", layout="wide")

st.markdown(
    """
    <h1 style="text-align: center; color: #4CAF50;">🧹 Data Sweeper</h1>
    <h3 style="text-align: center; color: #FF5722;">Created by Tahira</h3>
    <p style="text-align: center; font-size: 18px;">🔄 <b>Easily convert and clean your CSV & Excel files with built-in data visualization!</b></p>
    <hr style="border: 1px solid #ddd;">
    """,
    unsafe_allow_html=True
)

# # App Title & Description
# st.title("🧹 Data Sweeper")
# st.write("🔄 **Easily convert and clean your CSV & Excel files with built-in data visualization!**")

# File Upload Section
uploaded_files = st.file_uploader(
    "📤 Upload your files (CSV or Excel formats):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Load file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display File Info
        st.write(f"📄 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {len(file.getvalue()) / 1024:.2f} KB")

        # Show preview of DataFrame
        st.subheader("👀 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧼 Data Cleaning Options")
        if st.checkbox(f" Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates()
                    st.write("✅ **Duplicates removed!**")

            with col2:
                if st.button(f"🛠 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ **Missing values has been fixed **")

            # Column Selection
            st.subheader("📌 Select Columns to Keep")
            selected_columns = st.multiselect(f"Columns for {file.name}", df.columns, default=df.columns)
            df = df[selected_columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📉 Show visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # File Conversion Options
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"])

            if st.button(f"📥 Convert {file.name}"):
                buffer = BytesIO()

                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                # Download Button
                st.download_button(
                    label=f"🔽 Download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

                st.success("✅ **File successfully converted and ready for download!**")