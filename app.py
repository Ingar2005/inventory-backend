from flask import request,jsonify
from config import app,SessionLocal
from config import db
from modles import *
import os
store_id = 1

# - read
# - stock tabble ~~~
# - items + single from name/id ~
# - rooms + single from name/ id ~
# - suppliers ~
# log
# catagory
# store

#READ
@app.route("/stock_table", methods=["GET"])
def get_stock_table():
    stock_lst = stock.query.all()
    json_content = list(map(lambda obj: obj.stock_table(store_id), stock_lst))
    return jsonify (json_content)
@app.route("/stock/<int:room_id>", methods=["GET"])
def get_stock(room_id):
    stock_lst = stock.query.filter_by(room_id = room_id)
    json_content = list(map(lambda obj: obj.stock_table(store_id), stock_lst))
    return jsonify (json_content)

@app.route("/items", methods=["GET"])
def get_items():
    item_lst = items.query.all()
    json_content = list(map(lambda obj: obj.to_json(), item_lst))
    return jsonify (json_content)
@app.route("/items/data-list", methods=["GET"])
def get_items_datalist():
    item_lst = items.query.all()
    json_content = list(map(lambda obj: obj.datalist(), item_lst))
    return jsonify (json_content)



@app.route("/suppliers", methods=["GET"])
def get_suppliers():
    suppliers_lst = suppliers.query.all()
    json_content = list(map(lambda obj: obj.to_json(),suppliers_lst))
    return jsonify(json_content)
@app.route("/suppliers/data-list", methods=["GET"])
def get_suppliers_datalist():
    item_lst = suppliers.query.all()
    json_content = list(map(lambda obj: obj.datalist(), item_lst))
    return jsonify (json_content)

@app.route("/rooms", methods=["GET"])
def get_rooms():
    rooms_lst = rooms.query.all()
    json_content = list(map(lambda obj: obj.to_json(),rooms_lst))
    return jsonify(json_content)
@app.route("/rooms/data-list", methods=["GET"])
def rooms_datalist():
    rooms_lst = rooms.query.all()
    json_content = list(map(lambda obj: obj.datalist(),rooms_lst))
    return jsonify(json_content)

@app.route("/link_supplier/<int:supplier_id>", methods=["GET"])
def supplier_link(supplier_id):
    json_content = {}
    supplier = suppliers.query.filter_by(id = supplier_id).first()
    dependent = supplier.items
    if dependent:
        json_content = list(map(lambda obj: obj.to_json(),dependent))
    return jsonify(json_content),200

@app.route("/link_item/<int:item_id>", methods=["GET"])
def item_link(item_id):
    json_content = {}
    supplier = suppliers.query.filter_by(id = item_id).first()
    dependent = supplier.items
    if dependent:
        json_content = list(map(lambda obj: obj.to_json(),dependent))
    print(json_content)
    return jsonify(json_content),200

@app.route("/logs", methods=["GET"])
def get_logs():
    log = logs.query.all()
    json_content = list(map(lambda obj: obj.to_json(),log))
    return jsonify(json_content)

# - if thy dont exist it will return none
# CREATE
#
# - new item ~~~
# - new stock instance ~~
# - new log ~~
# - new supplier ~~~
# - new catagory
# - new store
# - new room 

@app.route("/create_item", methods =["POST"])
def create_item():
    res =""
    new_item_name = request.json.get("itemName") # type: ignore
    new_supplier = request.json.get("supplier") # type: ignore
    new_incident = request.json.get("incidentLevel") # type: ignore
    supplier= suppliers.query.filter_by(supplier_name = new_supplier).first()
    is_name_used = items.query.filter_by(item_name = new_item_name).first()
    if not new_item_name:
        res += "must contain item name "
    elif is_name_used:
        res += "must contain a unique item name"
    if not new_supplier:
        res += "must contain supplier "
    elif not supplier:
        res += "must use a real supplier "
    if not new_incident:
        res += "must contain incident level "
    
    if len(res) == 0 :
        new_item = items(item_name=new_item_name, supplier_id=supplier.id, incident=new_incident) # type: ignore
        try:
            db.session.add(new_item)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}),400
        
        return jsonify({"message":"item created"}),201
    else:
        return jsonify({"message":res}), 400

