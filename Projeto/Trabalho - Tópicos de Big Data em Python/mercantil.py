from playwright.sync_api import sync_playwright
import pandas as pd

urls_especificas = {
    'arroz': 'https://www.mercantilatacado.com.br/arroz/arroz?_q=arroz&fuzzy=0&initialMap=ft&initialQuery=arroz&map=category-3,ft&operator=and',
    'feijao': 'https://www.mercantilatacado.com.br/feijao/feij%C3%A3o?_q=feij%C3%A3o&fuzzy=0&initialMap=ft&initialQuery=feij%C3%A3o&map=category-3,ft&operator=and',
    'farinha': 'https://www.mercantilatacado.com.br/farinha%20de%20mandioca?_q=farinha%20de%20mandioca&map=ft',
    'acucar': 'https://www.mercantilatacado.com.br/acucar/a%C3%A7ucar?_q=a%C3%A7ucar&fuzzy=0&initialMap=ft&initialQuery=a%C3%A7ucar&map=category-2,ft&operator=and',
    'sal': 'https://www.mercantilatacado.com.br/sal/sal?_q=sal&fuzzy=0&initialMap=ft&initialQuery=sal&map=category-3,ft&operator=and',
    'oleo': 'https://www.mercantilatacado.com.br/azeite/oleo/outros/%C3%B3leo?_q=%C3%B3leo&fuzzy=0&initialMap=ft&initialQuery=%C3%B3leo&map=category-3,category-3,category-3,ft&operator=and',
    'leite': 'https://www.mercantilatacado.com.br/leite-liquido/leite%20liquido?_q=leite%20liquido&fuzzy=0&initialMap=ft&initialQuery=leite%20liquido&map=category-2,ft&operator=and',
    'pao': 'https://www.mercantilatacado.com.br/pao/p%C3%A3o?_q=p%C3%A3o&fuzzy=0&initialMap=ft&initialQuery=p%C3%A3o&map=category-2,ft&operator=and',
    'banana': 'https://www.mercantilatacado.com.br/hortifruti/banana?_q=banana&fuzzy=0&initialMap=ft&initialQuery=banana&map=category-1,ft&operator=and',
    'tomate': 'https://www.mercantilatacado.com.br/hortifruti/tomate?_q=tomate&fuzzy=0&initialMap=ft&initialQuery=tomate&map=category-1,ft&operator=and',
    'batata': 'https://www.mercantilatacado.com.br/hortifruti/batata?_q=batata&fuzzy=0&initialMap=ft&initialQuery=batata&map=category-1,ft&operator=and'
}

def coletar_preco(produto):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        url = urls_especificas.get(produto, f'https://www.mercantilatacado.com.br/{produto.replace(" ", "%20")}')
        print(f"🔍 Acessando: {url}")
        page.goto(url, timeout=50000)

        page.wait_for_timeout(4000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)

        try:
            page.wait_for_selector('.vtex-product-summary-2-x-container', timeout=10000)
        except:
            print(f"⚠️ Nenhum produto visível para {produto}")
            browser.close()
            return pd.DataFrame([])

        produtos = page.locator('.vtex-product-summary-2-x-container').all()

        dados = []

        for prod in produtos:
            try:
                if prod.locator('.mercantilatacado-mercantil-components-1-x-ProductName').count() == 0:
                    continue
                nome = prod.locator('.mercantilatacado-mercantil-components-1-x-ProductName').inner_text().strip()

                if prod.locator('.vtex-store-components-3-x-sellingPrice .mercantilatacado-mercantil-components-1-x-currencyInteger').count() == 0:
                    continue
                inteiro = prod.locator('.vtex-store-components-3-x-sellingPrice .mercantilatacado-mercantil-components-1-x-currencyInteger').first.inner_text()

                fracao = prod.locator('.vtex-store-components-3-x-sellingPrice .mercantilatacado-mercantil-components-1-x-currencyFraction').first.inner_text()

                preco_str = f"{inteiro},{fracao}"
                preco = float(preco_str.replace(',', '.'))

                if preco == 0:
                    continue

                dados.append({
                    'mercado': 'Mercantil',
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

        df = df[df['nome'].str.lower().str.contains(produto.lower())]

        print(f"✅ Coleta finalizada para {produto}. Produtos encontrados: {len(df)}")

        return df

