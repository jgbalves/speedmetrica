import streamlit as st

st.sidebar.title('Menu')
selected_page = st.sidebar.selectbox('Selecionar Pagina',['Página 1', 'Página 2'])

if selected_page == 'Página 1':
    st.title('Thiago Sapekinha')
    st.selectbox('Selecione uma opção',['Opção 1', 'Opção 2'])

elif selected_page == 'Página 2':
    st.title('Pagina 2 exemplo')
    st.selectbox('Selecione uma opção',['Opção 1', 'Opção 2'])
    x = st.slider('x')  # 👈 this is a widget
    st.write(x, 'squared is', x * x)
