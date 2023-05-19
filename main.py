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
from service import convert_usdz_upload_glb, convert_and_send_confirmation, ResponseInfo;
from task_queue import get_task_queue, get_job_information

app = FastAPI(debug=True)
config = get_config()

class UrlToUrlRequest(BaseModel):
    url: str
    upload_url: str

class UrlToUrlQueueRequest(BaseModel):
    to_convert_url: str
    to_upload_url: str
    x_access_token: str
    callback_url: str
    organization_id: str
    device_name: str
    lat: str
    lon: str
    session_id: str
    scanning_type_id: str
    subscription_type: str
    firebase_device_token: str
    model_name: str

class JobInfoRequest(BaseModel):
    job_id: str

@app.post("/convert-from-url-to-url")
async def create_upload_file(request: UrlToUrlRequest):

    download_url = request.url;
    upload_url = request.upload_url;

    upload_response = await convert_usdz_upload_glb(download_url, upload_url);

    return {"success": True, 'upload_response': upload_response }

@app.post("/convert-payload-async")
async def create_upload_file(request: UrlToUrlQueueRequest):

    download_url = request.to_convert_url;
    upload_url = request.to_upload_url;
    
    payload = ResponseInfo();
    payload.x_access_token = request.x_access_token
    payload.callback_url = request.callback_url
    payload.organization_id = request.organization_id
    payload.device_name = request.device_name
    payload.lat = request.lat
    payload.lon = request.lon
    payload.session_id = request.session_id
    payload.scanning_type_id = request.scanning_type_id
    payload.subscription_type = request.subscription_type
    payload.firebase_device_token = request.firebase_device_token
    payload.model_name = request.model_name

    lr_task_queue = get_task_queue()
    job = lr_task_queue.enqueue(convert_and_send_confirmation, download_url, upload_url, payload)

    return {"success": True, "job_id": job.id}

@app.post("/get_job_info")
async def create_upload_file(request: JobInfoRequest):

    job_id = request.job_id

    print(get_job_information(job_id))

    return {"success": True, "job_info": get_job_information(job_id).get_status()}
