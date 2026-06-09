from fastapi import fastAPI

app = fastAPI()

@app.get("/")
def home():
    return {"msg":{"API Online"}}