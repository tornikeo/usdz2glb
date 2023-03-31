import pytest, tempfile, shutil
from pathlib import Path


@pytest.mark.parametrize("file", [
    Path("store/sneaker_airforce.usdz"),
    Path("store/Fox/glTF"),
    Path("store/LibertyStatue"),
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
        res = (tmp_path / file.name /  'down.glb')
        res.parent.mkdir(exist_ok=True)
        res.write_bytes(resp.content)
        print("FILE HERE >>>>>>>>>>>",res)
        

        # print((tmp_path / 'down.glb'))

        
