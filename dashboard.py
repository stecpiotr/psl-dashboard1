import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import io

st.set_page_config(page_title="PSL – Dashboard popularności słów", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 60px !important;
        overflow: visible !important;
    }
    @media (max-width: 700px) {
        .block-container {
            padding-top: 102px !important;   /* więcej luzu pod belką Streamlit */
        }
    }
    @media (max-width: 500px) {
        .block-container {
            padding-top: 80px !important;
        }
    }
    .psl-logo-title-row {
        display: flex;
        align-items: center;
        gap: 32px;
        margin-bottom: 0.5em;
        flex-wrap: wrap;
    }
    .psl-logo-img {
        height: 56px;
        width: auto;
        max-width: 140px;
        object-fit: contain;
        display: block;
        margin-right: 4px;
    }
    @media (max-width: 700px) {
        .psl-logo-title-row {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 0 !important;
        }
        .psl-logo-img {
            height: 38px !important;
            max-width: 80vw !important;
            width: auto !important;
            margin-bottom: 15px;
        }
        .psl-title {
            font-size: 1.28rem !important;
            line-height: 1.13 !important;
        }
    }
    @media (max-width: 420px) {
        .psl-logo-img {
            height: 24px !important;
            max-width: 64vw !important;
        }
        .psl-title {
            font-size: 0.98rem !important;
        }
    }
    .psl-title {
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0.08em;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        line-height: 2;
        word-break: break-word;
    }
    .psl-subtitle {
        font-size: 1.22rem;
        color: #444;
        margin-top: 0.3em;
        margin-bottom: 1.5em;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        line-height: 1.35;
        font-weight: 500;
    }
    /* Tabela ... (reszta bez zmian) */
    .dynamic-psl-table { width: 100%; border-collapse: collapse; font-size: 0.91em; }
    .dynamic-psl-table th { background-color: #fafafa; text-align: center; }
    .dynamic-psl-table td, .dynamic-psl-table th {
        padding: 4px 6px 4px 6px !important;
    }
    .dynamic-psl-table tr.highlight-row { background-color: #ffe1ba !important; }
    .dynamic-psl-table td.center { text-align: center !important; }
    .dynamic-psl-table td.bold { font-weight: bold; }
    .dynamic-psl-table td.lp-col, .dynamic-psl-table th.lp-col {
        width: 18px !important;
        min-width: 14px !important;
        max-width: 22px !important;
        text-align: center !important;
        padding-left: 1px !important;
        padding-right: 1px !important;
    }
    .dynamic-psl-table td.slowo-col, .dynamic-psl-table th.slowo-col {
        width: 66px !important;
        min-width: 36px !important;
        max-width: 90px !important;
        text-align: left !important;
        padding-left: 6px !important;
        padding-right: 6px !important;
    }
    .dynamic-psl-table td.liczba-col, .dynamic-psl-table th.liczba-col,
    .dynamic-psl-table td.proc-col, .dynamic-psl-table th.proc-col {
        width: 44px !important;
        min-width: 28px !important;
        max-width: 55px !important;
        text-align: center !important;
        padding-left: 3px !important;
        padding-right: 3px !important;
    }
    .stDownloadButton { margin-top: 12px; }
    </style>
""", unsafe_allow_html=True)

# ----------- LOGO + TYTUŁ -----------
st.markdown(
    """
    <div class="psl-logo-title-row">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Polnische_Bauernpartei_%28PSL%29_Logo.svg/509px-Polnische_Bauernpartei_%28PSL%29_Logo.svg.png"
             class="psl-logo-img" alt="Logo PSL"/>
        <span class="psl-title">
            <span style='color:#18b46e'>PSL</span> – dashboard popularności <span style='color:#ff6c25'>słów</span>
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="psl-subtitle" style="font-size:1.12rem;">
        Dashboard popularności tagów w odpowiedzi na otwarte pytanie<br>
        <span style="color:#666;font-style:italic;font-weight:400">
        "Jakimi konkretnymi projektami powinien zająć się PSL w ramach rządu, aby przyczyniło się to do rozwoju Polski?"
        </span>
    </div>
    """, unsafe_allow_html=True
)

# ----------- DANE WEJŚCIOWE -----------
tags_data = """
podatek 237
rozwój 222
polski 200
rolnictwo 192
PSL 176
mieć 169
zdrowie 161
młody 154
mały 143
rolnik 141
program 138
projekt 135
wsparcie 135
kwota 134
człowiek 132
wolna 126
przedsiębiorca 126
Polska 119
ustawa 113
samorząd 112
budowa 111
powinien 110
gospodarka 109
wieś 105
PiS 104
bezpieczeństwo 103
lokalny 103
ochrona 103
praca 96
służba 91
duży 87
energia 86
zmiana 85
mieszkanie 85
wiejski 85
składka 84
zwiększyć 83
infrastruktura 83
zdrowotny 79
bardzo 77
edukacja 75
inwestycja 69
gmina 68
sprawa 68
CPK 66
wprowadzić 66
zielony 64
rząd 63
rolny 62
cena 62
ład 62
kredyt 62
nowy 62
reforma 62
obniżyć 61
gospodarczy 60
państwo 60
firma 59
obronność 59
czas 59
inny 58
droga 58
kraj 57
musieć 57
osoba 57
partia 57
działanie 55
podatkowy 55
system 54
społeczny 54
szkoła 53
obszar 52
wspierać 51
elektrownia 51
mieszkaniowy 51
emerytura 51
wybory 50
prawo 50
średni 49
produkcja 47
polityka 46
poprawa 46
zakres 46
koalicja 46
miasto 44
rodzina 44
życie 44
trzeba 43
dobry 43
pracować 42
dziecko 42
energetyczny 41
uprościć 40
atomowa 40
społeczeństwo 40
energetyka 39
związek 39
działalność 39
zmniejszyć 39
kobieta 39
"""

# ----------- PRZETWARZANIE DANYCH -----------
lines = [l.strip().split() for l in tags_data.strip().split('\n')]
tags_df = pd.DataFrame(lines, columns=['Tag', 'Count'])
tags_df['Count'] = tags_df['Count'].astype(int)
tags_df = tags_df.sort_values('Count', ascending=False).reset_index(drop=True)
tags_df['% udział'] = (tags_df['Count'] / tags_df['Count'].sum() * 100).round(1)

# ----------- SIDEBAR -----------
st.sidebar.header("Filtry")
max_tags = min(len(tags_df), 100)
top_n = st.sidebar.slider("Liczba najczęstszych słów (TOP N):", min_value=5, max_value=max_tags, value=min(20, max_tags))
highlight = st.sidebar.multiselect(
    "Wyróżnij słowa (kolor pomarańczowy):",
    options=tags_df['Tag'].tolist(),
    default=["rolnictwo", "podatek"]
)
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="Pobierz dane (CSV)",
    data=tags_df.to_csv(index=False).encode('utf-8'),
    file_name="tags_popularity.csv",
    mime='text/csv'
)

# ----------- WYKRES PLOTLY -----------
top_tags_df = tags_df.head(top_n).copy()
labels = [f"{c} / {p}%" for c, p in zip(top_tags_df['Count'], top_tags_df['% udział'])]
bar_colors = [
    "#ff9a36" if tag in highlight else "#18b46e"
    for tag in top_tags_df['Tag']
]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=top_tags_df['Count'][::-1],
    y=top_tags_df['Tag'][::-1],
    orientation='h',
    marker=dict(
        color=bar_colors[::-1],
        line=dict(width=0),
    ),
    text=labels[::-1],
    textposition='inside',
    insidetextanchor='middle',
    hovertemplate="<b>%{y}</b><br>Liczba: %{x}<br>Udział: %{text}<extra></extra>",
    width=0.7,
    opacity=0.93
))

# --- Ustaw ticki główne co 50, delikatną siatkę co 25 ---
fig.update_xaxes(
    tickvals=list(range(0, int(top_tags_df['Count'].max())+51, 50)),
    ticklen=13,
    showline=True,
    linecolor="#cfcfcf",
    linewidth=1.2,
    showgrid=True,
    gridcolor="#f1f1f1",
    gridwidth=1,
    dtick=25,   # grid co 25
    ticks="outside",
    side="top",
    tickfont=dict(size=14, color="#aaaaaa"),
    zeroline=False
)
fig.update_yaxes(
    showgrid=False,
    tickfont=dict(size=16, color="#111"),
    ticks="outside",
    ticklen=8,
    showline=True,
    linecolor="#cfcfcf",
    linewidth=1.2,
    automargin=True
)

fig.update_layout(
    bargap=0.14,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Montserrat,Segoe UI,sans-serif", size=15),
    height=top_n*32 + 110,
    margin=dict(l=18, r=28, t=80, b=10),
    showlegend=False,
    xaxis_title="Liczba wystąpień"
)

# ----------- UKŁAD 2 KOLUMN (WYKRES + TABELA) -----------

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col2:
    table_df = top_tags_df[['Tag', 'Count', '% udział']].rename(
        columns={'Tag': 'Słowo', 'Count': 'Liczba', '% udział': '%'}
    ).copy()
    table_df.insert(0, "L.p.", range(1, len(table_df) + 1))
    table_df = table_df.sort_values('Liczba', ascending=False).reset_index(drop=True)
    table_df['%'] = table_df['%'].map(lambda x: '{:.1f}'.format(float(x)).replace(",", "."))

    def make_html_table(df, highlight_tags):
        html = '<table class="dynamic-psl-table">'
        html += "<tr>"
        html += f'<th class="lp-col">L.p.</th>'
        html += f'<th class="slowo-col">Słowo</th>'
        html += f'<th class="liczba-col">Liczba</th>'
        html += f'<th class="proc-col">%</th>'
        html += "</tr>"
        for _, row in df.iterrows():
            is_highlight = str(row['Słowo']) in highlight_tags
            row_class = "highlight-row" if is_highlight else ""
            html += f'<tr class="{row_class}">'
            html += f'<td class="center lp-col">{row["L.p."]}</td>'
            html += f'<td class="bold slowo-col">{row["Słowo"]}</td>'
            html += f'<td class="center liczba-col">{row["Liczba"]}</td>'
            html += f'<td class="center proc-col">{row["%"]}</td>'
            html += '</tr>'
        html += '</table>'
        return html

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        table_df.to_excel(writer, sheet_name="Dane", index=False)
    excel_buffer.seek(0)
    excel_data = excel_buffer.getvalue()

    st.markdown(
        "<div style='margin-bottom: 0.65em; margin-down:0.5em; font-size:1.15rem; font-weight:600'>⬇️ Zobacz dane tabelaryczne (Top N)</div>",
        unsafe_allow_html=True)
    st.markdown(make_html_table(table_df, highlight), unsafe_allow_html=True)
    st.download_button(
        label="📥 Pobierz jako Excel (.xlsx)",
        data=excel_data,
        file_name="tags_popularity.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown(
    "<div style='margin-top:3.5em; font-size:1.05rem; color:#18b46e; font-weight:500;'>"
    "Wizualizacja do strategicznych analiz, prezentacji zarządczych i budowania przewagi PSL.<br>"
    "<span style='color:#ff6c25'>Zaprojektowano przez: Piotr Stec, Badania.pro®.</span></div>",
    unsafe_allow_html=True
)
