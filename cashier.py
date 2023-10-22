import pandas as pd
import json

class Transaction:
    def __init__(self, item_list, columns=['Item', 'Price', 'Qty', 'Total Prices']):
        self.df = pd.DataFrame(columns=columns)
        self.message = 'Order is valid'
        self.item_list = item_list
    
    def get_price(self, search_name):
        '''
        Daftar barang-barang yang bisa dibeli ada di barang.json beserta harganya. 
        Fungsi ini berfungsi untuk mencari harga barang berdasarkan namanya.
        
        '''
        with open(self.item_list, 'r') as file:
            data_list = json.load(file)
            
            for data in data_list:
                if data['item'] == search_name:
                    return data['price']  
            return None

    def add_item(self, item,  qty):
        '''
        Fungsi ini digunakan untuk memasukkan satu buah barang ke daftar belanjaan, rincian yang dimasukkan
        adalah nama barang, harga, dan jumlah. Fungsi akan memeriksa apakah nama barang berupa tipe data 
        string, jumlah barang berupa tipe data integer, dan harga barang berupa tipe data integer. Jika
        tidak sesuai, fungsi ini akan memberitahu pengguna untuk memeriksa kembali pesanan.
        '''
        try:
            price = self.get_price(item)
        except:
            price = ''
       
        if isinstance(item, str) and isinstance(price, int) and isinstance(qty, int):
            row_values = [item, price, qty]
            row_values.append(price*qty)
            self.df = pd.concat([self.df, pd.DataFrame([row_values], columns=self.df.columns)], ignore_index=True)
        else:
            print(self.check_order())
            raise ValueError('Periksa kembali pesanan anda, pastikan anda memasukkan input sesuai urutan')
        
        #if self.df['Barang'].value_counts().get(barang, 0) > 1:
         #   print(self.check_order())
          #  raise ValueError('Barang sudah ada, silakan edit saja jumlahnya')
        
        

    def delete_item(self, item_name):
        '''
        Fungsi ini digunakan untuk menghapus satu rincian barang dari daftar belanjaan. Masukan fungsi ini
        adalah nama barang. Kemudian, fungsi akan memeriksa apakah nama barang yang dimaksud ada di daftar belanjaan.
        Jika ada, rincian tentang barang, harga, dan jumlahnya akan terhapus.
        '''
        try:
            index_to_delete = self.df.index[self.df['Item'] == item_name].tolist()
            if index_to_delete:
                self.df = self.df.drop(index_to_delete)
        except:
           pass
        
    def update_item_name(self, item_name, new_item_name):
       '''
       Fungsi ini digunakan untuk mengedit nama barang. Fungsi akan mencari nama barang yang dimaksud dan akan diganti 
       dengan yang baru. Total harga barang juga disesuaikan dengan barang yang diedit.
       '''
       try:
          self.df.loc[self.df['Item'] == item_name, ['Item', 'Price']] = [new_item_name, self.get_price(new_item_name)]
          for i in range(len(self.df)):
                self.df.loc[i, 'Total Prices'] = self.df.loc[i, 'Qty']*self.df.loc[i, 'Price']
                if isinstance(self.df.loc[i, 'Total Prices'], str):
                    self.df.loc[i, 'Total Prices'] = ''  

       except:
          pass
       
    def update_item_qty(self, item_name, new_item_qty):
       '''
       Fungsi ini digunakan untuk mengedit jumlah barang. Total harga barang juga disesuaikan
       dengan jumlah yang diedit.
       '''
       try:
            self.df.loc[self.df['Item'] == item_name, 'Qty'] = int(new_item_qty)
            for i in range(len(self.df)):
                self.df.loc[i, 'Total Prices'] = self.df.loc[i, 'Qty']*self.df.loc[i, 'Price']
                if isinstance(self.df.loc[i, 'Total Prices'], str):
                    self.df.loc[i, 'Total Prices'] = ''  
       except:
            pass
    '''
    # Saya tidak menerapkan fungsi untuk mengganti harga karena customer tidak seharusnya dapat mengganti harga

    def update_item_price(self, item_name, new_item_price):
       try:
            self.df.loc[self.df['Barang'] == item_name, 'Harga'] = int(new_item_price)
            for i in range(len(self.df)):
                self.df.loc[i, 'Total Harga'] = self.df.loc[i, 'Jumlah']*self.df.loc[i, 'Harga']
                if isinstance(self.df.loc[i, 'Total Harga'], str):
                    self.df.loc[i, 'Total Harga'] = ''
       except:
           pass
    
    '''
    
    def reset_transaction(self):
      '''
      Fungsi ini digunakan untuk menghapus seluruh pesanan sekaligus.
      
      '''
      self.df = self.df.drop(self.df.index)
    
    def check_order(self):
        '''
        Fungsi ini digunakan untuk memeriksa pesanan. Apabila pesanan masih kosong, fungsi ini
        akan memberitahu bahwa terdapat kesalahan input data. Jika tidak ada masalah, fungsi 
        ini akan memberitahu bahwa pesmesanan sudah benar.
        '''

        if self.df.empty:
            self.message = 'Terdapat kesalahan input data'
        else:
            if self.df['Item'].apply(lambda x: isinstance(x, str)).all() and self.df['Qty'].apply(lambda x: isinstance(x, int)).all() and self.df['Price'].apply(lambda x: isinstance(x, int)).all():
                self.message = 'Pemesanan sudah benar'
        return self.df, self.message
    
    def total_prices(self):
      try:
            if not self.df.empty:
                total = self.df['Total Prices'].sum()
                if total > 200000:
                    total = total - total*0.05
                elif total > 300000:
                    total = total - total*0.08
                elif total > 500000:
                    total = total - total*0.1
                return total
            else:
                return 0
      except:
            pass

'''

Test case


buy = Transaction('barang.json')
buy.add_item("Apel", 5)
buy.add_item("Jeruk", 6)
buy.update_item_qty("Jeruk", 7)
buy.update_item_name("Jeruk", "Pisang")
buy.reset_transaction()

print(buy.check_order(), buy.total_prices())

'''
