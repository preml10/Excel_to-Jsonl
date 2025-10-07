import pandas as pd
import json
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Excel to JSONL Converter", page_icon="📘")

st.title("📘 Excel to JSONL Converter")


uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

def safe_convert(value):
   
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, (list, dict, str, int, float, bool, type(None))):
        return value
    return str(value)

if uploaded_file is not None:
    try:
        
        df = pd.read_excel(uploaded_file)

        if df.empty:
            st.error("❌ The Excel file is empty. Please upload a valid file.")
        else:
            st.success(f"✅ File loaded successfully with {len(df)} rows and {len(df.columns)} columns.")

           
            df = df.applymap(safe_convert)

           
            jsonl_data = "\n".join(df.apply(lambda row: json.dumps(row.to_dict(), ensure_ascii=False), axis=1))

         
            st.subheader("🔍 Preview of Converted JSONL")
            st.code("\n".join(jsonl_data.splitlines()[:5]))

          
            st.download_button(
                label="⬇️ Download JSONL File",
                data=jsonl_data.encode("utf-8"),
                file_name="converted.jsonl",
                mime="application/json"
            )

    except Exception as e:
        st.error(f"⚠️ Error during conversion: {e}")
else:
    st.info("👆 Please upload an Excel file to begin.")
