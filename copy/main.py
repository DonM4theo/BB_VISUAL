from fastapi import FastAPI, Request
import pyodbc
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="templates/static"), name="static")
templates = Jinja2Templates(directory="templates")

# volume - ilość wyświetlanych rekordów TOP *
volume = 3
# URL DATA
DB = "MG_GT"
DB_SERVER = "SL-SQL"
DB_USER = "srv-wizual"
DB_PASSWORD = "DNy6013701C"
DB_DRIVER = "{ODBC Driver 17 for SQL Server}"

db_URL = (f"DRIVER={DB_DRIVER};"
          f"Server={DB_SERVER};"
          f"Database={DB};"
          f"UID={DB_USER};"
          f"PWD={DB_PASSWORD};"
          # "Trusted_Connection=yes;"
          )

@app.get('/', tags=["GetDataFromLine"], response_class=HTMLResponse)
def get_programs(request: Request):
    try:
        conn = pyodbc.connect(db_URL)
        query_znk_1 = f"""SELECT TOP ({volume}) * FROM  dbo.wusr_fn_mg_AktywneZlecenieOdProdukcji('ZNK1')"""
        query_znk_2 = f"""SELECT TOP ({volume}) * FROM  dbo.wusr_fn_mg_AktywneZlecenieOdProdukcji('ZNK2')"""
        query_znk_3 = f"""SELECT TOP ({volume}) * FROM  dbo.wusr_fn_mg_AktywneZlecenieOdProdukcji('ZNK1:D1')"""
        
        cursor = conn.cursor()
        cursor.execute(query_znk_1)
        list_znk_1 = cursor.fetchall()
        cursor.execute(query_znk_2)
        list_znk_2 = cursor.fetchall()
        cursor.execute(query_znk_3)
        list_znk_1d1 = cursor.fetchall()

        conn.close()
    except pyodbc.OperationalError:
        conn.close()
        return HTMLResponse("__Server MSSQL is not found or not accessible__")
    
    return templates.TemplateResponse("widok.html", {"request": request, "list_znk_1": list_znk_1, "list_znk_2": list_znk_2, "list_znk_1d1": list_znk_1d1})