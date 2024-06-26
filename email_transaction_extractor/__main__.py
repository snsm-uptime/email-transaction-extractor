# email_transaction_extractor/__main__.py
import uvicorn


def run():
    uvicorn.run("email_transaction_extractor.main:app",
                host="127.0.0.1", port=8000, reload=True)
