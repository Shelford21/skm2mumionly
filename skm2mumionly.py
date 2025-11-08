import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

url = "https://docs.google.com/spreadsheets/d/1dK2tKeeRGAiVc6p0guapTITane-NckvuAFB3rrHu3k8/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, worksheet="1750077145")

name= conn.read(spreadsheet=url, worksheet="1750077145")

# Safely slice rows B6:B27 (column index 1 since A=0, B=1)
if name.shape[1] >= 2:  # ensure at least 2 columns exist
    names = name.iloc[5:27, 1].dropna().astype(str).tolist()  # B6–B27
else:
    names = []

# Show dropdown
if names:
    selected_name = st.selectbox("Select a name:", names)
    st.write(f"You selected: **{selected_name}**")
else:
    st.warning("No names found in range B6:B27.")


st.dataframe(data)

# File to store submissions
CSV_FILE = "submissions.csv"
# Set your admin password here
ADMIN_PASSWORD = "mumi99"

st.set_page_config(page_title="Mumi Sukamulya 2",
                   page_icon="✨",
                   layout="wide")

st.markdown(
        """
        <div class="transparent-container">
            <h1>✨ Mumi SKM 2</h1>
            <h4>
            يٰٓاَيُّهَا الَّذِيْنَ اٰمَنُوْٓا اِنْ تَنْصُرُوا اللّٰهَ يَنْصُرْكُمْ وَيُثَبِّتْ اَقْدَامَكُمْ <br><br> 💡"Wahai orang-orang yang beriman, jika kamu menolong (agama) Allah, niscaya Dia akan menolongmu dan meneguhkan kedudukanmu" QS 47 ayat 7 <br><br>INFO:<br>mumi skm 2 only ok<br>skm 1 dan 3 skip aja gaperlu pakai web ini 🔎
    </h4>
    
        """,
        unsafe_allow_html=True
    )

# Text input
user_input = st.text_input("Ketik nama: (contoh: fauzan / bagas ijin kerja / rehan sakit demam)")

# Submit button
if st.button("Submit"):
    if user_input.strip() == "":
        st.warning("Tidak boleh kosong ok!")
    else:
        # Load or create dataframe
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
        else:
            df = pd.DataFrame(columns=["Text"])

        # Add new submission
        new_row = pd.DataFrame({"Text": [user_input]})
        df = pd.concat([df, new_row], ignore_index=True)

        # Save to CSV
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ جَزَاكُمُ اللهُ خَيْرًا")

# Display current submissions
if os.path.exists(CSV_FILE):
    st.subheader("Kehadiran hari ini:")
    df_display = pd.read_csv(CSV_FILE)

    # Function to censor from second word onward
    def censor_from_second_word(text):
        words = str(text).split()
        if len(words) > 1:
            censored = [words[0]] + ["*" * len(w) for w in words[1:]]
            return " ".join(censored)
        else:
            return text

    df_display["Absen"] = df_display["Text"].apply(censor_from_second_word)
    st.dataframe(df_display[["Absen"]])

# Divider
st.markdown("---")

# Admin section
st.subheader("Khusus Admin")

# Ask for password first
admin_password = st.text_input("Masukan password untuk menggunakan fitur:", type="password")

# If password is correct, show expander
if admin_password == ADMIN_PASSWORD:
    with st.expander("🧹 Clear all data"):
        if st.button("Clear Data"):
            if os.path.exists(CSV_FILE):
                os.remove(CSV_FILE)
                st.success("✅ All data cleared successfully!")
            else:
                st.info("No data file found to clear.")
    with st.expander("🚀 Download data absen"):
        st.download_button(
            label="⬇️ Unduh absen ok",
            data=df_display.to_csv(index=False).encode('utf-8'),
            file_name="submissions.csv",
            mime="text/csv"
    )
else:
    if admin_password != "":
        st.error("❌ Incorrect password.")































