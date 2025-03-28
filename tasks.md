<!-- markdownlint-disable MD033 -->

# 01 Cvičení CRUD z umělé databáze

Vytvořte si umělou databázi pomocí listů a objektů (například „books“) uloženou v paměti aplikace. Implementujte nad ní CRUD operace (Create, Read, Update, Delete) pro každý model v rámci FastAPI. Ověřte funkčnost voláním jednotlivých endpointů různými HTTP metodami.

<details>
    <summary>Nápověda</summary>

```python

data = [
    {
        
    }

]


@app.get("/data")
def get_all_data()->list[dict]:
    ...

@app.post("/data")
def create_data()-> ? :
    return data

@app.get("/data/{data_id}")
def get_data(...)->dict:
    ...


@app.put("/data/{data_id}")
def update_data(...)->dict:
    ...


@app.delete("/data/{data_id}")
def delete_data(...)->None:
    ...




```

</details>
