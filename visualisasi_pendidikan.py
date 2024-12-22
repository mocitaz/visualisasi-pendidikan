import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Visualisasi Data Pendidikan", page_icon="📊", layout="wide")

# Header dengan Logo
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0;">📊 Visualisasi Data Pendidikan SD Indonesia 2023-2024</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Deskripsi Proyek
st.markdown(
    """ 
    ### 🎓 Final Project Visualisasi Data 
    **Kelompok 5**
    - **Fadhil Muhamad**
    - **Luthfi Fauzi**

    Proyek ini bertujuan untuk memberikan wawasan mendalam tentang kondisi pendidikan SD di Indonesia selama tahun ajaran 2023-2024. 
    Dengan memanfaatkan Streamlit dan Plotly, kami menyediakan fitur interaktif seperti:
    - Filter Data Berdasarkan Provinsi, Tahun, dan Jumlah Siswa
    - Visualisasi Multi-Indikator (Bar Chart, Pie Chart, Box Plot, Line Chart, Histogram, Scatter Plot)
    - Heatmap Korelasi Antar Variabel
    - Highlight Data dan Statistik Ringkas
    - Tabel Interaktif dan Statistik Deskriptif
    - Fitur Download Dataset

    Aplikasi ini diharapkan dapat mendukung pengambilan keputusan yang berbasis data untuk meningkatkan kualitas pendidikan di Indonesia.
    """
)

# Membaca dataset
@st.cache_data
def load_data():
    return pd.read_csv("data_pendidikan_cleaned.csv")

df = load_data()

# Sidebar untuk Multi-Filter
st.sidebar.header("📊 Filter Data")
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

# Filter Tahun
if 'Tahun' in df.columns:
    tahun = st.sidebar.slider(
        "Pilih Tahun",
        int(df["Tahun"].min()), int(df["Tahun"].max()),
        (int(df["Tahun"].min()), int(df["Tahun"].max()))
    )
    filtered_df = df[
        (df["Provinsi"].isin(provinsi)) &
        (df["Siswa"] >= min_siswa) &
        (df["Siswa"] <= max_siswa) &
        (df["Tahun"] == tahun)
    ]
else:
    filtered_df = df[
        (df["Provinsi"].isin(provinsi)) &
        (df["Siswa"] >= min_siswa) &
        (df["Siswa"] <= max_siswa)
    ]

# Sidebar Statistik Ringkas
st.sidebar.header("📊 Statistik Ringkas")
st.sidebar.metric("Total Siswa", f"{filtered_df['Siswa'].sum():,}")
st.sidebar.metric("Jumlah Sekolah", f"{filtered_df['Sekolah'].sum():,}")
st.sidebar.metric("Rata-rata Ruang Kelas Baik", f"{filtered_df['Ruang kelas(baik)'].mean():.2f}")

# Filter Multi-Kriteria
st.sidebar.header("Pilih Indikator Visualisasi")
indikator = st.sidebar.multiselect(
    "Pilih Indikator untuk Visualisasi",
    options=["Sekolah", "Siswa", "Ruang kelas(baik)", "Ruang kelas(rusak ringan)", "Ruang kelas(rusak sedang)", "Ruang kelas(rusak berat)"],
    default=["Sekolah", "Siswa"]
)

# Highlight Provinsi
highlight_provinsi = st.sidebar.multiselect(
    "Sorot Provinsi (Highlight)",
    options=df["Provinsi"].unique(),
    default=[]  # Tidak ada sorotan secara default
)

