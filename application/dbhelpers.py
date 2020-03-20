from application import db
from application.models import *
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'ambflexjson.json', scope) # Your json file here

gc = gspread.authorize(credentials)

wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1kzSEuwhU0cqFeCkG--0Q4V_hAkAXPejA_vsHgm2ML5s/edit?usp=sharing")

#products
products_sheet = wks.worksheet("products")
products_data = products_sheet.get_all_values()
products_headers = products_data.pop(0)
products_df = pd.DataFrame(products_data, columns=products_headers)

#cdds
cdds_sheet = wks.worksheet("cdds")
cdds_data = cdds_sheet.get_all_values()
cdds_headers = cdds_data.pop(0)
cdds_df = pd.DataFrame(cdds_data, columns=cdds_headers)

#clients
clients_sheet = wks.worksheet("clients")
clients_data = clients_sheet.get_all_values()
clients_headers = clients_data.pop(0)
clients_df = pd.DataFrame(clients_data, columns=clients_headers)

#vehicles
vehicles_sheet = wks.worksheet("vehicles")
vehicles_data = vehicles_sheet.get_all_values()
vehicles_headers = vehicles_data.pop(0)
vehicles_df = pd.DataFrame(vehicles_data, columns=vehicles_headers)

def Populate():
    #Products
    for row_id in range(len(products_df)):
        args={}
        for column_id in range(len(products_headers)):
            key=products_headers[column_id]
            value=products_df[products_headers[column_id]][row_id]
            args[key]=value
        new_product=Product(**args)
        db.session.add(new_product)

    #CDDs
    for row_id in range(len(cdds_df)):
        args={}
        for column_id in range(len(cdds_headers)):
            key=cdds_headers[column_id]
            value=cdds_df[cdds_headers[column_id]][row_id]
            args[key]=value
        new_cdd=CDD(**args)
        db.session.add(new_cdd)
        
    #Clients
    for row_id in range(len(clients_df)):
        args={}
        for column_id in range(len(clients_headers)):
            key=clients_headers[column_id]
            value=clients_df[clients_headers[column_id]][row_id]
            args[key]=value
        new_client=Client(**args)
        db.session.add(new_client)
        
    #Vehicles
    for row_id in range(len(vehicles_df)):
        args={}
        for column_id in range(len(vehicles_headers)):
            key=vehicles_headers[column_id]
            value=vehicles_df[vehicles_headers[column_id]][row_id]
            args[key]=value
        new_vehicle=Vehicle(**args)
        db.session.add(new_vehicle)
    
    db.session.commit()
    
def CreateDatabase():
    db.create_all()
    Populate()
    
