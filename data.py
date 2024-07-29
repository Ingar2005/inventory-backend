from config import db
from modles import *



aig = suppliers(supplier_name= 'aig',lead=2,monday = True,tuesday= True,wenesday= True,thursday= True,friday= True,sataday= True,sunday= False)
db.session.add(aig)
db.session.commit()
aig = suppliers.query.filter_by(supplier_name = 'aig').first()

leicester = stores(store_name= '158 evington rd')
db.session.add(leicester)
db.session.commit()
leicester = stores.query.filter_by(store_name= '158 evington rd').first()

downstairs = rooms(store_id = leicester.id , room_name = 'downstairs storage')
db.session.add(downstairs)
db.session.commit()
downstairs = rooms.query.filter_by(room_name = 'downstairs storage').first()

milk = items(item_name = 'milk', supplier_id = aig.id,incident = 2)
db.session.add(milk)
db.session.commit()
milk = items.query.filter_by(item_name = 'milk').first()

lc_milk = stock(item_id = milk.id, level = 4, room_id = downstairs.id, store_id = leicester.id )
db.session.add(lc_milk)
db.session.commit()
lc_milk = stock.query.filter_by(level = 4).first()



