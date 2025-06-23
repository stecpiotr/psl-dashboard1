import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard tagów", layout="wide")

# Dane wejściowe
dane = """
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

# Przetwarzanie danych
lines = [l.strip().split() for l in dane.strip().split('\n')]
df = pd.DataFrame(lines, columns=['Tag', 'Count'])
df['Count'] = df['Count'].astype(int)
df = df.sort_values('Count', ascending=False).reset_index(drop=True)
df['% udział'] = (df['Count'] / df['Count'].sum() * 100).round(1)

# Sidebar
st.sidebar.header("Ustawienia dashboardu")
max_tags = min(len(df), 100)
top_n = st.sidebar.slider(
    "Liczba tagów na wykresie (Top N):",
    min_value=5,
    max_value=max_tags,
    value=min(20, max_tags)
)
highlight = st.sidebar.multiselect(
    "Które tagi wyróżnić innym kolorem?",
    options=df['Tag'].tolist(),
    default=["rolnictwo", "zdrowie"]
)
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="Pobierz dane (CSV)",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="tags_popularity.csv",
    mime='text/csv'
)

# Główna część
st.title("📊 Dashboard popularności tagów w odpowiedzi na otwarte pytanie ''Jakimi konkretnymi projektami powinien zająć się PSL w ramach rządu, aby przyczyniło się to do rozwoju Polski?''")
st.caption("Wizualizacja oraz szybka analiza częstości występowania wyrazów-kluczy w dokumentach/projektach. Wykres pozwala szybko wyłapać trendy, potencjalne priorytety oraz punkty zapalne (wyróżnione innym kolorem).")

col1, col2 = st.columns([2,1])

with col1:
    # Przygotuj dane do wykresu
    top = df.head(top_n)
    fig, ax = plt.subplots(figsize=(10, top_n * 0.35 + 1))
    colors = ['#d74a5a' if tag in highlight else '#24ae5f' for tag in top['Tag']]
    bars = ax.barh(top['Tag'], top['Count'], color=colors)
    for i, (cnt, perc) in enumerate(zip(top['Count'], top['% udział'])):
        ax.text(cnt + 2, i, f"{cnt} / {perc}%", va='center', fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Liczba wystąpień")
    ax.set_ylabel("")
    ax.set_title(f"Top {top_n} tagów wg liczby wystąpień")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("**Tabela danych (Top N):**")
    st.dataframe(top[['Tag', 'Count', '% udział']].rename(columns={'Tag': 'Tag', 'Count': 'Liczba', '% udział': '%'}), use_container_width=True)
    st.markdown("> **Tip:** Przeciągnij kolumny lub skopiuj dane bezpośrednio z tabeli do Excela!")

st.markdown("---")
st.write("**Wskazówki**: Możesz dowolnie zmieniać liczbę wyświetlanych tagów oraz wyróżniać je kolorystycznie, aby lepiej zobaczyć obszary wymagające uwagi lub szczególnie istotne dla strategii. Dane możesz też pobrać do dalszej analizy (np. scoring, dashboardy PowerBI, raportowanie zarządcze).")
