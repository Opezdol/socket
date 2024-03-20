import uvicorn
from fastapi import FastAPI


app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]
#
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your deals."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