@app.route("/create_stock", methods = ["POST"])
def create_stock():
    level = request.json.get("level")
    room_name = request.json.get("roomName")
    item_name = request.json.get("itemName")
    
    response = ""
    accept = True
    item_filter= items.query.filter_by(item_name = item_name).first()
    if item_filter:
        unique = stock.query.filter_by(item_id=item_filter.id,store_id=store_id).first()
    room_valid = rooms.query.filter_by(room_name= room_name,store_id=store_id).first()
    if item_filter == None:
        accept = False
        response +="must contain a valid item "
    elif unique != None:
        accept = False
        response +="must use unique item (item not used already) "
    
    if room_valid == None:
        accept = False
        response +="must use existing room "    

    if accept == False:
        return jsonify({"message":response}),400
    
    item_id = item_filter.id #becouse item filter would have returned the object
    room_id = room_valid.id
    new_stock = stock(item_id = item_id, level = level, room_id = room_id, store_id= store_id)
    try:
        db.session.add(new_stock)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message":"stock created"}),201 

@app.route("/create_supplier", methods=["POST"])
def create_supplier():
    supplier_name = request.json.get("supplierName")
    supplier_contact_num = ""
    lead =  request.json.get("lead")
    monday = request.json.get("monday")
    tuesday = request.json.get("tuesday")
    wenesday = request.json.get("wenesday")
    thursday = request.json.get("thursday")
    friday = request.json.get("friday")
    sataday = request.json.get("sataday")
    sunday = request.json.get("sunday")

    if not supplier_name:
        return jsonify({"message":"must contain a supplier name"})
    new_supplier = suppliers(supplier_name = supplier_name, lead=lead, monday= monday,tuesday=tuesday ,wenesday=wenesday,thursday=thursday, friday=friday,sataday=sataday,sunday=sunday)
    
    try:
        db.session.add(new_supplier)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message":"supplier created"}),201 

@app.route("/create_room", methods= ["POST"])
def create_room():
    room_name = request.json.get("roomName")
    store_id =1  

    if not room_name:
        return jsonify({"message":"must contain a room name"})
    elif ( rooms.query.filter_by(room_name = room_name).first()):
        return jsonify({"message":"name already in use"}),404
    new_room = rooms(room_name=room_name, store_id=store_id)

    try:
        db.session.add(new_room)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message":"room created"}),201 

def new_log(stock_id,before,after):
    log = logs(stock_id = stock_id, amount_before=before,amount_after =after)

    try:
        db.session.add(log)
        db.session.commit()
    except:
            return False
    
    return True


#UPDATE 
#
# 
# item ~~
# stock ~~
# log
# supplier ~~
# catagory
# store
# room


@app.route("/update_item/<int:item_id>", methods= ["PATCH"])
def update_item(item_id):
    item = items.query.get(item_id)
    
    if not item:
        return jsonify({"message":"item not found"}),404
    
    data = request.json

    supplier_id = suppliers.query.filter_by(supplier_name = data.get("supplier")).first().id
    item_name = data.get("itemName")
    if item_name != item.item_name:
        there = items.query.filter_by(item_name=item_name).first()
        if there:
            return jsonify({"message":"please use a unique item name"}),400
            
    item.item_name = data.get("itemName",item.item_name)
    item.supplier_id = data.get(supplier_id,item.supplier_id)
    item.incident = data.get("incidentLevel",item.incident)
    db.session.commit()

    return jsonify({"message":"item updated"}),200

@app.route("/update_stock/<int:stock_id>", methods = ["PATCH"])
def update_stock(stock_id):
    stock_item = stock.query.get(stock_id)

    if not stock_item:
        return jsonify({"message":"stock item not found"}),404
    
    data = request.json

    new_room =  rooms.query.filter_by(room_name = data.get("roomName")).first()
    new_item = items.query.filter_by(item_name = data.get("itemName")).first()

    if new_room != None and new_item != None:
        if data.get("level") != stock_item.level:
            new_log(stock_id,stock_item.level,data.get("level"))
            stock_item.level = data.get("level",stock_item.level)

        stock_item.room_id = (new_room.id)
        stock_item.item_id = (new_item.id)
        db.session.commit()

        return jsonify({"message":"stock item updated"}),200

