import pandas as pd
import os


#Mengambil File CSVnya  
file_order = os.path.join('archive', 'olist_orders_dataset.csv')
file_harga_barang = os.path.join('archive', 'olist_order_items_dataset.csv')
file_customer = os.path.join('archive', 'olist_customers_dataset.csv')

#Baca File
try:
    df_order = pd.read_csv(file_order)
    df_harga = pd.read_csv(file_harga_barang)
    df_customer = pd.read_csv(file_customer)
    print("Sukses Bacanya")
except FileNotFoundError:
    print('eror')
except Exception as e:
    print(f'Terjadi Kesalahan {e}')

#karena belum semuanya date maka kita ubah semua formatnya
df_harga['shipping_limit_date'] = pd.to_datetime(df_harga['shipping_limit_date'])
df_order['order_delivered_carrier_date'] = pd.to_datetime(df_order['order_delivered_carrier_date'])
df_order['order_delivered_customer_date'] = pd.to_datetime(df_order['order_delivered_customer_date'])
df_order['order_estimated_delivery_date'] = pd.to_datetime(df_order['order_estimated_delivery_date'])
df_order['order_purchase_timestamp'] = pd.to_datetime(df_order['order_purchase_timestamp'])

#filter yang ada nan dan juga ada yang tidak 
valid_data = df_order[(df_order['order_status'] == 'delivered') & (df_order['order_delivered_customer_date'].notnull())]

not_valid = df_order[(df_order['order_status'] == 'delivered') & (df_order['order_delivered_customer_date'].isnull())]

#Laporan 
print(f'Ditemukan data bersih sejumlah {len(valid_data)} data bersih dan {len(not_valid)} data kotor')


#Bagian B

#Membandingkan Tanggal mana yang telat (selisih estimasi lebih besar dari aktual) dan mana yang tepat waktu(selisih aktualnya lebih besar daripada selisih estimasi)

## Kita membuat perbandingan langsung dimana jika aktual > estimasi maka telat dan aktual <= estimasi tepat waktu

valid_data['Telat/Tidak'] = valid_data['order_delivered_customer_date'] > valid_data['order_estimated_delivery_date']

## Kita menghitung jumlah yang telat dengan menggunakan sum dan print hasilnya, Dibawah ini bukan merupakan dataframe asli karena berasal dari valid data dan bukan df_order
hasil_telat = valid_data['Telat/Tidak'].sum()

print(f'Jumlah Pesanan Telat adalah {hasil_telat} pesanan')
 
#Hitung Freight Ratio

## Kita harus gabungkan antara valid data dengan df harga berdasarkan order id menggunakan pd.merge

df_gabungan = pd.merge(valid_data,df_harga, on='order_id', how='inner')

## Langsung membuat kolom baru disampingnya yang berisikan hasil hitung price dan freight_value 
df_gabungan['Hasil_Hitung'] = (df_gabungan['freight_value']/df_gabungan['price'])*100


# Menjawab pertanyaan nomor 1 

## Apakah benar 80% keterlambatan disebabkan oleh kondisi tertentu? (Misalnya, rute jarak jauh atau jam sibuk?)

## Kita harus menggunakan analisis pareto untuk melakukan analisis

### kita membutuhkan dataset dari customer dataset untuk mengambil customer statenya, kita merge dengan df gabungan

df_gabungan_akhir = pd.merge(df_gabungan,df_customer,on='customer_id', how='inner')

### Kita filtering karena pareto butuhnya cacat (telat kita hanya hitung yang telat saja)
df_telat = df_gabungan_akhir[df_gabungan_akhir['Telat/Tidak'] == True].reset_index(drop=True)

### Kita hitung dulu berdasarkan customer state
total_telat = df_telat.groupby('customer_state')['Telat/Tidak'].count().sort_values(ascending=False)

### kita hitung persentasenya dulu

persentase_telat = (total_telat/hasil_telat)*100

#laporan

print(f'Top 5 Wilayah Paling Sering Telat:\n1. SP : {total_telat['SP']} kasus {persentase_telat['SP']:.2f}%\n2. RJ : {total_telat['RJ']} kasus {persentase_telat['RJ']:.2f}%\n3. MG : {total_telat['MG']} kasus {persentase_telat['MG']:.2f}%\n4. BA : {total_telat['BA']} kasus {persentase_telat['BA']:.2f}%\n5. RS : {total_telat['RS']} kasus {persentase_telat['RS']:.2f}%\n')



# Menjawab pertanyaan nomor 2

## Berapa total freight_value yang terbuang untuk pesanan yang statusnya 'canceled' atau 'unavailable'?

### Caranya kita filter dulu untuk statusnya yang canceled

canceled_order = df_order[(df_order['order_status'].isin(['canceled', 'unavailable']))].reset_index(drop=True)

###gabungin sama df harga

df_gabungan_canceled = pd.merge(canceled_order,df_harga,on='order_id',how='inner')

### Kita hitung freight valuenya 
total_freight_value = df_gabungan_canceled['freight_value'].sum()

### Kita print dengan kalimat 
print(f'Maka total freight_value pada data yang tidak valid adalah {total_freight_value}')