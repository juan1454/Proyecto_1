import subprocess
from pathlib import Path
import tempfile
import os


SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"


def convertir_a_pdf(ruta_archivo):
    ruta_archivo = Path(ruta_archivo)
    salida_dir = ruta_archivo.parent

    # 🔥 perfil temporal (evita bloqueo de LibreOffice)
    perfil_temp = tempfile.mkdtemp()

    cmd = [
        SOFFICE_PATH,
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        f"-env:UserInstallation=file:///{perfil_temp.replace(os.sep, '/')}",
        "--convert-to",
        "pdf",
        str(ruta_archivo),
        "--outdir",
        str(salida_dir),
    ]

    resultado = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        print("STDOUT:", resultado.stdout)
        print("STDERR:", resultado.stderr)
        raise Exception("Error convirtiendo a PDF")

    return ruta_archivo.with_suffix(".pdf")