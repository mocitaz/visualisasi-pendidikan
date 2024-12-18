import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder

# Membaca data CSV
st.title("Visualisasi Data Pendidikan SD Indonesia 2023-2024")
data_path = "data_pendidikan_cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(data_path)

df = load_data()

# Sidebar untuk Multi-Filter
st.sidebar.header("Filter Data")
provinsi = st.sidebar.multiselect(
    "Pilih Provinsi",
    options=df["Provinsi"].unique(),
    default=df["Provinsi"].unique()
)

# Filter Range Numerik
min_siswa, max_siswa = st.sidebar.slider(
    "Filter Jumlah Siswa (Range)",
    int(df["Siswa"].min()), int(df["Siswa"].max()),
    (int(df["Siswa"].min()), int(df["Siswa"].max()))
)

# Filter Multi-Kriteria
filtered_df = df[
    (df["Provinsi"].isin(provinsi)) &
    (df["Siswa"] >= min_siswa) &
    (df["Siswa"] <= max_siswa)
]

# Dropdown Multi-Visualisasi
st.sidebar.header("Pilih Indikator Visualisasi")
indikator = st.sidebar.multiselect(
    "Pilih Indikator untuk Visualisasi",
    options=[
        "Sekolah", "Siswa", "Ruang kelas(baik)", 
        "Ruang kelas(rusak ringan)", "Ruang kelas(rusak sedang)", 
        "Ruang kelas(rusak berat)"
    ],
    default=["Sekolah", "Siswa"]
)

# Visualisasi Dinamis Berdasarkan Indikator
st.subheader("Visualisasi Multi-Indikator per Provinsi")
for col in indikator:
    fig = px.bar(
        filtered_df, 
        x="Provinsi", 
        y=col, 
        title=f"{col} per Provinsi",
        color=col,
        text_auto=True
    )
    st.plotly_chart(fig)

# Visualisasi Line Chart Tren
st.subheader("Tren Jumlah Sekolah dan Siswa per Provinsi")
fig_line = px.line(
    filtered_df,
    x="Provinsi",
    y=["Sekolah", "Siswa"],
    title="Tren Jumlah Sekolah dan Siswa",
    markers=True
)
st.plotly_chart(fig_line)

# Heatmap Korelasi Antar Variabel Numerik
st.subheader("Heatmap Korelasi Variabel Numerik")
corr_matrix = filtered_df.select_dtypes(include="number").corr()
fig_heatmap = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale="Viridis"
))
st.plotly_chart(fig_heatmap)

# Scatter Plot Dinamis
st.subheader("Hubungan Antar Variabel")
x_axis = st.selectbox("Pilih Variabel untuk Sumbu X", options=filtered_df.select_dtypes(include="number").columns)
y_axis = st.selectbox("Pilih Variabel untuk Sumbu Y", options=filtered_df.select_dtypes(include="number").columns)

fig_scatter = px.scatter(
    filtered_df,
    x=x_axis,
    y=y_axis,
    size="Siswa",
    color="Provinsi",
    title=f"Scatter Plot: {x_axis} vs {y_axis}"
)
st.plotly_chart(fig_scatter)

# Tabel Interaktif Menggunakan AgGrid
st.subheader("Tabel Interaktif Data Pendidikan")
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_side_bar()
grid_options = gb.build()
AgGrid(filtered_df, gridOptions=grid_options)

# Statistik Deskriptif Per Provinsi
st.subheader("Statistik Deskriptif Dataset")
statistik_provinsi = filtered_df.groupby("Provinsi").sum(numeric_only=True).reset_index()
st.dataframe(statistik_provinsi)

# Footer
st.caption("Data: Dataset Pendidikan SD Indonesia 2023-2024 | Dibuat dengan Streamlit dan Plotly")
