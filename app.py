import gradio as gr
import pandas as pd

header_keyword = "JOURNAL SOURCE"

def merge_excel(files):
    cleaned_dataframes = []

    for file in files:
        for i in range(20):
            try:
                df_try = pd.read_excel(file, skiprows=i, engine="openpyxl")
                if header_keyword in df_try.columns:
                    cleaned_dataframes.append(df_try)
                    break
            except Exception as e:
                print(f"Error reading file: {e}")
                break

    if cleaned_dataframes:
        merged_df = pd.concat(cleaned_dataframes, ignore_index=True)
        return merged_df
    else:
        return pd.DataFrame()

demo = gr.Interface(
    fn=merge_excel,
    inputs=gr.File(file_types=[".xlsx"], label="Upload Excel Files", type="file", multiple=True),
    outputs="dataframe",
    title="Excel Merger Tool"
)

demo.launch()
