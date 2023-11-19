"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import errorcode
from pydantic import BaseModel
from typing import List

db_config = {
    "user": "root",
    "password": "smartapp",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "STORAGE",
}

# Connect to tb
try:
    connection = mysql.connector.connect(**db_config)
    print("Connessione al database riuscita")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Errore: Accesso negato.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Errore: Database non esistente.")
    else:
        print(f"Errore: {err}")


class KPI(BaseModel):
    nome: str
    valore: float

class ApiResponse(BaseModel):
    message: str
    
  
    
app = FastAPI()


# Endpoint 
@app.post("/add_kpi", response_model=KPI)
async def add_kpi(kpi: KPI):
    try:
        cursor = connection.cursor()
        query = f"INSERT INTO KPIS (NOME, VALORE) VALUES ('{kpi.nome}', {kpi.valore});"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        return kpi
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Errore del database: {err}")

# curl -X POST "http://localhost:8000/add_kpi" -H "accept: application/json" -H "Content-Type: application/json" -d '{"nome": "NuovoKPI", "valore": 42.0}'




# Endpoint 
@app.get("/", response_model=ApiResponse)
async def api_center():
    return {"message": "API center"}
  



# Endpoint per ottenere tutti i KPI
@app.get("/get_kpis")
async def get_kpis():
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM KPIS;"
        cursor.execute(query)
        kpis = cursor.fetchall()
        cursor.close()
        
        result = [{"nome": kpi["NOME"], "valore": kpi["VALORE"]} for kpi in kpis]
        return result
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Errore del database: {err}")
#curl http://localhost:8000/get_kpis
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import errorcode
from pydantic import BaseModel
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

db_config = {
    "user": "root",
    "password": "smartapp",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "STORAGE",
}

# Connect to tb
try:
    connection = mysql.connector.connect(**db_config)
    print("Connessione al database riuscita")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Errore: Accesso negato.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Errore: Database non esistente.")
    else:
        print(f"Errore: {err}")

class KPI(BaseModel):
    nome: str
    valore: float

class ApiResponse(BaseModel):
    message: str

app = FastAPI()

# Aggiungi HTTPSRedirectMiddleware per reindirizzare HTTP a HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Endpoint
@app.post("/add_kpi", response_model=KPI)
async def add_kpi(kpi: KPI):
    try:
        cursor = connection.cursor()
        query = f"INSERT INTO KPIS (NOME, VALORE) VALUES ('{kpi.nome}', {kpi.valore});"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        return kpi
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Errore del database: {err}")

# Endpoint
@app.get("/", response_model=ApiResponse)
async def api_center():
    return {"message": "API center"}

# Endpoint per ottenere tutti i KPI
@app.get("/get_kpis")
async def get_kpis():
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM KPIS;"
        cursor.execute(query)
        kpis = cursor.fetchall()
        cursor.close()

        result = [{"nome": kpi["NOME"], "valore": kpi["VALORE"]} for kpi in kpis]
        return result

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Errore del database: {err}")
