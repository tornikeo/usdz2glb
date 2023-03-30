from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import tempfile
from pathlib import Path


app = FastAPI(debug=True)

@app.post('/convert')
async def create_upload_file(file: UploadFile):
    sess = Path(tempfile.mkdtemp())
    contents = await file.read()
    filepath = (sess / file.filename)
    filepath.write_bytes(contents)
    return FileResponse(
        filepath, 
        filename=file.filename,
    )