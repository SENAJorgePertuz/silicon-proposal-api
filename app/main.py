# backend/app/main.py

"""
Módulo principal de la API del Generador de Propuestas (v1).

Este módulo expone un único endpoint POST `/render` que:
- Recibe datos de un cliente y configuración de tarifas.
- Carga una plantilla PPTX predefinida (`template.pptx`).
- Reemplaza placeholders con los valores proporcionados.
- Filtra diapositivas según tags en las notas (opcional).
- Devuelve el archivo PPTX generado como descarga directa.

Versión: v1
Autor: Ing Jorge Pertuz M
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import RenderRequest
from .ppt import generate_presentation
import os

# Inicialización de la aplicación FastAPI con metadatos
app = FastAPI(
    title="SiliconCP Proposal Generator API",
    version="1.0",
    description=(
        "API para generar propuestas comerciales personalizadas en formato PPTX. "
        "Soporta reemplazo de placeholders y filtrado de diapositivas mediante tags. "
        "v1: solo descarga de PPTX. v2+: email, PDF, autenticación."
    )
)

# Configuración de CORS
# Permite solicitudes desde:
# - Dominios de producción: appsiliconcapital.com y subdominio
# - Entornos de desarrollo local (Python server, Live Server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://appsiliconcapital.com",
        "https://proposal.appsiliconcapital.com",
        "https://silicon-proposal-frontend.netlify.app",  # Frontend en producción
        "http://localhost:5500",  # Live Server (VS Code)
        "http://127.0.0.1:5500",  # Live Server alternativa
        "http://localhost:3000",  # Dev local
        "http://127.0.0.1:3000",  # Dev local
    ],
    allow_credentials=True,
    allow_methods=["POST",  "OPTIONS"], # Incluye OPTIONS para preflight CORS
    allow_headers=["*"],
)

# Ruta absoluta a la plantilla PPTX
# La plantilla debe residir en el mismo directorio que este archivo.
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.pptx")

@app.post(
    "/render", 
    summary="Generar y descargar propuesta PPTX"
)
async def render_proposal(request: RenderRequest):
    """
    Endpoint principal para generar una propuesta personalizada.

    Flujo:
    1. Valida que la plantilla `template.pptx` exista.
    2. Prepara un diccionario de reemplazos para los placeholders.
    3. Llama a `generate_presentation()` para procesar la PPTX.
    4. Devuelve el archivo como stream binario con nombre dinámico.

    Parámetros:
        request (RenderRequest): Datos del cliente, programa, tarifas y toggles.

    Retorna:
        StreamingResponse: Archivo .pptx listo para descargar.

    Errores:
        500: Si la plantilla no se encuentra o falla la generación.
    """
    
    # Verificación temprana: asegurar que la plantilla existe
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(status_code=500, detail="Plantilla PPTX no encontrada")

    # Preparar el diccionario de reemplazos para los placeholders
    # Formato numérico: 6000 → "6.000€" (separador de miles con punto, símbolo € al final)
    overrides = request.pricing_overrides
    replacements = {
        "{COMPANY_NAME}": request.company_name,
        "{SETUP_FEE}": f"{overrides.SETUP_FEE:,.0f}€".replace(",", "."),
        "{SHORT_FEE}": f"{overrides.SHORT_FEE:,.0f}€".replace(",", "."),
        "{FULL_FEE}": f"{overrides.FULL_FEE:,.0f}€".replace(",", "."),
        "{GRANT_FEE}": overrides.GRANT_FEE,      # Ej: "9%"
        "{EQUITY_FEE}": overrides.EQUITY_FEE,    # Ej: "3%"
        
        # Placeholders extra (v1 opcional, útiles para notas o futuras versiones)
        "{CONTACT_NAME}": request.contact_name,
        "{CONTACT_EMAIL}": request.contact_email,
        "{DATE}": request.proposal_date.strftime("%d/%m/%Y"),  # Formato: 30/09/2025
        "{PROGRAM}": request.program,
    }

    # Generar la presentación en memoria (BytesIO)
    try:
        pptx_stream = generate_presentation(
            template_path=TEMPLATE_PATH,
            replacements=replacements,
            slide_toggles=request.slide_toggles # Dict[str, bool] para filtrar slides
        )
    except Exception as e:
        # Captura cualquier error durante la manipulación de la PPTX
        raise HTTPException(status_code=500, detail=f"Error al generar PPTX: {str(e)}")

    # Generar nombre de archivo seguro (solo alfanumérico, guiones y guiones bajos)
    safe_company = "".join(c if c.isalnum() or c in " _-" else "_" for c in request.company_name)
    filename = f"SiliconCP_Proposal_{safe_company}.pptx"

    # Devolver el archivo como descarga adjunta
    return StreamingResponse(
        pptx_stream,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
    
    


import io
import tempfile
import subprocess

@app.post(
    "/render/pdf", 
    summary="Generar y descargar propuesta en formato PDF"
)
async def render_proposal_pdf(request: RenderRequest):
    """
    Genera una propuesta PDF basada en la plantilla PPTX.

    Flujo:
    1. Usa la misma lógica de reemplazos que `/render`.
    2. Genera un archivo PPTX temporal.
    3. Usa LibreOffice en modo headless para convertirlo a PDF.
    4. Devuelve el PDF como descarga directa.

    Requiere:
        - LibreOffice instalado en el entorno (Render: via apt-get install libreoffice)
    """

    # 1️⃣ Validar que la plantilla existe
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(status_code=500, detail="Plantilla PPTX no encontrada")

    # 2️⃣ Preparar los reemplazos (idéntico a /render)
    overrides = request.pricing_overrides
    replacements = {
        "{COMPANY_NAME}": request.company_name,
        "{SETUP_FEE}": f"{overrides.SETUP_FEE:,.0f}€".replace(",", "."),
        "{SHORT_FEE}": f"{overrides.SHORT_FEE:,.0f}€".replace(",", "."),
        "{FULL_FEE}": f"{overrides.FULL_FEE:,.0f}€".replace(",", "."),
        "{GRANT_FEE}": overrides.GRANT_FEE,
        "{EQUITY_FEE}": overrides.EQUITY_FEE,
        "{CONTACT_NAME}": request.contact_name,
        "{CONTACT_EMAIL}": request.contact_email,
        "{DATE}": request.proposal_date.strftime("%d/%m/%Y"),
        "{PROGRAM}": request.program,
    }

    try:
        # 3️⃣ Generar la presentación en memoria
        pptx_stream = generate_presentation(
            template_path=TEMPLATE_PATH,
            replacements=replacements,
            slide_toggles=request.slide_toggles
        )

        # 4️⃣ Guardarla temporalmente para conversión
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_pptx:
            tmp_pptx.write(pptx_stream.getvalue())
            tmp_pptx.flush()
            pptx_path = tmp_pptx.name

        # 5️⃣ Definir ruta destino del PDF
        pdf_path = pptx_path.replace(".pptx", ".pdf")

        # 6️⃣ Ejecutar LibreOffice headless
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", os.path.dirname(pptx_path),
            pptx_path
        ], check=True)

        # 7️⃣ Leer PDF resultante
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        # 8️⃣ Limpiar archivos temporales
        os.remove(pptx_path)
        os.remove(pdf_path)

        # 9️⃣ Preparar nombre de archivo
        safe_company = "".join(c if c.isalnum() or c in " _-" else "_" for c in request.company_name)
        filename = f"SiliconCP_Proposal_{safe_company}.pdf"

        # 🔟 Retornar PDF
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error en conversión LibreOffice: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error general: {str(e)}")
    