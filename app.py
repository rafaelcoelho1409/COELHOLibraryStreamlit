import streamlit as st
import pandas as pd
import re
import uuid
from functions import (
    image_carousel,
    view_more_details
)

# Load the catalog data
catalog = pd.read_csv("catalog.csv")
catalog = catalog[catalog['sold_out'] == 'No']

# Set up the Streamlit app
st.set_page_config(page_title = "COELHO Library", layout = "wide")


# Navbar
st.markdown(
    """
    <style>
    .navbar {
        font-size: 250%;
        font-weight: bold;
        font-family: Times New Roman;
        text-align: center;
    }
    </style>
    <div class="navbar">
        COELHO Library
    </div>
    """,
    unsafe_allow_html = True
)

# Introduction section
st.markdown("""
    ### Bem-vindo(a) à COELHO Library!
    Eu sou o Rafael, e criei esta página com o intuito de vender diversos livros que comprei nos últimos meses,
    mas que não terei tempo para ler por questões pessoais e profissionais.

    Decidi vender a maioria dos livros que estão sem nenhuma (ou quase nenhuma) marca de uso por 50%
    do valor original. São livros nas seguintes categorias: Desenvolvimento pessoal,
    Ciência, Ficção, Comunicação, Marketing Digital, História, Biografia, Negócios e
    Mercado Financeiro.

    Os livros disponíveis estão à venda APENAS para quem mora em Curitiba e Região Metropolitana. 
    Para adquirí-los, é necessário combinar detalhes através de contato pelo WhatsApp. 
    Clique no botão abaixo para saber mais e para comprar livros.
""")

st.link_button(
    "Quero saber mais / Quero comprar livros",
    "https://api.whatsapp.com/send/?phone=5541996234222&text=Ol%C3%A1+Rafael,+quero+saber+mais+informa%C3%A7%C3%B5es+sobre+os+livros+que+voc%C3%AA+est%C3%A1+vendendo.",
    use_container_width = True
)

st.markdown("""
    Aproveitando a oportunidade, também quero convidar você a conhecer minha carreira
    e meus projetos profissionais. Trabalho há mais de quatro anos nas áreas de Ciência de Dados,
    Inteligência Artificial, Visão Computacional e Cybersecurity, e nos últimos meses venho
    desenvolvendo um portfólio de projetos profissionais robustos, visando atingir o mercado
    internacional nos próximos anos.
""")

col1, col2 = st.columns(2)
with col1:
    st.link_button(
        "Portfólio Profissional - Rafael Coelho",
        "https://rafaelcoelho1409.github.io/",
        use_container_width = True
    )
with col2:
    st.link_button(
        "LinkedIn - Rafael Coelho",
        "https://linkedin.com/in/rafaelcoelho1409/",
        use_container_width = True
    )

st.divider()

# Filters section
st.header("FILTROS")
filter_columns = st.columns(5)
search = filter_columns[0].text_input("Buscar")
seller = filter_columns[1].multiselect(
    "Seller", 
    catalog["seller"].unique(), 
    default = catalog["seller"].unique())
genre = filter_columns[2].multiselect(
    "Categoria", 
    catalog["genre"].unique(), 
    default = catalog["genre"].unique())
min_price = filter_columns[3].number_input(
    "Preço Mínimo (R$)", 
    min_value = float(catalog['price_discount'].min()), 
    max_value = float(catalog['price_discount'].max()), 
    value = float(catalog['price_discount'].min()))
max_price = filter_columns[4].number_input(
    "Preço Máximo (R$)", 
    min_value = float(catalog['price_discount'].min()), 
    max_value = float(catalog['price_discount'].max()), 
    value = float(catalog['price_discount'].max()))

# Filter the catalog based on user input
filtered_catalog = catalog.copy()
if search:
    search = re.sub(r'[^A-Za-z0-9]', '', search)
    filtered_catalog = filtered_catalog[
        (filtered_catalog['name'].str.contains(search, case=False) |
         filtered_catalog['author'].str.contains(search, case=False) |
         filtered_catalog['genre'].str.contains(search, case=False))
    ]
filtered_catalog = filtered_catalog[filtered_catalog['seller'].isin(seller)]
filtered_catalog = filtered_catalog[filtered_catalog['genre'].isin(genre)]
filtered_catalog = filtered_catalog[filtered_catalog['price_discount'] >= min_price]
filtered_catalog = filtered_catalog[filtered_catalog['price_discount'] <= max_price]

# Display the filtered books
st.markdown("## LIVROS")
books_display = st.columns(2)
for index, row in filtered_catalog.iterrows():
    with books_display[index % 2].expander(f"**{row['name']} - {row['author']}**", expanded = True):
        col1, col2 = st.columns(2)
        with col1:
            image_carousel([f"assets/{row['filename']}1.png", f"assets/{row['filename']}2.png"], [])
        with col2:
            st.write(f"## {row['name']}")
            st.write(f"### *{row['author']}*")
            st.divider()
            st.write(f"**Gênero:** *{row['genre']}*")
            st.write(f"**Vendedor:** *{row['seller']}*")
            st.write(f"**Descrição do preço:** *{row['price_description']}*")
            st.divider()
        st.divider()
        col1_, col2_ = st.columns(2)
        with col1_:
            st.write("**Preço com desconto**")
            st.write(f"# :green[R${row['price_discount']:.2f}]")
        with col2_:
            st.write("**Preço original**")
            st.write(f"# :red[R${row['price']:.2f}]")