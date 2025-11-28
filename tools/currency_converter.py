import requests
from langchain.tools import tool   # veya from langchain_core.tools import tool

@tool
def convert_usd_to_try(amount: float, ids: str, vs_currencies: str) -> str:
    """USD miktarını verilen hedef para birimine çeviren LangChain aracı."""
    try:
        # String geldiyse: "100 usd" → 100.0
        if isinstance(amount, str):
            amount = float("".join(
                filter(lambda c: c.isdigit() or c == ".", amount)
            ))

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={vs_currencies}"
        response = requests.get(url)

        if response.status_code != 200:
            return f"API isteği başarısız oldu. Durum kodu: {response.status_code}"

        data = response.json()

        # Örnek JSON: { "usd": { "try": 33.2 } }
        rate = data[ids][vs_currencies]
        result = amount * rate

        return f"{amount} {ids.upper()} = {result:.2f} {vs_currencies.upper()} (Kur: {rate:.2f})"

    except Exception as e:
        return f"Hata oluştu: {e}"
if __name__ == "__main__":

    test_amount = 100
print("100 USD -> TRY")

print(
    convert_usd_to_try.run(
        {"amount": test_amount, "ids": "usd", "vs_currencies": "try"}
    )
)
# veya:
print(
    convert_usd_to_try.invoke(
        {"amount": test_amount, "ids": "usd", "vs_currencies": "try"}
    )
)
