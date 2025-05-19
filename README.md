## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [httpx](https://www.python-httpx.org/)
- [CoinGecko API](https://www.coingecko.com/)

# 🌐 Conversor de Moedas e Criptomoedas - API com FastAPI

## 📘 Descrição

API Web desenvolvida com **FastAPI** que permite conversão entre:

- **5 criptomoedas**: BTC, ETH, BNB, SOL, XRP
- **3 moedas fiduciárias**: USD, EUR, BRL

Este projeto foi desenvolvido como parte da disciplina Projeto em Desenvolvimento de Sistemas. Permite que qualquer pessoa ou sistema externo consulte valores convertidos de moedas e criptomoedas de forma simples, prática e em tempo real.

---

## 🎯 Funcionalidades

- 🔁 Conversão entre qualquer moeda e cripto suportada
- ⏱️ Cotações em tempo real via CoinGecko
- 📦 API RESTful, pronta para integração com outros sistemas
- 🌍 Endpoint `/converter`

---

## 🧪 Exemplo de uso

```http
GET /converter?de=btc&para=brl&valor=0.05

