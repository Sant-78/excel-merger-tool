import streamlit as st
import pandas as pd
import glob
import os

st.title("Excel Merger Tool")

# Step 1: User inputs folder path
folder_path = st.text_input("Enter the folder path containing Excel files")

if folder_path:
    excel_files = glob.glob(os.path.join(folder_path, "*.xls*"))
    st.write(f"Found {len(excel_files)} Excel files.")

    header_keyword = "JOURNAL SOURCE"

    def read_clean_excel(file_path):
        for i in range(20):  # check first 20 rows
            try:
                ext = os.path.splitext(file_path)[1]
                engine = "openpyxl" if ext == ".xlsx" else "xlrd"
                df_try = pd.read_excel(file_path, skiprows=i, engine=engine)
                if header_keyword in df_try.columns:
                    return df_try
            except Exception as e:
                st.error(f"Error reading {file_path}: {e}")
                break
        st.warning(f"Header not found in file: {file_path}")
        return pd.DataFrame()

    cleaned_dataframes = []
    for file in excel_files:
        st.write(f"📄 Processing: {os.path.basename(file)}")
        df = read_clean_excel(file)
        if not df.empty:
            cleaned_dataframes.append(df)

    if cleaned_dataframes:
        merged_df = pd.concat(cleaned_dataframes, ignore_index=True)
        st.success("✅ All files cleaned and merged successfully!")
        st.dataframe(merged_df)

        # Save merged file
        merged_file = "merged_capri_gl_dump.xlsx"
        merged_df.to_excel(merged_file, index=False)

        # Download button
        with open(merged_file, "rb") as f:
            st.download_button("Download Merged Excel", f, file_name=merged_file)
    else:
        st.error("❌ No valid data found to merge.")
