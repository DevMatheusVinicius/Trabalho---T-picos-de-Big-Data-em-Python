import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Comparação de Preços", layout="wide")

st.title('📊 Dashboard Comparação de Preços BIG DATA')
st.markdown("### Encontre o melhor preço para cada item da cesta básica")

with st.sidebar:
    st.header("🔍 Filtros")

    if st.button('🔄 Atualizar Preços'):
        import os
        os.system('python test.py')

try:
    df = pd.read_csv('precos_mercados.csv')
    df = df[df['preco'] > 0]

    produto_filter = st.sidebar.selectbox('Selecione o Produto', df['produto'].unique())
    mercado_filter = st.sidebar.multiselect('Selecione os Mercados', df['mercado'].unique(), default=df['mercado'].unique())

    df_filtered = df[(df['produto'] == produto_filter) & (df['mercado'].isin(mercado_filter))]

    if not df_filtered.empty:
        st.subheader(f"📦 Preços de **{produto_filter}**")
        st.dataframe(df_filtered.style.format({'preco': 'R$ {:.2f}'}))

        mais_barato = df_filtered.loc[df_filtered['preco'].idxmin()]
        st.success(f"✅ Mais barato: **{mais_barato['mercado']}** → R$ {mais_barato['preco']}")
        st.markdown(f"[🛒 Comprar aqui]({mais_barato['link']})")

        st.subheader("📊 Gráfico de comparação de preços")
        fig = px.bar(df_filtered, x='mercado', y='preco', color='mercado', text='preco', title='Comparativo de Preços')
        st.plotly_chart(fig, use_container_width=True)

        st.download_button('⬇️ Baixar CSV', df_filtered.to_csv(index=False), 'precos_filtrados.csv', 'text/csv')

    else:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")

except Exception as e:
    st.error(f'Erro ao carregar dados: {e}')