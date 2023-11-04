import pandas as pd
import json

class Transaction:
    def __init__(self, columns=['Item', 'Price', 'Qty', 'Total Prices']):
        self.df = pd.DataFrame(columns=columns)
        self.message = 'Order is valid'
        self.item_list = 'barang.json'
    
    def get_price(self, search_name):
        '''
       
        This function searches for item's price 

        search_name : string 
        
        '''
        with open(self.item_list, 'r') as file:
            data_list = json.load(file)
            
            for data in data_list:
                if data['item'] == search_name:
                    return data['price']  
            return None
    
    def see_available_items(self):
        with open(self.item_list, 'r') as file:
            data_list = json.load(file)
        available_items = pd.DataFrame(data_list)
        print(available_items)
    


    def add_item(self, item,  qty):
        '''
        This function adds item to the trolley

        item : string (the name of the item that we want to add)
        qty : int (how many of the item that we want to add)
        
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
        This function deletes an item

        item_name : string (name of the item that we want to delete)
        '''
        try:
            index_to_delete = self.df.index[self.df['Item'] == item_name].tolist()
            if index_to_delete:
                self.df = self.df.drop(index_to_delete)
        except:
           pass
        
    def update_item_name(self, item_name, new_item_name):
       '''
       This function changes an item to another item

       item_name : string (name of the item that we want to change)
       new_item_name : string (name of the item that we want to change with)
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
       This item edit the quantity of an item

       item_name : string (name of the item that we want to change the quantity)
       new_item_qty : the new quantity of the item 
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
    # There is no function to update the price because customer should not be able to change the price

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
      This function reset the trolley
      
      '''
      self.df = self.df.drop(self.df.index)
    
    def check_order(self):
        '''
        This function gives information about all the items in the trolley
        '''

        if self.df.empty:
            self.message = 'There is an error in the input'
        else:
            if self.df['Item'].apply(lambda x: isinstance(x, str)).all() and self.df['Qty'].apply(lambda x: isinstance(x, int)).all() and self.df['Price'].apply(lambda x: isinstance(x, int)).all():
                self.message = 'Order is valid'
        return self.df, self.message
    
    def total_price(self):
      '''
      This function gives the total price
      '''
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


