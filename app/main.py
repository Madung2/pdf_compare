from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, FileResponse, JSONResponse
from pathlib import Path
from typing import Tuple
from .compare import make_output_pdf
import shutil
from tempfile import NamedTemporaryFile
import fitz  # PyMuPDF
import zipfile
from pathlib import Path
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()
app = FastAPI()
ADDRESS = os.getenv("ADDRESS")
dir_name = 'outputs'
output_dir = Path(dir_name)
output_dir.mkdir(exist_ok=True)
output_path1 = os.path.join(dir_name, "output1.pdf")
output_path2 = os.path.join(dir_name, "output2.pdf")

origins = [
    "http://localhost:3000",
    "http://localhost:5500",
    "http://localhost:8000",
    "https://yourdomain.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/api/compare_pdf")
async def compare_pdf(pdf1: UploadFile = File(...), pdf2: UploadFile = File(...)):

    with NamedTemporaryFile(delete=False) as tmp1:
        shutil.copyfileobj(pdf1.file, tmp1)
        tmp1_path = tmp1.name
    
    with NamedTemporaryFile(delete=False) as tmp2:
        shutil.copyfileobj(pdf2.file, tmp2)
        tmp2_path = tmp2.name

    doc1 = fitz.open(tmp1_path)
    doc2 = fitz.open(tmp2_path)

    output1, output2 = make_output_pdf(doc1, doc2 ,output_path1,output_path2 )

    if not output1 or not output2:
        return JSONResponse(status_code=500, content={"message": "Failed to process PDF files."})
    print(f"http://{ADDRESS}/{output_path1.replace(os.sep, '/')}")
    return JSONResponse(
        content={
            "url1": f"http://{ADDRESS}/app/{output_path1.replace(os.sep, '/')}",
            "url2": f"http://{ADDRESS}/app/{output_path2.replace(os.sep, '/')}"
        },
        status_code=200
    )


@app.get("/app/outputs/{filename}")
async def get_output_file(filename: str):
    file_path = Path("outputs") / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse(content={"detail": "Not found"}, status_code=404)


app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/static/index.html")