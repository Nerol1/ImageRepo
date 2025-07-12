import random
from pathlib import Path


import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os


from utils.file_utils import is_allowed_file, MAX_FILE_SIZE, get_unique_name


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static/", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    image_dir = Path("static/img/heroes/")
    file_names = []
    for file_name in os.listdir(image_dir):
        file_names.append(file_name)
    random_number = random.randrange(0, len(file_names))
    context["hero"] = file_names[random_number]


    return templates.TemplateResponse("index.html", context=context)


@app.get("/images/", response_class=HTMLResponse)
async def images(request: Request):
    context = {"request": request}
    image_dir = Path("static/img/uploads/")
    file_names = []
    for file_name in os.listdir(image_dir):
        file_names.append(file_name)
    context["images"] = file_names

    return templates.TemplateResponse("images.html", context=context)


@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("upload.html", context=context)


@app.post("/upload/")
async def upload_image(request: Request, file: UploadFile = File(...)):
    print(f"Файл {file.filename} получен")

    my_file = Path(file.filename)

    if is_allowed_file(my_file):
        print("Верное расширение файла")
    else:
        print("Не верное расширение файла")
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат. Разрешены только jpg, jpeg, png, gif")

    content = await file.read(MAX_FILE_SIZE + 1)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Файл слишком большой")

    new_file_name = get_unique_name(my_file)

    print(f"app.py {new_file_name}")

    image_dir = Path("static/img/uploads/")
    image_dir.mkdir(exist_ok=True)
    save_path = image_dir / new_file_name

    save_path.write_bytes(content)

    print(f"{save_path=}")

    context = {"request": request,
              "filename": file.filename,
              "new_filename": new_file_name,
               }
    return templates.TemplateResponse("upload.html", context=context)


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
