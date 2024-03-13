import time
import pika
import yfinance as yf

xu100_stocks = [
    "AEFES.IS", "AGHOL.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS",
    "AKFYE.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS", "ALBRK.IS",
    "ALFAS.IS", "ARCLK.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS",
    "BERA.IS", "BIENY.IS", "BIMAS.IS", "BIOEN.IS", "BOBET.IS",
    "BRSAN.IS", "BRYAT.IS", "BUCIM.IS", "CANTE.IS", "CCOLA.IS",
    "CIMSA.IS", "CWENE.IS", "DOAS.IS", "DOHOL.IS", "ECILC.IS",
    "ECZYT.IS", "EGEEN.IS", "EKGYO.IS", "ENERY.IS", "ENJSA.IS",
    "ENKAI.IS", "EREGL.IS", "EUPWR.IS", "EUREN.IS", "FROTO.IS",
    "GARAN.IS", "GESAN.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS",
    "HEKTS.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISGYO.IS",
    "ISMEN.IS", "IZENR.IS", "IZMDC.IS", "KARSN.IS", "KAYSE.IS",
    "KCAER.IS", "KCHOL.IS", "KLSER.IS", "KMPUR.IS", "KONTR.IS",
    "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS",
    "MAVI.IS", "MGROS.IS", "MIATK.IS", "ODAS.IS", "OTKAR.IS",
    "OYAKC.IS", "PENTA.IS", "PETKM.IS", "PGSUS.IS", "QUAGR.IS",
    "SAHOL.IS", "SASA.IS", "SDTTR.IS", "SISE.IS", "SKBNK.IS",
    "SMRTG.IS", "SOKM.IS", "TATEN.IS", "TAVHL.IS", "TCELL.IS",
    "THYAO.IS", "TKFEN.IS", "TOASO.IS", "TSKB.IS", "TTKOM.IS",
    "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS",
    "VESTL.IS", "YEOTK.IS", "YYLGD.IS", "ZOREN.IS"
]

def get_realtime_stock_data(stock_symbols, interval_seconds=60):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='stock_data')

    while True:
        for symbol in stock_symbols:
            stock = yf.Ticker(symbol)
            price = stock.info['regularMarketPrice']
            body = f"{symbol}:{price}"
            channel.basic_publish(exchange='', routing_key='stock_data', body=body)
        print(f"Data fetched at {time.ctime()}. Next fetch in {interval_seconds} seconds.")
        time.sleep(interval_seconds)

    connection.close()

get_realtime_stock_data(xu100_stocks)

