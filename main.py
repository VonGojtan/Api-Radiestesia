from fastapi import fastapi

app = fastapi()

@app.get("/")
def home():
    return {"msg":{"API Online"}}