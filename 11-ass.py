def  start_charging(drivers_db, stations_db, driver_id, station_id, kwh_amount):
    if driver_id not in drivers_db:
        raise KeyError('Driver not found')
    driver_info = drivers_db[driver_id]


    if station_id  not in stations_db :
        raise KeyError ('Station offline')
    price_per_kwh = stations_db[station_id]["price"]


    if (type(kwh_amount) != int and type(kwh_amount)!= float) or kwh_amount <= 0 :
        raise ValueError ('Invalid kWh amount')
    
    total_cost = kwh_amount * price_per_kwh 

    
    if driver_info['plan'] == 'Subscriber':
        total_cost= total_cost * 0.75

    if driver_info['wallet'] < total_cost:
        raise ValueError ('Insufficient funds')
    driver_info['wallet'] -= total_cost
    return total_cost
    
    


def batch_charge_requests(drivers_db, stations_db, request_list):
    revenue = 0.0
    denied_sessions = 0
    
    for request in request_list:
        driver_id, station_id, kwh_amount = request
        try:
            
            cost = start_charging(drivers_db, stations_db, driver_id, station_id, kwh_amount)
            revenue += cost
        except (KeyError , ValueError) as e:
            print('Charge Error for' , driver_id, ':', e)
            denied_sessions += 1
    return {'revenue' : revenue , 'denied_sessions': denied_sessions }
stations = {
    "S_Fast": {"price": 0.50},
    "S_Slow": {"price": 0.20}
}

drivers = {
    "D1": {"wallet": 10.0, "plan": "Guest"},
    "D2": {"wallet": 10.0, "plan": "Subscriber"} # 25% off
}

requests = [
    ("D1", "S_Slow", 20),      
    ("D2", "S_Fast", 20),      
    ("D1", "S_Fast", 50),  
    ("D1", "S_Hyper", 10), 
    ("D9", "S_Slow", 10),   
    ("D1", "S_Slow", -5)      
]

print(batch_charge_requests(drivers, stations, requests))
 





