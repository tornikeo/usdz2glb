from fastapi import FastAPI, BackgroundTasks, File, UploadFile
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
from task_queue import get_task_queue, get_job_information

app = FastAPI(debug=True)
config = get_config()

class UrlToUrlRequest(BaseModel):
    url: str
    upload_url: str

class UrlToUrlSplitRequest(BaseModel):
    url: str
    upload_url: str

class JobInfoRequest(BaseModel):
    job_id: str

@app.post("/convert-from-url-to-url")
async def create_upload_file(request: UrlToUrlRequest):

    download_url = request.url;
    upload_url = request.upload_url;

    upload_response = await convert_usdz_upload_glb(download_url, upload_url);

    return {"success": True, 'upload_response': upload_response }

@app.post("/convert-payload-async")
async def create_upload_file(request: UrlToUrlRequest, background_tasks: BackgroundTasks):

    download_url = request.url;
    upload_url = request.upload_url;
    
    lr_task_queue = get_task_queue()

    print("STARTING")
    print(download_url)
    print(upload_url)

    job = lr_task_queue.enqueue(helper, download_url, upload_url)


    return {"success": True, "job_id": job.id}

@app.post("/get_job_info")
async def create_upload_file(request: JobInfoRequest):

    job_id = request.job_id

    print(get_job_information(job_id))

    return {"success": True, "job_info": get_job_information(job_id).get_status()}

get_job_information
async def helper(download_url,upload_url):
    print("CALLED")
    res = await convert_usdz_upload_glb(download_url, upload_url)
    print("DONE DONE DONE")
    print(res)
