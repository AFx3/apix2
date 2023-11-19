openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365

uvicorn main:app --host localhost --port 8000 --reload

sudo uvicorn main:app --host 127.0.0.1 --port 8000 --reload --ssl-keyfile key.pem --ssl-certfile cert.pem

sudo uvicorn main:app --host 127.0.0.1 --port 443 --reload --ssl-keyfile key.pem --ssl-certfile cert.pem 

curl --insecure -X POST "https://localhost:8000/add_kpi" -H "accept: application/json" -H "Content-Type: application/json" -d '{"nome": "NuovoKPI", "valore": 42.0}'

curl --insecure https://127.0.0.1:8000/get_kpis

sudo chmod -R 777 /home/af/Video/a/mysql/data