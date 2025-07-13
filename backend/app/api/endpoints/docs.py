from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

from backend.app.rag.ingest import ingest_file

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    if not filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF or TXT files are supported")

    save_path = f"docs/{filename}"
    os.makedirs("docs", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    chunks_added = ingest_file(save_path)
    return JSONResponse(status_code=200, content={"msg": "File ingested", "chunks": chunks_added})
