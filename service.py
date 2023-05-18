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


config = get_config();
def convert_usdz_file_to_glb(file_usdz_src, file_glb_dest):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = [ob for ob in bpy.context.scene.objects if ob.type in ('CAMERA', 'MESH')]
    bpy.ops.object.delete({"selected_objects": objs})

    # TODO: If file id invalid and cannot be open error is logged to console but not thrown
    if file_usdz_src.suffix == '.usdz':
        bpy.ops.wm.usd_import("EXEC_DEFAULT", filepath=str(file_usdz_src))
    elif file_usdz_src.suffix == '.gltf':
        bpy.ops.import_scene.gltf(filepath=str(file_usdz_src))
    elif file_usdz_src.suffix == '.obj':
        bpy.ops.import_scene.obj(
            filepath=str(file_usdz_src)
        )
    elif file_usdz_src.suffix == '.zip':
        folder_unpacked = Path(file_usdz_src).with_suffix('')
        shutil.unpack_archive(
            filename=file_usdz_src,
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

    # TODO: Clear blender to save memory (if needed)
    bpy.ops.export_scene.gltf(
        filepath=str(file_glb_dest),
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
        export_draco_position_quantization=config.QUANTIZATION
    )

async def convert_usdz_upload_glb(url_download, url_upload):
    # download file
    sess = Path(tempfile.mkdtemp())
    filename = 'upload.usdz'
    file_usdz = sess / filename
    file_usdz.write_bytes(requests.get(url_download).content)

    filename = 'upload.glb'
    file_glb = sess / filename

    # Convert usdz file to glb file
    convert_usdz_file_to_glb(file_usdz, file_glb);

    # Compress glb file using ktx2
    filename = 'upload_compressed.glb'
    file_glb_compressed = sess / filename
    upload_File = ktx2_compression(file_glb, file_glb_compressed)

    # Upload file
    upload_result = requests.put(
        url_upload, 
        data=open(upload_File, 'rb'),
        headers={
            'Content-Type': 'application/octet-stream',
        });
    
    return upload_result.status_code
