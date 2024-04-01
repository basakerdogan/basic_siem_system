import time
from elasticsearch import Elasticsearch
import auth as auth

# Elasticsearch bağlantısını oluştur
es = Elasticsearch(
    [auth.ELASTICSEARCH_URL],
    http_auth=(auth.USERNAME, auth.PASSWORD),
    scheme="https",
    port=443,
)


def log_network_activity(source_ip, destination_ip, event_type, description):
    # Ağ etkinliğini Elasticsearch'e kaydet
    doc = {
        '@timestamp': int(time.time() * 1000),  # Geçerli zamanı milisaniye cinsinden al
        'source_ip': source_ip,
        'destination_ip': destination_ip,
        'event_type': event_type,
        'description': description
    }
    try:
        # Hata alabileceğiniz kod buraya gelir
        es.index(index="network_activity", body=doc)
    except Exception as e:
        # Hata olduğunda burası çalışır
        print("Elasticsearch'e doküman ekleme hatası:", e)

def main():
    # Örnek ağ etkinlikleri
    network_events = [
        {"source_ip": "192.168.1.100", "destination_ip": "8.8.8.8", "event_type": "DNS Query",
         "description": "Looking up domain"},
        {"source_ip": "192.168.1.101", "destination_ip": "10.0.0.1", "event_type": "HTTP Request",
         "description": "GET request to server"},
        {"source_ip": "192.168.1.102", "destination_ip": "8.8.8.8", "event_type": "DNS Query",
         "description": "Looking up domain"},
    ]

    # Ağ etkinliklerini kaydet
    for event in network_events:
        log_network_activity(**event)
        time.sleep(1)  # 1 saniye bekleyerek işlemi yavaşlat


if __name__ == "__main__":
    main()
