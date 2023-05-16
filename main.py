from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi import status, HTTPException
from fastapi import Response
import tempfile
from pathlib import Path
import shutil, tempfile
from pathlib import Path
from config import get_config
from ktx2_compress import ktx2_compression
import bpy
import requests
from pydantic import BaseModel
from service import convert_usdz_upload_glb;

app = FastAPI(debug=True)
config = get_config()

class UrlToUrlRequest(BaseModel):
    url: str
    upload_url: str

class UrlToUrlSplitRequest(BaseModel):
    url: str
    upload_url: str

@app.post("/convert-from-url-to-url")
async def create_upload_file(request: UrlToUrlRequest):

    download_url = request.url;
    upload_url = request.upload_url;

    return {"success": True, 'upload_response': convert_usdz_upload_glb(download_url, upload_url)}

@app.post("/convert-payload")
async def create_upload_file(request: UrlToUrlRequest):

    download_url = request.url;
    upload_url = request.upload_url;

    return {"success": True, 'upload_response': convert_usdz_upload_glb(download_url, upload_url)}


