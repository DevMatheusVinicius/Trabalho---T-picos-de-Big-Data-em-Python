import mercantil
import hiperideal
import gbarbosa
import paodeacucar
import redemix
import pandas as pd

produtos = ['arroz', 'feijão', 'macarrão', 'farinha', 'açúcar', 'sal', 'óleo', 'leite', 'pão', 'café', 'manteiga', 'banana', 'tomate', 'batata']

df_list = []

for produto in produtos:
    print(f"\n✅ Coletando no Mercantil: {produto}")
    df_merc = mercantil.coletar_preco(produto)
    df_list.append(df_merc)

    print(f"\n✅ Coletando no Hiperideal: {produto}")
    df_hiper = hiperideal.coletar_preco(produto)
    df_list.append(df_hiper)

    print(f"\n✅ Coletando no GBarbosa: {produto}")
    df_gbarb = gbarbosa.coletar_preco(produto)
    df_list.append(df_gbarb)

    print(f"\n✅ Coletando no Pao de Acucar: {produto}")
    df_pao = paodeacucar.coletar_preco(produto)
    df_list.append(df_pao)

    print(f"\n✅ Coletando no Redemix: {produto}")
    df_redemix = redemix.coletar_preco(produto)
    df_list.append(df_redemix)

df_final = pd.concat(df_list, ignore_index=True)
df_final.to_csv('precos_mercados.csv', index=False)

print("\n✅ Coleta finalizada! Arquivo salvo: precos_mercados.csv")