import os


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from workflow-scratch-2!"}


##TODO: Add workflow routing
app.include_router("")

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", 8000)

    uvicorn.run(app, host=host, port=port)
