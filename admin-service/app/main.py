from fastapi import FastAPI

app = FastAPI()


@app.get("/addurl")
async def api_addurl(url: str):
    return {"message": url}
