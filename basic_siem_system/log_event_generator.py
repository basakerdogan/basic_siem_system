import os
import requests
import json
import time
import auth
from elasticsearch import Elasticsearch

# Elasticsearch bağlantısını oluştur
es = Elasticsearch(
    [auth.ELASTICSEARCH_URL],
    http_auth=(auth.USERNAME, auth.PASSWORD),
    scheme="https",
    port=443,
)

def send_event(event):
    headers = {'Content-Type': 'application/json'}
    INDEX_NAME = "network_activity"
    url = f"{auth.ELASTICSEARCH_URL}/{INDEX_NAME}/_doc"
    try:
        es.index(index="network_activity", body=generate_log_event())
        print("başarılı bir şekilde olay oluştu.")
    except Exception as e:
        print("İstek gönderilirken bir hata oluştu:", e)


def generate_log_event():
    # Rastgele bir IP adresi oluştur
    import random
    source_ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    destination_ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

    # Rastgele bir event tipi seç
    event_types = ["Login Attempt", "File Download", "SQL Injection", "Malware Detected"]
    event_type = random.choice(event_types)

    # Rastgele bir açıklama oluştur
    descriptions = [
        "Failed login attempt for user admin",
        "Downloaded file 'report.pdf' from server",
        "Detected SQL injection attempt in query string",
        "Malware 'TrojanXYZ' detected and quarantined"
    ]
    description = random.choice(descriptions)

    # Olay oluştur
    event = {
        "timestamp": int(time.time()),
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "event_type": event_type,
        "description": description
    }
    return event


def main():
    while True:
        event = generate_log_event()
        send_event(event)
        time.sleep(5)  # 5 saniyede bir olay gönder


if __name__ == "__main__":
    main()
