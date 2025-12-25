def process_sensor_data(raw_data):
    """
    Membersihkan data sensor produksi dan menghitung rata-rata valid.
    
    Args:
        raw_data (list): List of lists berisi data mentah per workstation.
        
    Returns:
        dict: Dictionary berisi 'production_stats' dan 'error_logs'.
    """
    clean_stats = []
    audit_log = []
    
    # Loop Workstation dengan index (enumerate) untuk ID
    for ws_id, shift_data in enumerate(raw_data, 1):
        valid_sum = 0
        valid_count = 0
        
        for reading in shift_data:
            # TANTANGAN ANDA:
            # 1. Cek tipe data (harus int). Jika bukan, append pesan ke audit_log, lalu continue.
            if isinstance(reading,int) == False:
                 kalimat = f'WS{ws_id}: Data {reading} rejected'
                 audit_log.append(kalimat)
                 continue
            # 2. Cek value (harus >= 0). Jika negatif, append pesan ke audit_log, lalu continue.
            if reading >= 0:
                valid_sum += reading
            else:
                kalimat = f'WS{ws_id}: Negative value {reading} rejected'
                audit_log.append(kalimat)
                continue
            # 3. Jika lolos, tambahkan ke valid_sum dan valid_count.
            
            valid_count +=1
            
        # HITUNG RATA-RATA
        # Hati-hati: Bagaimana jika valid_count adalah 0? 
        # Jangan sampai crash "ZeroDivisionError"
        average = 0.0 
        if valid_count > 0:
            average += (valid_sum/valid_count)
        else:
            average = 0.0
        
        # Simpan hasil per workstation
        ws_info = {
            "id": ws_id,
            "valid_count": valid_count,
            "average": average
        }
        clean_stats.append(ws_info)
        
    return {
        "production_stats": clean_stats,
        "error_logs": audit_log
    }

# Data Dummy
log_produksi = [
    [100, "MAINTENANCE", 95, 102],
    ["ERROR", 50, -20, "STOP", 60],
    [80, 85, 90],
    ["OFF", "BROKEN"] # Kasus Ekstrem: Semua sampah
]

# Eksekusi
result = process_sensor_data(log_produksi)

# Tampilkan Hasil dengan Rapi (Pretty Print manual)
print("--- PRODUCTION REPORT ---")
for stat in result["production_stats"]:
    print(f"Machine {stat['id']}: Avg = {stat['average']} (Based on {stat['valid_count']} valid data)")

print("\n--- ERROR AUDIT LOG ---")
for error in result["error_logs"]:
    print(error)