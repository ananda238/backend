from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/api/exchange", tags=["Exchange Rate"])
API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6"

@router.get("/")
async def get_exchange_rate(from_currency: str = "USD", to_currency: str = "IDR"):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="ExchangeRate-API key tidak ditemukan")
    url = f"{BASE_URL}/{API_KEY}/latest/{from_currency}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Gagal mengambil data kurs")
        data = response.json()
        if data["result"] != "success":
            raise HTTPException(status_code=500, detail="API error: " + data.get("error-type", ""))
        rate = data["conversion_rates"].get(to_currency)
        if not rate:
            raise HTTPException(status_code=404, detail="Mata uang tidak ditemukan")
        return {"from": from_currency, "to": to_currency, "rate": rate}