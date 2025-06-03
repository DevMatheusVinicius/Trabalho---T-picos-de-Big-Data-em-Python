from playwright.sync_api import sync_playwright
import pandas as pd

urls_especificas = {
    'farinha': 'https://www.paodeacucar.com/busca?terms=farinha%20de%20mandioca',
    'acucar': 'https://www.paodeacucar.com/busca?terms=a%C3%A7%C3%BAcar%20%20pacote%201kg',
    'banana': 'https://www.paodeacucar.com/categoria/alimentos/hortifruti/frutas/banana?s=relevance&p=1'
}

def coletar_preco(produto):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        url = urls_especificas.get(produto, f'https://www.paodeacucar.com/busca?terms={produto.replace(" ", "%20")}')
        print(f"🔍 Acessando: {url}")
        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        produtos = page.locator('.Link-sc-j02w35-0.bEJTOI.Title-sc-20azeh-10.gdVmss').all_text_contents()
        precos_raw = page.locator('.PriceValue-sc-20azeh-4').all()

        dados = []

        for nome, preco_element in zip(produtos, precos_raw):
            try:
                preco_text = preco_element.inner_text().replace('R$', '').strip()
                preco = float(preco_text.replace(',', '.'))
                if preco == 0:
                    continue

                dados.append({
                    'mercado': 'Paodeacucar',
                    'produto': produto,
                    'nome': nome,
                    'preco': preco,
                    'link': url
                })
            except Exception as e:
                print(f"❗️Erro ao processar produto: {nome} - {e}")
                continue

        browser.close()
        print(f"✅ Coleta finalizada para {produto}. Produtos encontrados: {len(dados)}")

        return pd.DataFrame(dados)

