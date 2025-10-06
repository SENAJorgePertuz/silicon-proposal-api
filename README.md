# 🚀 SiliconCP Proposal Generator (v1)

Automatiza la generación de propuestas comerciales personalizadas en formato **PPTX** para clientes de **Silicon Capital**, con soporte para los programas **EIC Accelerator** y **STEP Scale Up**.

> ✅ **v1**: Generación y descarga de PPTX  
> 📧 **v2 (próximamente)**: Envío por email + conversión a PDF  
> 🔐 **v4 (roadmap)**: Autenticación, marca blanca, firma electrónica

---

## 🧩 Características

- ✅ Formulario web para capturar datos del cliente
- ✅ Reemplazo dinámico de placeholders en plantilla PPTX
- ✅ Inclusión/exclusión de diapositivas mediante **tags en notas**
- ✅ Descarga directa del archivo generado (sin persistencia)
- ✅ Soporte para caracteres especiales (ñ, tildes, símbolos)
- ✅ Formato de tarifas: `6.000€`, `9%`
- ✅ Totalmente compatible con **IONOS + Render.com**

---

## 📂 Estructura del Proyecto

```Bash
    siliconcp-proposal-generator/
    ├── backend/
    │   ├── app/
    │   │   ├── __init__.py
    │   │   ├── main.py
    │   │   ├── ppt.py
    │   │   ├── models.py
    │   │   └── template.pptx
    |   ├── venv
    │   ├── requirements.txt
    │   └── Procfile
    └── frontend/
        ├── README.md
        └── index.html
```

---

## ⚙️ Requisitos

- Python 3.13.2
- PowerPoint o LibreOffice (para editar `template.pptx`)

---

## 🛠️ Desarrollo Local

### 1. Clonar y configurar entorno

```bash
    git clone silicon-proposal-api.git
    cd silicon-proposal-api

    # Crear y activar entorno virtual
    cd backend
    python -m venv venv
    venv\Scripts\Activate  # Windows
    source venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias

```bash
    pip install -r requirements.txt
```

> ⚠️ Asegúrate de que `requirements.txt` incluya:

```Bash
    fastapi==0.110.0
    uvicorn==0.27.1
    python-pptx==0.6.21
    python-multipart==0.0.9
    email-validator==2.2.0
```

### 3. Ejecutar backend

```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Ejecutar frontend

En una **nueva terminal**:

```bash
    cd frontend
    python -m http.server 3000
```

### 5. Probar

- Abre: http://localhost:3000
- Llena el formulario → descarga tu PPTX personalizado

---

## 🎨 Crear tu plantilla `template.pptx`

1. Edita `backend/app/template.pptx` con PowerPoint.
2. Usa **placeholders exactos**:
   - `{COMPANY_NAME}`, `{SETUP_FEE}`, `{SHORT_FEE}`, `{FULL_FEE}`, `{GRANT_FEE}`, `{EQUITY_FEE}`
   - *(Opcional)* `{CONTACT_NAME}`, `{CONTACT_EMAIL}`, `{DATE}`, `{PROGRAM}`
3. En las **notas de diapositivas**, añade tags para controlar visibilidad:
   
   ```bash
    [[tag:about_eic_accelerator]]
    [[tag:step_scaleup_pricing]]
    [[tag:annex_a]]  
   ```

> 💡 Ve a **Ver → Notas** en PowerPoint para editar las notas.

---

## 🌐 Despliegue en Producción

### Frontend (IONOS)
1. Sube `frontend/index.html` a `/apps_home/` vía SFTP.
2. Asegura SSL en `https://appsiliconcapital.com`.
3. Incluye enlace a: `https://proposal.appsiliconcapital.com`

### Backend (Render.com)
- **Build command**:

  ```Bash
    pip install -r backend/requirements.txt
  ```

- **Start command**:

  ```bash
    uvicorn backend.app.main:app --host 0.0.0.0 --port 10000
  ```

### DNS (IONOS)

- Crea un **CNAME**:
  - Nombre: `proposal`
  - Valor: `tu-app.onrender.com`
- Activa SSL para `proposal.appsiliconcapital.com`

---

## 📡 Contrato de API

**POST** `https://proposal.appsiliconcapital.com/render`

```json
{
  "company_name": "Acme Robotics",
  "contact_name": "Jane Doe",
  "contact_email": "jane@acme.com",
  "program": "EIC Accelerator",
  "proposal_date": "2025-09-29",
  "slide_toggles": {
    "about_eic_accelerator": true,
    "step_scaleup_pricing": true,
    "annex_a": false
  },
  "pricing_overrides": {
    "SETUP_FEE": 6000,
    "SHORT_FEE": 5000,
    "FULL_FEE": 2500,
    "GRANT_FEE": "9%",
    "EQUITY_FEE": "3%"
  }
}
```

**Respuesta**: Archivo `.pptx` descargable.

---

## 🔒 Seguridad

- **Sin persistencia**: los PPTX se generan en memoria y no se almacenan.
- **CORS restringido**: solo orígenes autorizados.
- **Validación de entrada**: Pydantic + `EmailStr`.
- **No se almacenan datos del cliente** tras la generación.

---

## 📈 Roadmap

| Versión | Características |
|--------|----------------|
| **v2** | Envío por email (SendGrid), conversión a PDF (LibreOffice), logs |
| **v3** | Múltiples plantillas, editor visual de tarifas |
| **v4** | Autenticación, marca blanca, firma electrónica |

---

## 📄 Licencia

Propiedad intelectual de **Silicon Capital**. Uso interno exclusivo.

---

> 💡 **Consejo**: Mantén `template.pptx` actualizado con los últimos términos legales y tarifas. Es el corazón del sistema.




¡Claro! Aquí tienes los comandos exactos para ejecutar tu proyecto **en desarrollo local**, paso a paso:

---

### 🖥️ **1. Ejecutar el BACKEND**

Abre una terminal (PowerShell, CMD o Bash) y ejecuta:

```powershell
# Navegar a la carpeta del backend
cd backend

# Activar el entorno virtual (Windows)
venv\Scripts\Activate.ps1

# Ejecutar el servidor FastAPI en modo desarrollo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ El backend estará disponible en:  
👉 **http://localhost:8000**  
👉 Documentación interactiva: **http://localhost:8000/docs**

> 💡 En Linux/Mac, activa el entorno con:  
> `source venv/bin/activate`

---

### 🌐 **2. Ejecutar el FRONTEND**

Abre **una segunda terminal** (deja el backend corriendo en la primera) y ejecuta:

```powershell
# Navegar a la carpeta del frontend
cd frontend

# Iniciar un servidor HTTP estático en el puerto 3000
python -m http.server 3000
```

✅ El frontend estará disponible en:  
👉 **http://localhost:3000**

> 💡 Asegúrate de tener Python instalado.  
> Alternativa: si usas la extensión **Live Server** en VS Code, abre `index.html` y haz clic en "Go Live" (se abrirá en `http://127.0.0.1:5500`).

---

### 🔗 **3. Probar la integración**

1. Abre el frontend: **http://localhost:3000**
2. Llena el formulario y haz clic en **"Generar y descargar propuesta"**
3. ¡Se descargará un archivo `.pptx` personalizado!

> ⚠️ **Importante**: el frontend está configurado para hablar con `http://localhost:8000/render` (ver `fetch` en `index.html`).  
> Para producción, recuerda cambiar esa URL a `https://proposal.appsiliconcapital.com/render`.

---

Con estos dos comandos, tienes todo listo para desarrollar y probar localmente. 🚀