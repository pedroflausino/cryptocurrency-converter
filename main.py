from fastapi import FastAPI, Query
import httpx

app = FastAPI(title="Crypto Converter API")

# Dicionário com os códigos das criptos e seus IDs no CoinGecko
CRYPTO_IDS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "bnb": "binancecoin",
    "sol": "solana",
    "xrp": "ripple"
}

# Lista de moedas fiduciárias aceitas
FIAT = ["usd", "eur", "brl"]

@app.get("/converter")
async def converter(
    de: str = Query(..., description="Moeda de origem"),
    para: str = Query(..., description="Moeda de destino"),
    valor: float = Query(..., description="Valor a ser convertido")
):
    # Transformar tudo para minúsculo
    de = de.lower()
    para = para.lower()

    # Validar se as moedas são suportadas
    if de not in FIAT and de not in CRYPTO_IDS:
        return {"erro": f"Moeda de origem '{de}' não é suportada"}
    if para not in FIAT and para not in CRYPTO_IDS:
        return {"erro": f"Moeda de destino '{para}' não é suportada"}

    # Identificar quais moedas cripto precisamos buscar da API
    moedas_para_consultar = set()
    if de in CRYPTO_IDS:
        moedas_para_consultar.add(CRYPTO_IDS[de])
    if para in CRYPTO_IDS:
        moedas_para_consultar.add(CRYPTO_IDS[para])

    # Se ambas forem fiat, ainda assim precisamos de uma cripto para saber a cotação
    if not moedas_para_consultar:
        moedas_para_consultar.add("bitcoin")

    # Montar a URL da API do CoinGecko
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(moedas_para_consultar)}&vs_currencies=usd,eur,brl"

    # Requisição HTTP assíncrona
    async with httpx.AsyncClient() as client:
        resposta = await client.get(url)
        dados = resposta.json()

    # Função que retorna quanto vale 1 unidade da moeda em USD
    def get_valor_em_usd(moeda: str):
        if moeda == "usd":
            return 1.0
        elif moeda in FIAT:
            # Se for moeda fiat, pegamos o valor da primeira cripto como base
            base = list(dados.values())[0]
            return base["usd"] / base[moeda]
        elif moeda in CRYPTO_IDS:
            return dados[CRYPTO_IDS[moeda]]["usd"]
        return None

    preco_origem_usd = get_valor_em_usd(de)
    preco_destino_usd = get_valor_em_usd(para)

    # Validação extra
    if preco_origem_usd is None or preco_destino_usd is None:
        return {"erro": "Erro ao calcular valores. Verifique os parâmetros."}

    # Converter
    valor_em_usd = valor * preco_origem_usd
    valor_convertido = valor_em_usd / preco_destino_usd

    # Função de formatação
    def formatar_valor(moeda: str, valor: float):
        if moeda in FIAT:
            return f"{valor:,.2f}"
        return f"{valor:.8f}"

    return {
        "de": de.upper(),
        "para": para.upper(),
        "valor_original": formatar_valor(de, valor),
        "valor_convertido": formatar_valor(para, valor_convertido),
        "fonte": "CoinGecko"
    }