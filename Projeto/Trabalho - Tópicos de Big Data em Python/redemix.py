from playwright.sync_api import sync_playwright
import pandas as pd

urls_especificas = {
    'sal': 'https://www.redemix.com.br/mercearia/temperos-e-condimentos/sal/sal?O=OrderByTopSaleDESC&PS=18#2',
    'arroz': 'https://www.redemix.com.br/mercearia/graos-e-farinaceos/arroz/arroz?O=OrderByTopSaleDESC&PS=18#3',
    'feijao': 'https://www.redemix.com.br/mercearia/graos-e-farinaceos/feijao/feij%C3%A3o?O=OrderByTopSaleDESC&PS=18#2',
    'farinha': 'https://www.redemix.com.br/farinha%20de%20mandioca#1',
    'acucar': 'https://www.redemix.com.br/mercearia/acucar-e-adocante/a%C3%A7ucar?O=OrderByTopSaleDESC&PS=18#1',
    'oleo': 'https://www.redemix.com.br/mercearia/azeite-oleo-e-vinagre/oleos/especiais/%C3%B3leo?O=OrderByTopSaleDESC&PS=18#1',
    'leite': 'https://www.redemix.com.br/mercearia/leites/liquido/leite?O=OrderByTopSaleDESC&PS=18#1',
    'manteiga': 'https://www.redemix.com.br/frios-e-laticinios/manteiga-e-margarina/manteiga/manteiga?O=OrderByTopSaleDESC&PS=18#1',
    'banana': 'https://www.redemix.com.br/hortifruti/frutas/banana?O=OrderByTopSaleDESC&PS=18#1',
    'tomate': 'https://www.redemix.com.br/hortifruti/frutas/tomate?O=OrderByTopSaleDESC&PS=18#1',
    'batata': 'https://www.redemix.com.br/hortifruti/legumes/batata?O=OrderByTopSaleDESC&PS=18#1'
}

def coletar_preco(produto):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        url = urls_especificas.get(produto, f'https://www.redemix.com.br/{produto}#1')
        print(f"🔍 Acessando: {url}")
        page.goto(url, timeout=60000)
        
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)

        try:
            page.wait_for_selector('.product__content', timeout=10000)
        except:
            print(f"⚠️ Nenhum produto visível para {produto}")
            browser.close()
            return pd.DataFrame([])

        produtos = page.locator('.product__content').all()

        dados = []

        for prod in produtos:
            try:
                if prod.locator('.product__buy button').count() == 0:
                    continue
                nome = prod.locator('.product__buy button').get_attribute('data-name').strip()

                if prod.locator('.price__list.price-loaded').count() == 0:
                    continue
                preco_text = prod.locator('.price__list.price-loaded').inner_text().replace('R$', '').strip()
                preco = float(preco_text.replace(',', '.'))

                if preco == 0:
                    continue

                dados.append({
                    'mercado': 'Redemix',
                    'produto': produto,
                    'nome': nome,
                    'preco': preco,
                    'link': url
                })
            except Exception as e:
                print(f"❗️Erro ao processar produto: {e}")
                continue

        browser.close()
        print(f"✅ Coleta finalizada para {produto}. Produtos encontrados: {len(dados)}")

        return pd.DataFrame(dados)


