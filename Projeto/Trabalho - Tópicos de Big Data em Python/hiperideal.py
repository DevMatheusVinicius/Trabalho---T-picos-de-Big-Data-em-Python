from playwright.sync_api import sync_playwright
import pandas as pd

urls_especificas = {
    'arroz': 'https://www.hiperideal.com.br/arroz?_q=arroz&fuzzy=0&initialMap=ft&initialQuery=arroz&map=category-3,ft&operator=and&query=/arroz/arroz&searchState',
    'feijao': 'https://www.hiperideal.com.br/feij%C3%A3o?_q=feij%C3%A3o&fuzzy=0&initialMap=ft&initialQuery=feij%C3%A3o&map=category-3,ft&operator=and&query=/feijao/feij%C3%A3o&searchState',
    'macarrao': 'https://www.hiperideal.com.br/macarrao?_q=macarrao&fuzzy=0&initialMap=ft&initialQuery=macarrao&map=category-2,ft&operator=and&query=/massas---molhos/macarrao&searchState',
    'farinha': 'https://www.hiperideal.com.br/farinha%20de%20mandioca?_q=farinha%20de%20mandioca&map=ft',
    'acucar': 'https://www.hiperideal.com.br/a%C3%A7%C3%BAcar?_q=a%C3%A7%C3%BAcar&fuzzy=0&initialMap=ft&initialQuery=a%C3%A7%C3%BAcar&map=category-3,ft&operator=and&query=/acucar---adocante/a%C3%A7%C3%BAcar&searchState',
    'sal': 'https://www.hiperideal.com.br/sal?_q=sal&fuzzy=0&initialMap=ft&initialQuery=sal&map=category-3,ft&operator=and&query=/sal/sal&searchState',
    'oleo': 'https://www.hiperideal.com.br/%C3%B3leo?_q=%C3%B3leo&fuzzy=0&initialMap=ft&initialQuery=%C3%B3leo&map=category-3,ft&operator=and&query=/oleo/%C3%B3leo&searchState',
    'leite': 'https://www.hiperideal.com.br/leite?_q=leite&fuzzy=0&initialMap=ft&initialQuery=leite&map=category-3,ft&operator=and&query=/leite/leite&searchState',
    'pao': 'https://www.hiperideal.com.br/p%C3%A3o?_q=p%C3%A3o&fuzzy=0&initialMap=ft&initialQuery=p%C3%A3o&map=category-1,ft&operator=and&query=/padaria/p%C3%A3o&searchState',
    'banana': 'https://www.hiperideal.com.br/banana?_q=banana&fuzzy=0&initialMap=ft&initialQuery=banana&map=category-1,ft&operator=and&query=/hortifruti/banana&searchState',
    'tomate': 'https://www.hiperideal.com.br/tomate?_q=tomate&fuzzy=0&initialMap=ft&initialQuery=tomate&map=category-1,ft&operator=and&query=/hortifruti/tomate&searchState',
    'batata': 'https://www.hiperideal.com.br/batata?_q=batata&fuzzy=0&initialMap=ft&initialQuery=batata&map=category-1,ft&operator=and&query=/hortifruti/batata&searchState'
}

def coletar_preco(produto):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        url = urls_especificas.get(produto, f'https://www.hiperideal.com.br/{produto.replace(" ", "%20")}')
        print(f"🔍 Acessando: {url}")
        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        produtos = page.locator('.vtex-product-summary-2-x-productBrand').all_text_contents()
        precos_raw = page.locator('.vtex-product-price-1-x-currencyContainer--price-main').all()

        dados = []

        for nome, preco_element in zip(produtos, precos_raw):
            try:
                inteiro = preco_element.locator('.vtex-product-price-1-x-currencyInteger').inner_text()
                fracao = preco_element.locator('.vtex-product-price-1-x-currencyFraction').inner_text()
                preco_str = f"{inteiro},{fracao}"
                preco = float(preco_str.replace(',', '.'))

                if preco == 0:
                    continue

                dados.append({
                    'mercado': 'Hiperideal',
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