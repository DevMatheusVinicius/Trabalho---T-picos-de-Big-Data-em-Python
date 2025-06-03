from playwright.sync_api import sync_playwright
import pandas as pd

urls_especificas = {
    'arroz': 'https://www.gbarbosa.com.br/arroz/arroz?_q=arroz&fuzzy=0&initialMap=ft&initialQuery=arroz&map=category-3,ft&operator=and',
    'farinha': 'https://www.gbarbosa.com.br/farinha%20de%20mandioca?_q=farinha%20de%20mandioca&map=ft',
    'acucar': 'https://www.gbarbosa.com.br/acucar/a%C3%A7%C3%BAcar?_q=a%C3%A7%C3%BAcar&fuzzy=0&initialMap=ft&initialQuery=a%C3%A7%C3%BAcar&map=category-2,ft&operator=and',
    'sal': 'https://www.gbarbosa.com.br/sal/sal?_q=sal&fuzzy=0&initialMap=ft&initialQuery=sal&map=category-3,ft&operator=and',
    'oleo': 'https://www.gbarbosa.com.br/oleo/%C3%B3leo?_q=%C3%B3leo&fuzzy=0&initialMap=ft&initialQuery=%C3%B3leo&map=category-3,ft&operator=and',
    'leite': 'https://www.gbarbosa.com.br/leite-liquido/leite?_q=leite&fuzzy=0&initialMap=ft&initialQuery=leite&map=category-2,ft&operator=and',
    'pao': 'https://www.gbarbosa.com.br/pao/p%C3%A3o?_q=p%C3%A3o&fuzzy=0&initialMap=ft&initialQuery=p%C3%A3o&map=category-2,ft&operator=and',
    'cafe': 'https://www.gbarbosa.com.br/cafe-soluvel/cafe-torrado-moido/caf%C3%A9?_q=caf%C3%A9&fuzzy=0&initialMap=ft&initialQuery=caf%C3%A9&map=category-3,category-3,ft&operator=and',
    'banana': 'https://www.gbarbosa.com.br/hortifruti/banana?_q=banana&fuzzy=0&initialMap=ft&initialQuery=banana&map=category-1,ft&operator=and',
    'tomate': 'https://www.gbarbosa.com.br/hortifruti/tomate?_q=tomate&fuzzy=0&initialMap=ft&initialQuery=tomate&map=category-1,ft&operator=and',
    'batata': 'https://www.gbarbosa.com.br/hortifruti/batata?_q=batata&fuzzy=0&initialMap=ft&initialQuery=batata&map=category-1,ft&operator=and'
}

def coletar_preco(produto):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        url = urls_especificas.get(produto, f'https://www.gbarbosa.com.br/{produto.replace(" ", "%20")}')
        print(f"🔍 Acessando: {url}")
        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        while True:
            try:
                if page.locator('button:has-text("CARREGAR MAIS")').is_visible():
                    print("🔽 Clicando em 'CARREGAR MAIS'...")
                    page.locator('button:has-text("CARREGAR MAIS")').click()
                    page.wait_for_timeout(2000)
                else:
                    break
            except:
                break

        items = page.locator('.gbarbosa-cmedia-integration-cencosud-1-x-galleryItem').all()

        dados = []

        for item in items:
            try:
                nome = item.locator('.gbarbosa-gbarbosa-components-0-x-ProductName').inner_text().strip()

                selling_price_container = item.locator('.vtex-store-components-3-x-sellingPrice')

                inteiro = selling_price_container.locator('.gbarbosa-gbarbosa-components-0-x-currencyInteger').first.inner_text()
                fracao = selling_price_container.locator('.gbarbosa-gbarbosa-components-0-x-currencyFraction').first.inner_text()

                preco_str = f"{inteiro},{fracao}"
                preco = float(preco_str.replace(',', '.'))

                if preco == 0:
                    continue

                dados.append({
                    'mercado': 'Gbarbosa',
                    'produto': produto,
                    'nome': nome,
                    'preco': preco,
                    'link': url
                })

            except Exception as e:
                print(f"❗️Erro ao processar produto: {e}")
                continue

        browser.close()

        df = pd.DataFrame(dados)

        if not df.empty and 'nome' in df.columns:
            df = df[df['nome'].str.lower().str.contains(produto.lower())]

        print(f"✅ Coleta finalizada para {produto}. Produtos encontrados: {len(df)}")

        return df






