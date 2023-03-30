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
    import bpy


    bpy.ops.wm.usd_import("EXEC_DEFAULT", filepath=str(filepath))
    outfile = sess / filepath.with_suffix('.glb')

    bpy.ops.export_scene.gltf(
        filepath=str(outfile),
        check_existing=False,
        convert_lighting_mode = "SPEC",
        export_format="GLB"
    )

    return FileResponse(
        outfile, 
        filename=outfile.name,
    )