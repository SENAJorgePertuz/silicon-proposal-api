# backend/app/models.py
"""
Modelos Pydantic para la validación de la solicitud entrante en /render.

Define la estructura esperada del JSON enviado por el frontend.
Usado por FastAPI para validar y parsear automáticamente el cuerpo de la petición.
"""

from pydantic import BaseModel, EmailStr
from typing import Dict, Optional
from datetime import date

class PricingOverrides(BaseModel):
    """
    Tarifas personalizadas proporcionadas por el usuario.
    
    Los valores numéricos (SETUP_FEE, etc.) se envían como enteros (€),
    mientras que los porcentajes se envían como cadenas con símbolo '%' (ej. "9%").
    """
    SETUP_FEE: int      # Tarifa de configuración en euros (ej. 6000)
    SHORT_FEE: int      # Tarifa de éxito para aplicación corta en euros (ej. 5000)
    FULL_FEE: int       # Tarifa de éxito para aplicación completa en euros (ej. 2500)
    GRANT_FEE: str      # Porcentaje de éxito en subvención (ej. "9%")
    EQUITY_FEE: str     # Porcentaje de éxito en equity (ej. "3%")

class RenderRequest(BaseModel):
    """
    Solicitud completa para generar una propuesta.
    
    Corresponde al cuerpo del POST /render.
    Todos los campos son obligatorios.
    """
    company_name: str                    # Nombre de la empresa cliente
    contact_name: str                    # Nombre de la persona de contacto
    contact_email: EmailStr              # Email válido (validado por Pydantic + email-validator)
    program: str                         # Programa: "EIC Accelerator" o "STEP Scale Up"
    proposal_date: date                  # Fecha en formato ISO: "YYYY-MM-DD"
    slide_toggles: Dict[str, bool]       # Controles para incluir/excluir diapositivas por tag
    pricing_overrides: PricingOverrides  # Bloque de tarifas (ver arriba)