import json
import mysql.connector
from CollectedPlatesModel import CollectedPlatesModel



with open('appsettings.json', 'r') as file:
    c = json.load(file)


mydb = mysql.connector.connect(
    host=c["host"],
    user=c["user"],
    password=c["password"],
    database=c["database"]
)


async def fetch_data_from_base(plate: str):

    mycursor = mydb.cursor()

    query = "SELECT AutoPlate, AutoModel, Company, Contact FROM InsertedAutoPlates WHERE AutoPlate = %s"
    mycursor.execute(query, (plate,))
    
    rows = mycursor.fetchall()
    
    results = [CollectedPlatesModel(*row) for row in rows]

    return results