import csv
import requests
import schedule
import time

def login(userid, pin):
    base_url = "https://akademik.unbin.ac.id/absensi/"
    login_url = base_url + "login.php?action=login"
    
    session = requests.Session()
    
    # Akses halaman index untuk mendapatkan cookies
    response_index = session.get(base_url + "index.php")
    print(f"[{userid}] Akses index.php: Status Code {response_index.status_code}")
    
    # Siapkan header agar menyerupai browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Referer": base_url + "index.php",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    # Akses halaman login (opsional, untuk memastikan cookies terupdate)
    login_page = session.get(login_url, headers=headers)
    print(f"[{userid}] Akses login page: Status Code {login_page.status_code}")

    # Siapkan data login termasuk parameter submit (mengemulasi klik tombol login)
    data = {
        "userid": userid,
        "pin": pin,
        "login": "Login"
    }
    
    # Kirim POST request untuk login
    response = session.post(login_url, data=data, headers=headers)
    
    print(f"[{userid}] Status Code: {response.status_code}")
    print(f"[{userid}] Response (awal): {response.text[:500]}")
    
    # Cek cookies yang diterima (opsional)
    print(f"[{userid}] Cookies: {session.cookies.get_dict()}")
    
    # Validasi login (sesuaikan indikator sesuai dengan respons sebenarnya)
    if "Dashboard" in response.text or "Selamat datang" in response.text:
        print(f"[{userid}] Login Berhasil!")
    else:
        print(f"[{userid}] Login Gagal!")
    
    # Simpan response untuk analisa lebih lanjut (opsional)
    with open(f"{userid}_response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    return session

def login_from_csv(csv_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            userid = row['userid']
            pin = row['pin']
            print(f"\nMencoba login untuk akun: {userid}")
            login(userid, pin)

def scheduled_absence():
    csv_file = "akun.csv"  # Pastikan file CSV berada pada path yang benar
    print("Menjalankan absensi otomatis...")
    login_from_csv(csv_file)

if __name__ == "__main__":
    # Menjadwalkan absensi pada hari Senin s.d. Jumat pukul 09:30 dan 13:30
    schedule.every().monday.at("09:30").do(scheduled_absence)
    schedule.every().monday.at("13:30").do(scheduled_absence)
    schedule.every().tuesday.at("09:30").do(scheduled_absence)
    schedule.every().tuesday.at("13:30").do(scheduled_absence)
    schedule.every().wednesday.at("09:30").do(scheduled_absence)
    schedule.every().wednesday.at("13:30").do(scheduled_absence)
    schedule.every().thursday.at("09:30").do(scheduled_absence)
    schedule.every().thursday.at("13:30").do(scheduled_absence)
    schedule.every().friday.at("14:40").do(scheduled_absence)
    schedule.every().friday.at("14:45").do(scheduled_absence)
    
    print("Scheduler berjalan. Menunggu jadwal absensi ...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # cek setiap 60 detik
