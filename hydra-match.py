Trading_market = {"BUY": {
                     150.00 : [{"ID": 101,"qty": 10}, {"ID": 102,"qty": 20}] , 
                     149.00 : [{"ID": 103, "qty": 15}, {"ID": 104, "qty": 35}]
                  },
                  "SELL" : {
                      151.00 : [{"ID": 201,"qty": 5}, {"ID": 202,"qty": 17}],
                      148.00 : [{"ID": 203,"qty": 25}, {"ID": 204,"qty": 30}]
                  }
}
def process_new_order(incoming_side, incoming_price, incoming_qty, order_ID):
    if incoming_side == "BUY":
        opposite_side = "SELL"
        own_side = "BUY"
    else:
        opposite_side = "BUY"
        own_side = "SELL"
    while incoming_qty > 0:
        if len(Trading_market[opposite_side]) == 0:
            break #No seller left, no need for looping

        if opposite_side == "SELL":
            best_opposing_price = min(Trading_market[opposite_side].keys())
            if best_opposing_price > incoming_price:
                print(f"Seller ({best_opposing_price}) is too expensive for buyer ({incoming_price})")
                break 
        
        else:
            best_opposing_price = max(Trading_market[opposite_side].keys())
            if best_opposing_price < incoming_price:
                print(f"Buyer ({best_opposing_price}) is offering too little to our seller ({incoming_price})")
                break 

        current_match = Trading_market[opposite_side][best_opposing_price][0]
    
        sell = current_match["qty"]

        if sell > incoming_qty:
            inventory = sell - incoming_qty
            print("The Buyer's need was fulfilled")
            current_match["qty"] = inventory
            incoming_qty = 0
            print(Trading_market)
        elif incoming_qty > sell:
            inventory = incoming_qty - sell
            print("The buyer is not satisfied, still needs a seller")
            incoming_qty = incoming_qty - sell
            del Trading_market[opposite_side][best_opposing_price][0]
            if len(Trading_market[opposite_side][best_opposing_price]) == 0:
                del Trading_market[opposite_side][best_opposing_price]
        else:
            print("Perfect Match!! Both orders are cleared")
            del Trading_market[opposite_side][best_opposing_price][0]
            if len(Trading_market[opposite_side][best_opposing_price]) == 0:
                del Trading_market[opposite_side][best_opposing_price]
                incoming_qty = 0
    if incoming_qty > 0:
        print()
        if incoming_price not in Trading_market[own_side]:
            Trading_market[own_side][incoming_price] = []
        Trading_market[own_side][incoming_price].append({"ID" : order_ID , "qty" : incoming_qty})

print("------BEFORE TRANSACTION------")
print(Trading_market)
print("\n-----------------------------------\n")

process_new_order("SELL", 147.00 , 400 , 99)

print("\n-------AFTER TRANSACTION-------")
print(Trading_market)
