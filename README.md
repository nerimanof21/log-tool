# log-tool
# Log Təhlili Aləti

Bu layihə server log fayllarını işləyən, şübhəli fəaliyyətləri aşkar edən və tanınmış təhlükəli IP-lərlə uyğunluq taparaq potensial təhlükəsizlik risklərini müəyyən edən Python əsaslı log təhlili aləti təqdim edir. Alət `os`, `re`, `json`, `csv` və `selenium` kimi müxtəlif kitabxanalardan istifadə etməklə həyata keçirilmişdir.

## Xüsusiyyətlər

1. **Log Təhlili:**
   - Server log fayllarından IP ünvanlarını, zaman möhürlərini, HTTP metodlarını və status kodlarını çıxarır.

2. **Uğursuz Giriş Cəhdlərinin Aşkarlanması:**
   - Təkrarlanan uğursuz giriş cəhdləri olan (HTTP status kodları `40` ilə başlayan) IP ünvanlarını müəyyən edir.

3. **Təhlükəli IP Uyğunluğu:**
   - Log qeydlərini xarici mənbədən əldə edilən tanınmış təhlükəli IP-lərin siyahısı ilə müqayisə edir.

4. **Məlumatların Çıxarılması:**
   - Nəticələri müxtəlif fayl formatlarında saxlayır:
     - **JSON**: Uğursuz giriş cəhdləri və uyğun təhlükələr üçün.
     - **CSV**: Tam log məlumatları üçün.

5. **Veb Scraping:**
   - Selenium istifadə edərək təhlükəli IP məlumatlarını dinamik şəkildə bir veb səhifədən yükləyir.

## Quraşdırma

1. Repozitoriyanı klonlayın:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Virtual mühit yaradın:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows üçün: .venv\Scripts\activate
   ```

3. Lazımi asılılıqları quraşdırın:
   ```bash
   pip install -r requirements.txt
   ```

## İstifadə

1. Lazımi faylların və konfiqurasiyaların mövcud olduğundan əmin olun:
   - Log faylını `server_logs.txt` adı ilə layihə qovluğuna yerləşdirin.
   - Selenium WebDriver-in (məsələn, ChromeDriver) düzgün quraşdırıldığından və PATH-də mövcud olduğundan əmin olun.

2. Aləti işə salın:
   ```bash
   python main.py
   ```

3. Çıxışlar:
   - **JSON Faylları:**
     - `unsuccessful_logins.json`: Uğursuz giriş cəhdlərini ehtiva edir.
     - `detected_threat_ips.json`: Yüklənmiş təhlükəli IP məlumatlarını ehtiva edir.
     - `matched_threat_logs.json`: Tanınmış təhlükəli IP-lərlə uyğun gələn log qeydlərini ehtiva edir.
   - **CSV Faylı:**
     - `logs_report.csv`: Təhlil edilən bütün log məlumatlarının ətraflı hesabatını ehtiva edir.

## Fayl Strukturu

```
project_directory/
|— main.py                 # Əsas skript
|— server_logs.txt         # Giriş log faylı
|— output_files/          # Yaradılmış çıxış faylları üçün qovluq
|   |— unsuccessful_logins.json
|   |— detected_threat_ips.json
|   |— matched_threat_logs.json
|   |— logs_report.csv
|— requirements.txt       # Python asılılıqları
```

## Konfiqurasiya

### Log Faylı
Log faylı hər sətirdə aşağıdakıları əhatə edən formatda olmalıdır:
- Bir IP ünvanı.
- Kvadrat mötərizələrdə zaman möhürü.
- HTTP metodu və status kodu.

Nümunə:
```
192.168.1.1 - - [12/Dec/2024:12:34:56 +0000] "GET /index.html HTTP/1.1" 200 1234
192.168.1.2 - - [12/Dec/2024:12:35:00 +0000] "POST /login HTTP/1.1" 401 567
```

### Təhlükəli IP Mənbəyi
Alət təhlükəli IP məlumatlarını konfiqurasiya edilə bilən bir URL-dən yükləyir. `main.py` faylındakı `threat_url` dəyişənini istədiyiniz mənbəyə yeniləyin:
```python
threat_url = "http://127.0.0.1:8000/"
```

## Asılılıqlar

- Python 3.8+
- Lazımi Python kitabxanaları (`requirements.txt` faylında):
  - `selenium`
  - `os`
  - `re`
  - `json`
  - `csv`
- ChromeDriver (və ya Selenium ilə uyğun digər WebDriver)

## Problemlərin Həlli

1. **FileNotFoundError:**
   - Giriş log faylı (`server_logs.txt`) layihə qovluğunda mövcud olduğundan əmin olun.

2. **Selenium WebDriver Səhvləri:**
   - ChromeDriver-in quraşdırıldığını və versiyasının Chrome brauzerinizlə uyğun gəldiyini yoxlayın.

3. **Boş Çıxışlar:**
   - Log faylının boş olmadığını və gözlənilən formata uyğun olduğunu yoxlayın.
   - Təhlükəli IP mənbəyinin əlçatan olduğundan əmin olun.

## Töhfələr

Töhfələrə açığıq! Repozitoriyanı fork edin və pull request təqdim edin.


