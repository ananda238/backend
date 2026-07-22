from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import transactions, dashboard, exchange, auth

app = FastAPI(title="MoneyWise API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)
app.include_router(dashboard.router)
app.include_router(exchange.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "MoneyWise API is running!"}