# Validasi jika data kosong
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter. Silakan ubah filter atau reset pilihan.")
else:
    # Visualisasi Multi-Indikator per Provinsi
    st.subheader("📊 Visualisasi Multi-Indikator per Provinsi")
    for col in indikator:
        fig = px.bar(
            filtered_df, 
            x="Provinsi", 
            y=col, 
            title=f"{col} per Provinsi",
            color=col,
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"Visualisasi ini menunjukkan jumlah **{col}** per Provinsi. Data ini berguna untuk menganalisis distribusi {col} di seluruh Indonesia.")

    # Highlight Data
    if highlight_provinsi:
        highlighted_df = filtered_df[filtered_df["Provinsi"].isin(highlight_provinsi)]
        fig_highlight = px.bar(
            highlighted_df,
            x="Provinsi",
            y="Siswa",
            title="Highlight Jumlah Siswa untuk Provinsi Terpilih",
            color="Provinsi"
        )
        st.plotly_chart(fig_highlight, use_container_width=True)
        st.write("Grafik ini menyoroti jumlah siswa di provinsi tertentu yang dipilih.")

    # Box Plot untuk Sebaran Siswa
    st.subheader("📦 Sebaran Siswa per Provinsi")
    fig_box = px.box(
        filtered_df, 
        x="Provinsi", 
        y="Siswa", 
        title="Sebaran Jumlah Siswa per Provinsi"
    )
    st.plotly_chart(fig_box, use_container_width=True)
    st.write("Box plot ini menunjukkan distribusi jumlah siswa di setiap provinsi. Ini membantu memahami nilai minimum, maksimum, median, dan outliers.")

    # Line Chart Tren Jumlah Sekolah dan Siswa
    st.subheader("📈 Tren Jumlah Sekolah dan Siswa")
    fig_line = px.line(
        filtered_df,
        x="Provinsi",
        y=["Sekolah", "Siswa"],
        title="Tren Jumlah Sekolah dan Siswa per Provinsi",
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.write("Grafik ini menggambarkan tren jumlah sekolah dan siswa di berbagai provinsi, membantu memahami perubahan jumlah sekolah dan siswa.")

    # Histogram Distribusi Siswa
    st.subheader("📊 Histogram Distribusi Jumlah Siswa")
    fig_hist = px.histogram(
        filtered_df, 
        x="Siswa", 
        nbins=20, 
        title="Distribusi Jumlah Siswa",
        color_discrete_sequence=["blue"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.write("Histogram ini menggambarkan distribusi jumlah siswa, memberikan wawasan tentang frekuensi berbagai jumlah siswa.")

    # Scatter Plot Dinamis
    st.subheader("🔍 Hubungan Antar Variabel")
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
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.write(f"Scatter plot ini menunjukkan hubungan antara variabel **{x_axis}** dan **{y_axis}**, dengan ukuran titik berdasarkan jumlah siswa.")

    # Heatmap Korelasi Antar Variabel Numerik
    st.subheader("🔥 Korelasi Antar Variabel")
    corr_matrix = filtered_df.select_dtypes(include="number").corr()
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale="Viridis"
    ))
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.write("Heatmap ini membantu menganalisis hubungan antar variabel numerik untuk mengidentifikasi pola yang signifikan.")

    # Treemap Visualisasi
    st.subheader("📊 Treemap Distribusi Siswa per Provinsi")
    fig_treemap = px.treemap(
        filtered_df,
        path=["Provinsi"],
        values="Siswa",
        title="Treemap Distribusi Siswa per Provinsi"
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
    st.write("Treemap ini memberikan gambaran visual tentang distribusi jumlah siswa di setiap provinsi dengan ukuran area mewakili jumlah siswa.")

    # Stacked Bar Chart
    st.subheader("📊 Stacked Bar Chart: Jumlah Siswa Berdasarkan Kondisi Ruang Kelas")
    fig_stacked = px.bar(
        filtered_df,
        x="Provinsi",
        y=["Ruang kelas(baik)", "Ruang kelas(rusak ringan)", "Ruang kelas(rusak sedang)", "Ruang kelas(rusak berat)"],
        title="Jumlah Siswa Berdasarkan Kondisi Ruang Kelas per Provinsi",
        labels={"value": "Jumlah Siswa", "variable": "Kondisi Ruang Kelas"},
        text_auto=True
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

    # Violin Plot
    st.subheader("📊 Violin Plot: Distribusi Jumlah Siswa per Provinsi")
    fig_violin = px.violin(
        filtered_df, 
        x="Provinsi", 
        y="Siswa", 
        box=True, 
        points="all", 
        title="Distribusi Jumlah Siswa per Provinsi"
    )
    st.plotly_chart(fig_violin, use_container_width=True)

    # Pair Plot
    st.subheader("📊 Pair Plot: Hubungan Antar Variabel")
    sns.set(style="ticks")
    pairplot = sns.pairplot(filtered_df.select_dtypes(include=["number"]))
    st.pyplot(pairplot)
    st.write("Pair plot ini menunjukkan hubungan antar berbagai variabel numerik.")

    # Bubble Chart
    st.subheader("🔵 Bubble Chart: Jumlah Siswa per Provinsi")
    fig_bubble = px.scatter(
        filtered_df,
        x="Provinsi",
        y="Ruang kelas(baik)",
        size="Siswa",
        color="Provinsi",
        title="Bubble Chart: Jumlah Siswa per Provinsi",
        hover_name="Provinsi"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# Tabel Interaktif Data Pendidikan dan Statistik Deskriptif
st.subheader("📋 Tabel Interaktif Data Pendidikan")
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_side_bar()
grid_options = gb.build()
AgGrid(filtered_df, gridOptions=grid_options)
st.write("Tabel interaktif ini memungkinkan eksplorasi data secara langsung, termasuk pencarian dan pengurutan data.")

st.subheader("📊 Statistik Deskriptif Dataset")
statistik_provinsi = filtered_df.groupby("Provinsi").sum(numeric_only=True).reset_index()
st.dataframe(statistik_provinsi)
st.write("Tabel ini menunjukkan statistik deskriptif, seperti jumlah total siswa, sekolah, dan kondisi ruang kelas.")

# Footer dengan Kesimpulan
st.markdown(
    """
    ### 📚 Kesimpulan
    Proyek ini memberikan wawasan yang mendalam mengenai kondisi pendidikan di tingkat Sekolah Dasar (SD) di Indonesia selama tahun ajaran 2023-2024. Dengan memanfaatkan teknologi visualisasi data interaktif menggunakan **Streamlit** dan **Plotly**, pengguna dapat dengan mudah memahami distribusi jumlah siswa, kondisi ruang kelas, serta jumlah sekolah di setiap provinsi di Indonesia.

    Fitur-fitur yang ada dalam aplikasi ini, seperti filter berdasarkan provinsi, tahun, dan jumlah siswa, serta visualisasi berbagai jenis grafik dan korelasi antar variabel, memberikan pemahaman yang lebih baik mengenai pola-pola yang ada dalam pendidikan SD. Pengguna juga dapat mengunduh dataset yang digunakan untuk analisis lebih lanjut dan mengambil keputusan berbasis data.

    Dengan adanya visualisasi ini, diharapkan dapat memberikan informasi yang bermanfaat untuk pengambil kebijakan, peneliti, dan masyarakat umum dalam upaya meningkatkan kualitas pendidikan di Indonesia.
    """,
    unsafe_allow_html=True
)

# Fitur Download Dataset
st.subheader("📥 Download Dataset")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV", data=csv, file_name="data_pendidikan_cleaned.csv", mime="text/csv")

# Catatan Footer
st.caption("Catatan: Dataset Pendidikan SD Indonesia 2023-2024 | Dibuat dengan Streamlit dan Plotly")
