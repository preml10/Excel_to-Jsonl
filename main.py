import streamlit as st
import pandas as pd
import json
from io import StringIO, BytesIO

st.title("📘 Excel/CSV → JSONL Converter")

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    try:
        # Detect file type
        if uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            st.error("❌ Unsupported file type! Please upload .xlsx, .xls, or .csv.")
            st.stop()

        # Handle empty file
        if df.empty:
            st.warning("⚠️ The file is empty. Please upload a file with data.")
            st.stop()

        # Convert Timestamps and other non-serializable objects
        df = df.applymap(lambda x: x.isoformat() if hasattr(x, "isoformat") else x)

        # Convert to JSONL
        jsonl_str = "\n".join(
            df.apply(lambda row: json.dumps(row.to_dict(), ensure_ascii=False), axis=1)
        )

        st.success("✅ Successfully converted!")

        # Preview
        st.subheader("🔍 Preview of Converted JSONL")
        st.code("\n".join(jsonl_str.splitlines()[:5]))

        # Create downloadable file
        jsonl_bytes = StringIO(jsonl_str).getvalue().encode("utf-8")
        st.download_button(
            label="⬇️ Download JSONL File",
            data=jsonl_bytes,
            file_name=uploaded_file.name.rsplit(".", 1)[0] + ".jsonl",
            mime="application/json"
        )

        

    except Exception as e:
        st.error(f"❌ Conversion failed: {str(e)}")

else:
    st.info("📤 Please upload an Excel or CSV file to start.")
