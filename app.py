from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "azure-webapps-linux-python-fastapi-basic"}