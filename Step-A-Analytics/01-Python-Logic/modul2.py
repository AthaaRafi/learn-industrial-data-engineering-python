import pandas as pd
import numpy as np # Library untuk numerik, NaN asalnya dari sini

data_gudang = {
    'Barang': ['Baut', 'Mur', 'Paku', 'Obeng'],
    'Stok': [100, 50, 0, 10],            # 0 artinya stok habis
    'Harga_Satuan': [500, 100, 200, np.nan] # NaN artinya harga belum diinput admin
}

df = pd.DataFrame(data_gudang)

rata_harga = df['Harga_Satuan'].mean()
df['Harga_Satuan'].fillna(rata_harga, inplace=True)


df['Total_Aset'] = df['Stok'] * df['Harga_Satuan']

df_stok = df[df['Stok'] < 20].sort_values(by='Total_Aset', ascending=False, ignore_index=True)



print(df_stok)