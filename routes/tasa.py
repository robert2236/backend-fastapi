from fastapi import APIRouter, HTTPException
import pyBCV


tasa = APIRouter()

@tasa.get("/api/tasa-de-cambio-usd")
def obtener_tasa_de_cambio_usd():
    currency = pyBCV.Currency()
    usd_rate = currency.get_rate(currency_code='USD', prettify=False)
    return float(usd_rate)

@tasa.get("/api/ultima-actualizacion")
def obtener_ultima_actualizacion():
    currency = pyBCV.Currency()
    last_update = currency.get_rate(currency_code='Fecha')
    return last_update