@app.route("/update_supplier/<int:supplier_id>", methods= ["PATCH"])
def update_supplier(supplier_id):
    supplier = suppliers.query.get(supplier_id)
    if not supplier:
        return jsonify({"message":"supplier not found"}),404
    data = request.json
    supplier.supplier_name = data.get("supplierName",supplier.supplier_name)
    supplier.supplier_contact_num = data.get("supplierNumber",supplier.supplier_contact_num)
    supplier.lead = data.get("lead",supplier.lead)

    supplier.monday=False
    supplier.tuesday=False
    supplier.wenesday=False
    supplier.thursday=False
    supplier.friday=False
    supplier.sataday=False
    supplier.sunday=False
    db.session.commit()

    return jsonify({"message":"supplier updated"}),200

@app.route("/update_room/<int:room_id>", methods= ["PATCH"])
def update_room(room_id):
    room = rooms.query.get(room_id)
    data = request.json

    if not room:
        return jsonify({"message":"room not found"}),404
    
    elif ( rooms.query.filter_by(room_name = data.get("roomName")).first()):
        return jsonify({"message":"name already in use"}),404

    room.room_name = data.get("roomName",room.room_name)
    room.store_id = 1

    db.session.commit()

    return jsonify({"message":"room updated"}),200

# DELETE
# item ~~
# stock ~~
# log
# supplier ~~
# catagory
# store
# room

@app.route("/delete_item/<int:item_id>", methods = ["DELETE"])
def delete_item(item_id):
    item = items.query.get(item_id)
    if not item:
        return ({"message":"item not found"}),400
    
    stock_items = item.stock
    for stock in stock_items:
        delete_stock(stock.id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message":"item deleted"}),200

@app.route("/delete_stock/<int:stock_id>", methods = ["DELETE"])
def delete_stock(stock_id):
    stock_item= stock.query.get(stock_id)

    if not stock_item:
        return ({"message":"stock not found"}),400
    
    log_list = logs.query.filter_by(stock_id = stock_item.id).all()
    for log in log_list:
        db.session.delete(log)
        db.session.commit()

    db.session.delete(stock_item)
    db.session.commit()

    return jsonify({"message":"stock deleted"}),200
@app.route("/delete_supplier/<int:supplier_id>", methods = ["DELETE"])
def delete_supplier(supplier_id):
    supplier_item= suppliers.query.get(supplier_id)
    if not supplier_item or supplier_item.id ==1:
        return ({"message":"supplier not found"}),400
    print("got here")
    supplier_items_list = supplier_item.items

    for item in supplier_items_list:
        item.supplier_id =(suppliers.query.filter_by(supplier_name = "generic").first().id)
        db.session.commit()
    db.session.delete(supplier_item)
    db.session.commit()

    return jsonify({"message":"supplier deleted"}),200

@app.route("/delete_room/<int:room_id>", methods = ["DELETE"])
def delete_room(room_id):
    room_item= rooms.query.get(room_id)
    generic = rooms.query.filter_by(room_name = "generic").first()
    if not room_item or room_item.id == generic.id:
        return ({"message":"room not found"}),400
    referential_integrity = room_item.stock
    for stock in referential_integrity:
        stock.room_id = generic.id
        db.session.commit()
        
    db.session.delete(room_item)
    db.session.commit()

    return jsonify({"message":"room deleted"}),200

@app.route("/delete_log/<int:log_id>", methods = ["DELETE"])
def delete_log(log_id):
    log_item= logs.query.get(log_id)
    if not log_item:
        return ({"message":"log not found"}),400
    before = log_item.amount_before
    after = log_item.amount_after
    diff = before - after
    stock_item = stock.query.filter_by(id = log_item.stock_id).first()
    count = stock_item.level
    count = count +diff
    stock_item.level = count
    db.session.commit()

    db.session.delete(log_item)
    db.session.commit()
    return jsonify({"message":"log deleted"}),200


# @app.route("/delete_zzz/<int:zzz_id>", methods = ["DELETE"])
# def delete_zzz(zzz_id):
#     zzz_item= zzz.query.get(zzz_id)
#     if not zzz_item:
#         return ({"message":"zzz not found"}),400
#     db.session.delete(zzz_item)
#     db.session.commit()

#     return jsonify({"message":"zzz deleted"}),200


@app.route('/')
def hello_world():

    return 'Hello, World!'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()