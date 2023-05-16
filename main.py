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

class UrlRequest(BaseModel):
    url: str

class UrlToUrlRequest(BaseModel):
    url: str
    upload_url: str

class UrlToUrlSplitRequest(BaseModel):
    url: str
    upload_url: str

@app.post("/convert")
async def create_upload_file(file: UploadFile):
    sess = Path(tempfile.mkdtemp())
    contents = await file.read()
    filepath = sess / file.filename
    filepath.write_bytes(contents)
    outfile = sess / filepath.with_suffix(".glb")

    objs = [ob for ob in bpy.context.scene.objects if ob.type in ('CAMERA', 'MESH')]
    bpy.ops.object.delete({"selected_objects": objs})

    if filepath.suffix == '.usdz':
        bpy.ops.wm.usd_import("EXEC_DEFAULT", filepath=str(filepath))
    elif filepath.suffix == '.gltf':
        bpy.ops.import_scene.gltf(filepath=str(filepath))
    elif filepath.suffix == '.obj':
        bpy.ops.import_scene.obj(
            filepath=str(filepath)
        )
    elif filepath.suffix == '.zip':
        folder_unpacked = Path(filepath).with_suffix('')
        shutil.unpack_archive(
            filename=filepath,
            extract_dir=folder_unpacked,
        )
        print(folder_unpacked)
        if len(list(folder_unpacked.glob('**/*.gltf')))>0:
            gltf_file = list(folder_unpacked.glob('**/*.gltf'))[0]
            print("Detected GLTF, at", folder_unpacked)
            bpy.ops.import_scene.gltf(filepath=str(gltf_file))
        elif len(list(folder_unpacked.glob('**/*.obj')))>0:
            obj_file = list(folder_unpacked.glob('**/*.obj'))[0]
            bpy.ops.import_scene.obj(
                filepath=str(obj_file)
            )
        else:
            raise HTTPException(detail=f"Provided zip file didn't have gltf or obj files in it {list(folder_unpacked.glob('*'))}.",status_code=500)
    
    bpy.ops.export_scene.gltf(
        filepath=str(outfile),
        export_format="GLB",
    )
    return FileResponse(
        outfile,
        filename=outfile.name,
    )

@app.post("/convert-from-url")
async def create_upload_file(request: UrlRequest):
    # download file
    sess = Path(tempfile.mkdtemp())
    filename = 'upload.usdz'
    filepath = sess / filename
    filepath.write_bytes(requests.get(request.url).content)

    # contents = await file.read()
    # filepath = sess / file.filename
    # filepath.write_bytes(contents)
    outfile = sess / filepath.with_suffix(".glb")

    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = [ob for ob in bpy.context.scene.objects if ob.type in ('CAMERA', 'MESH')]
    bpy.ops.object.delete({"selected_objects": objs})

    if filepath.suffix == '.usdz':
        bpy.ops.wm.usd_import("EXEC_DEFAULT", filepath=str(filepath))
    elif filepath.suffix == '.gltf':
        bpy.ops.import_scene.gltf(filepath=str(filepath))
    elif filepath.suffix == '.obj':
        bpy.ops.import_scene.obj(
            filepath=str(filepath)
        )
    elif filepath.suffix == '.zip':
        folder_unpacked = Path(filepath).with_suffix('')
        shutil.unpack_archive(
            filename=filepath,
            extract_dir=folder_unpacked,
        )
        print(folder_unpacked)
        if len(list(folder_unpacked.glob('**/*.gltf')))>0:
            gltf_file = list(folder_unpacked.glob('**/*.gltf'))[0]
            print("Detected GLTF, at", folder_unpacked)
            bpy.ops.import_scene.gltf(filepath=str(gltf_file))
        elif len(list(folder_unpacked.glob('**/*.obj')))>0:
            obj_file = list(folder_unpacked.glob('**/*.obj'))[0]
            bpy.ops.import_scene.obj(
                filepath=str(obj_file)
            )
        else:
            raise HTTPException(detail=f"Provided zip file didn't have gltf or obj files in it {list(folder_unpacked.glob('*'))}.",status_code=500)
    
    bpy.ops.export_scene.gltf(
        filepath=str(outfile),
        export_format="GLB",
    )
    return FileResponse(
        outfile,
        filename=outfile.name,
    )

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


