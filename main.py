import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="file Converter and cleaner", layout="wide")
st.title("📁File Converter and cleaner")
st.write("Upload your CVS and EXCEL files to convert them between formats.")
 
files = st.file_uploader("Upload your file", type=["csv", "xlsx", "xls"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split('.')[-1]
        df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)

    st.subheader(f"Preview of {file.name}")
    st.dataframe(df.head())

    if st.checkbox(f"fill missing values in {file.name}"):
        df.fillna(df.select_dtypes(include='number').mean(),inplace=True)
        st.success("Missing values filled using forward fill method.")
        st.dataframe(df.head())

        select_coloums = st.multiselect(f"Select columns to drop from {file.name}", df.columns ,default=df.columns)
        df = df[select_coloums]
        st.dataframe(df.head())

        if st.checkbox(f"show chart - {file.name}") and not df.select_dtypes(include='number').empty:
            chart = st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        format_choice = st.radio(f"convert {file.name} to:", ['CSV', 'Excel'], key=file.name)

        if st.button(f"⬇️Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == 'csv':
                df.to_csv(output, index=False)
                mime = 'text/csv'
                new_name = file.name.replace(ext, 'csv')
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                new_name = file.name.replace(ext, 'xlsx')
                output.seek(0)
                st.download_button("⬇️ Download file", data=output, file_name=new_name, mime=mime)
                st.success("conversion successful!") 