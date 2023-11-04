# CashierProject

## Background

## Feature Requirements
1. Customers can start the transaction by defining an object
```
transaction_1 = Transaction()
```

2. Customers see the available items 
```
transaction_1.see_available_items()
```
and then add the item they want to buy
```
transactions_1.add_item(item_name, item_qty)
```

3. Customers can change the item they want to buy or change the quantity of the item. They cannot change the price, because customers shouldn't be able to change the price
- To change the item
```
transaction_1.update_item_name(item_name, new_item_name)
```
- To change the item quantity
```
transaction_1.update_item_qty(item_name, new_item_qty)
```

4. Customers can delete the item in their trolley
- To delete one item
```
transaction_1.delete_item(item_name)
``` 
- To delete all items
```
transaction_1.reset_transaction()
```

5. Customers can check their trolley, so they can still edit the item or the quantity if needed
```
transaction_1.check_order()
```

6. Customers can see the total price they should pay
```
transaction_1.total_price()
```
Customers will get discounts as follows:
- If the total price is 200000 units, there will be 50% discount
- If the total price is 300000 units, there will be 8& discount
- If the total price is 500000 units, there will be 10% discount 
