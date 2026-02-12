import subprocess
from pathlib import Path
import tempfile
import os
import platform
import shutil


def get_soffice_path():
    """
    Detecta automáticamente la ruta de LibreOffice
    Windows → ruta típica
    Linux/EC2 → usa 'soffice' del sistema
    Permite override con variable de entorno SOFFICE_PATH
    """

    # 1️⃣ prioridad: variable de entorno (producción ideal)
    env_path = os.getenv("SOFFICE_PATH")
    if env_path:
        return env_path

    sistema = platform.system()

    # 2️⃣ Windows
    if sistema == "Windows":
        default = r"C:\Program Files\LibreOffice\program\soffice.exe"
        if Path(default).exists():
            return default

    # 3️⃣ Linux / EC2
    soffice = shutil.which("soffice")
    if soffice:
        return soffice

    raise FileNotFoundError(
        "LibreOffice (soffice) no encontrado. Instálalo o define SOFFICE_PATH."
    )


SOFFICE_PATH = get_soffice_path()


def convertir_a_pdf(ruta_archivo):
    ruta_archivo = Path(ruta_archivo)
    salida_dir = ruta_archivo.parent

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
        raise Exception("Error convirtiendo a PDF con LibreOffice")

    return ruta_archivo.with_suffix(".pdf")