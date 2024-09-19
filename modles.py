from config import db
from datetime import datetime,timezone


class  suppliers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    supplier_name = db.Column(db.String(50), nullable = False)
    supplier_contact_num = db.Column(db.String(15), unique = True, nullable = True)
    lead = db.Column(db.Integer, nullable = True)
    monday = db.Column(db.Boolean)
    tuesday = db.Column(db.Boolean)
    wenesday = db.Column(db.Boolean)
    thursday = db.Column(db.Boolean)
    friday = db.Column(db.Boolean)
    sataday = db.Column(db.Boolean)
    sunday = db.Column(db.Boolean)
    items = db.relationship('items', backref = 'suppliers')

    def to_json(self):
        return {
            "id": self.id,
            "supplierName": self.supplier_name,
            "supplierContactNum": self.supplier_contact_num,
            "lead": self.lead,
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wenesday": self.wenesday,
            "thursday": self.thursday,
            "friday": self.friday,
            "sataday": self.sataday,
            "sunday": self.sunday
        }
    def datalist(self):
        return{
            "id":self.id,
            "main": self.supplier_name,
            "supplierContactNum": self.supplier_contact_num,
            "lead": self.lead,
            "daysDeliver": ["monday" if (self.monday == True) else "","tuesday" if (self.tuesday ==True) else "","wenesday" if (self.wenesday==True) else "","thursday" if(self.thursday == True) else "","friday" if (self.friday ==True) else "" ,"sataday" if (self.sataday==True) else"","sunday" if(self.sunday ==True) else ""]
        }



class stores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    store_name = db.Column(db.String(50), unique = True, nullable = False)
    stock = db.relationship('stock', backref='stores')
    store = db.relationship('rooms', backref = 'stores')

    def to_json(self):
        return{
            "id": self.id,
            "storeName": self.store_name
        }

class rooms(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'),nullable = False)
    room_name = db.Column(db.String(50), unique = True, nullable = False)
    stock = db.relationship('stock', backref = 'rooms')

    def to_json(self):
        return{
            "id": self.id,
            "roomName": self.room_name,
            "storeId": self.store_id
        }
    def datalist(self):
        return{
            "id": self.id,
            "main": self.room_name,
            "storeId": self.store_id
        }

class catagory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    catagory_name = db.Column(db.String(50), unique = True, nullable = False)
    items = db.relationship('items', backref = 'catagory')
    
    def to_json(self):
        return{
            "id": self.id,
            "catagoryName": self.catagory_name
        }

class items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(50), unique = True, nullable = False)
    catagory_id = db.Column(db.Integer, db.ForeignKey('catagory.id'), nullable = True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable = False)
    incident = db.Column(db.Integer, nullable = False)
    stock = db.relationship('stock', backref = 'items')
    
    def to_json(self):
        return{
            "id": self.id,
            "itemName": self.item_name,
            "catagoryId": self.catagory_id,
            "supplierId": self.supplier_id,
            "incidet": self.incident
        }
    def datalist(self):
        cat = ""
        supp = ""
        if self.catagory_id:
            cat = catagory.query.filter_by(id=self.catagory_id).first().catagory_name
        supp = suppliers.query.filter_by(id = self.supplier_id).first().supplier_name
        return{
            "id":self.id,
            "main":self.item_name,
            "catagoryId": self.catagory_id,
            "catagory":cat ,
            "supplierId": self.supplier_id,
            "supplier":supp ,
            "incidet": self.incident
        }

class stock(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False)
    level = db.Column(db.Integer, nullable = False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable = False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable = False)
    logs = db.relationship('logs', backref='stock') 

    def to_json(self):
        return {
            "id": self.id,
            "itemId": self.item_id,
            "level": self.level,
            "roomId":self.room_id,
            "storeId":self.store_id
        }
    
    def stock_table(self,store_id):
        
        item_name = items.query.filter_by(id = self.item_id).first().item_name # type: ignore
        room_name = rooms.query.filter_by(id = self.room_id).first().room_name # type: ignore
        
        return{
            'id': self.id,
            'itemName': item_name,
            'level': self.level,
            'roomName': room_name,
            
        }

    

class logs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'),nullable = False)
    amount_before = db.Column(db.Integer, nullable = False)
    amount_after = db.Column(db.Integer, nullable = False)

    def to_json(self):
        stock_item = stock.query.filter_by(id = self.stock_id).first().item_id
        item_name = items.query.filter_by(id = stock_item).first().item_name
        date = self.datetime
        return{
            "id": self.id,
            "dateTime":self.datetime,
            "stockId":self.stock_id,
            "itemName":item_name,
            "amountBefore": self.amount_before,
            "amountAfter":self.amount_after
        }
    


