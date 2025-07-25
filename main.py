from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from docxtpl import DocxTemplate
import zipfile, os, shutil

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h2>Введите имя</h2>
    <form action="/generate" method="post">
        <input type="text" name="name" placeholder="Бауыржан, Арман, Ержан">
        <button type="submit">Создать кувертки</button>
    </form>
    """

@app.post("/generate")
def generate(name: str = Form(...)):
    names = [n.strip() for n in name.split(",") if n.strip()]
    output_files = []

    os.makedirs("output", exist_ok=True)

    for n in names:
        doc = DocxTemplate("template.docx")
        doc.render({"name": n})
        filename = f"output/{n}_кувертка.docx"
        doc.save(filename)
        output_files.append(filename)

    if len(output_files) == 1:
        return FileResponse(output_files[0], filename=os.path.basename(output_files[0]))
    else:
        zip_path = "output/кувертки.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for f in output_files:
                zipf.write(f, arcname=os.path.basename(f))
        return FileResponse(zip_path, filename="кувертки.zip")
