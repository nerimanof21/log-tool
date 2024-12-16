import os  # Qovluq yaratmaq üçün lazımdır
import re
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import Counter

# Çıxış üçün əsas qovluq yaradılır
OUTPUT_FOLDER = "output_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Qovluq yoxdursa yaradılır

# Çıxış fayllarının yolları təyin edilir
LOG_FILE = "server_logs.txt"
FAILED_LOGINS_FILE = os.path.join(OUTPUT_FOLDER, "unsuccessful_logins.json")
LOG_REPORT_CSV = os.path.join(OUTPUT_FOLDER, "logs_report.csv")
THREAT_IPS_FILE = os.path.join(OUTPUT_FOLDER, "detected_threat_ips.json")
MATCHED_THREATS_FILE = os.path.join(OUTPUT_FOLDER, "matched_threat_logs.json")

# 1. Log məlumatlarını oxumaq və ayırmaq
def extract_log_data(log_path):
    try:
        with open(log_path, 'r') as file:
            logs = []
            for entry in file:
                match = re.match(r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<timestamp>.*?)\] "(?P<method>\w+) .*? HTTP/.*?" (?P<status>\d+)', entry)
                if match:
                    logs.append(match.groupdict())
            print(f"{len(logs)} log qeydi oxundu.")
            return logs
    except FileNotFoundError:
        print(f"{log_path} faylı tapılmadı!")
        return []

# 2. Uğursuz giriş cəhdlərini tapmaq
def find_failed_attempts(log_entries):
    failed_ips = Counter()
    for entry in log_entries:
        if entry['status'].startswith('40'):  # "40x" kodları uğursuz girişləri göstərir
            failed_ips[entry['ip']] += 1
    return {ip: count for ip, count in failed_ips.items() if count >= 5}

# 3. Log məlumatlarını CSV faylında saxlamaq
def save_logs_to_csv(log_entries, csv_path):
    try:
        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["ip", "timestamp", "method", "status"])
            writer.writeheader()
            for log in log_entries:
                writer.writerow(log)
        print(f"Log məlumatları {csv_path} faylına yazıldı.")
    except Exception as e:
        print(f"CSV faylında problem yaranıb: {e}")

# 4. Təhlükəli IP-lərin siyahısını əldə etmək
def fetch_threat_ips(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        rows = driver.find_elements(By.XPATH, "//table//tr")
        threats = {}
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 2:
                threats[cols[0].text.strip()] = cols[1].text.strip()
        driver.quit()
        return threats
    except Exception as e:
        print(f"Təhlükəli IP-ləri yükləyərkən səhv baş verdi: {e}")
        return {}

# 5. Təhlükəli IP-lərlə log məlumatlarını uyğunlaşdırmaq
def correlate_threat_ips(log_entries, threat_data):
    correlated = []
    for log in log_entries:
        if log['ip'] in threat_data:
            log['threat_description'] = threat_data[log['ip']]
            correlated.append(log)
    return correlated

# 6. Bütün məlumatları JSON faylında saxlamaq
def save_to_json(data, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Məlumatlar {file_path} faylına yazıldı.")
    except Exception as e:
        print(f"JSON faylında problem: {e}")

# Əsas Funksiya
def main():
    print("Analiz başlanır...")
    # 1. Log məlumatlarını oxu
    logs = extract_log_data(LOG_FILE)
    if not logs:
        print("Log faylı boşdur və ya oxunmadı!")
        return

    # 2. Uğursuz giriş cəhdlərini tap
    failed_attempts = find_failed_attempts(logs)
    save_to_json(failed_attempts, FAILED_LOGINS_FILE)

    # 3. Logları CSV formatına yaz
    save_logs_to_csv(logs, LOG_REPORT_CSV)

    # 4. Təhlükəli IP-ləri yüklə
    threat_url = "http://127.0.0.1:8000/"
    threat_ips = fetch_threat_ips(threat_url)
    save_to_json(threat_ips, THREAT_IPS_FILE)

    # 5. Təhlükəli IP-lərlə log məlumatlarını uyğunlaşdır
    matched_threats = correlate_threat_ips(logs, threat_ips)
    if matched_threats:
        save_to_json(matched_threats, MATCHED_THREATS_FILE)
    else:
        print("Təhlükəli IP-lərlə uyğun log qeydi tapılmadı.")
    print("Analiz tamamlandı!")

if __name__ == "__main__":
    main()
