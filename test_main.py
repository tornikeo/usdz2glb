import time
import pytest, tempfile, shutil
from pathlib import Path

res_p = Path(f'store/gen/{time.time_ns()//1000}')
res_p.mkdir(parents=True,exist_ok=True)

@pytest.mark.parametrize("file", [
    Path("store/sneaker_airforce.usdz"),
    Path("store/Fox/glTF"),
    Path("store/LibertyStatue"),
    Path("store/scene.gltf"),
    Path("store/LibertyStatue"),
    Path("store/LibertyStatue/LibertStatue.obj"),
])
def test_main(tmp_path: Path, file:Path):
    from fastapi.testclient import TestClient
    from main import app

    with TestClient(app) as client:
        if file.suffix == '':
            upload = Path(shutil.make_archive(tmp_path / 'pack', 'zip', file))
        else:
            upload = file
        assert upload.exists()
        resp = client.post("/convert", 
            files={"file": (upload.name, upload.open("rb"))})
        assert resp.status_code == 200
        res = res_p/f'{file.name.lower()}-down.glb'
        res.write_bytes(resp.content)
        print("FILE HERE >>>>>>>>>>>",res)

        
url = "https://storage.googleapis.com/tornikeo-portfolio-cdn/sneaker_airforce.usdz"

@pytest.mark.parametrize("url", [url])
def test_from_url(tmp_path: Path, url:str):
    from fastapi.testclient import TestClient
    from main import app

    with TestClient(app) as client:
        resp = client.post("/convert-from-url", 
            json={"url": url}
        )
        assert resp.status_code == 200
        res = res_p/f'{time.time_ns()}-down.glb'
        res.write_bytes(resp.content)
        print("FILE HERE >>>>>>>>>>>",res)
