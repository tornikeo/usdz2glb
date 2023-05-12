from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi import status, HTTPException
from fastapi import Response
import tempfile
from pathlib import Path
import shutil, tempfile
from pathlib import Path

app = FastAPI(debug=True)

@app.post("/convert")
async def create_upload_file(file: UploadFile):
    sess = Path(tempfile.mkdtemp())
    contents = await file.read()
    filepath = sess / file.filename
    filepath.write_bytes(contents)
    outfile = sess / filepath.with_suffix(".glb")

    import bpy

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

import requests
from pydantic import BaseModel
class UrlRequest(BaseModel):
    url: str

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

    import bpy
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

class UrlToUrlRequest(BaseModel):
    url: str
    upload_url: str

@app.post("/convert-from-url-to-url")
async def create_upload_file(request: UrlToUrlRequest):
    # download file
    sess = Path(tempfile.mkdtemp())
    filename = 'upload.usdz'
    filepath = sess / filename
    filepath.write_bytes(requests.get(request.url).content)

    # contents = await file.read()
    # filepath = sess / file.filename
    # filepath.write_bytes(contents)
    outfile = sess / filepath.with_suffix(".glb")

    import bpy
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

    # upload file
    files = {'file': open(outfile, 'rb')}
    
    return {"success": True, 'upload_response': requests.put(request.upload_url, files=files).content.decode('utf-8')}
