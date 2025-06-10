<div align="right">

![Version](https://img.shields.io/badge/Version-0.0.1-blue?style=flat) 
![License](https://img.shields.io/badge/License-MIT-blue?style=flat) 
![Python](https://img.shields.io/badge/Language-Python-blue?style=flat) 

</div>

# Análisis de Tweets - Desafío Ingeniería de Datos LATAM Airlines

Solución al desafío de procesamiento eficiente de ~398MB de datos de Twitter (farmers-protest-tweets-2021-2-4.json), implementando optimizaciones de memoria y tiempo con Python y Google Cloud Platform.

## 📋 Resumen del Desafío

El dataset contiene tweets relacionados con las protestas de agricultores en India (2021), con más de 400K registros. El desafío consiste en procesar eficientemente este volumen de datos para extraer insights clave, priorizando ya sea velocidad de ejecución o uso mínimo de memoria RAM.

## 🎯 Descripción del Proyecto

El proyecto resuelve tres problemas de análisis de datos (questions/preguntas):

1. **Q1**: Top 10 fechas con más tweets, identificando el usuario más activo por día
2. **Q2**: Top 10 emojis más utilizados con sus conteos
3. **Q3**: Top 10 usuarios más mencionados en tweets

Cada problema (`qX_*.py` donde X es el número de pregunta) tiene dos implementaciones:
- **time**: Optimizada para tiempo de ejecución usando pandas
- **memory**: Optimizada para consumo de memoria procesamiento línea a línea.

**Contexto del Dataset:** El archivo JSON contiene ~400K tweets relacionados con las protestas de agricultores en India durante 2021, recopilados de Twitter.

## ⚙️ Arquitectura

El proyecto incluye:
- Procesamiento de datos con Python y Pandas
- Infraestructura en GCP (Storage, BigQuery, Cloud Run)
- CI/CD automatizado con GitHub Actions  
- Infraestructura como código con Terraform
- Análisis de rendimiento con memory-profiler
- Pre-commit hooks (Ruff para linting/formato, Bandit para seguridad)

## 📁 Estructura del Proyecto

```
.
├── Dockerfile                      # Dockerización del proyecto
├── LICENSE                         # Licencia del proyecto
├── README.md                       # Documentación principal
├── exploration/                    # Scripts para exploración inicial de datos
│   ├── explore_tweets_q1.py
│   ├── explore_tweets_q2.py
│   └── explore_tweets_q3.py
├── notebooks/                      # Cuaderno Jupyter con análisis detallado
│   └── challenge_analysis.ipynb
├── poetry.lock                     # Archivo lock generado por Poetry
├── pyproject.toml                  # Configuración del proyecto con Poetry
├── requirements.txt                # Dependencias del proyecto para pip
├── src/                            # Código fuente
│   ├── config.json                 # Configuración GCP y dataset
│   ├── main.py                     # CLI principal con argparse
│   ├── q1_memory.py                # Problema 1 optimizado para memoria
│   ├── q1_time.py                  # Problema 1 optimizado para tiempo
│   ├── q2_memory.py                # Problema 2 optimizado para memoria
│   ├── q2_time.py                  # Problema 2 optimizado para tiempo
│   ├── q3_memory.py                # Problema 3 optimizado para memoria
│   ├── q3_time.py                  # Problema 3 optimizado para tiempo
│   └── utils.py                    # Utilidades comunes (GCS, BigQuery, configuración)
└── terraform/                      # Infraestructura como Código (IaC)
    ├── Makefile                    # Automatización de tareas
    ├── backend.tf                  # Configuración del backend de Terraform
    ├── main.tf                     # Recursos principales en Terraform
    ├── modules/                    # Módulos reutilizables
    │   ├── bigquery/               # Configuración de BigQuery
    │   │   ├── dataset/            # Creación de dataset
    │   │   └── tables/             # Creación de tablas
    │   │       └── tables_schemas/ # Esquemas JSON para tablas
    │   │           ├── q1_results.json
    │   │           ├── q2_results.json
    │   │           └── q3_results.json
    │   ├── bucket/                 # Configuración de Cloud Storage
    │   └── serviceAccount/         # Configuración de cuenta de servicio
    ├── outputs.tf                  # Outputs definidos en Terraform
    ├── variables.tf                # Variables configurables en Terraform
    ├── terraform.tfvars.example    # Ejemplo de archivo de variables
    └── versions.tf                 # Versionado de providers
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Cuenta de Google Cloud Platform con permisos de administrador
- Terraform >= 1.0
- Google Cloud SDK (gcloud)
- Python 3.12+ con Poetry
- Docker (opcional)

### Setup de Infraestructura

#### 1. Configuración inicial del proyecto GCP:

Navega a la carpeta  `terraform/`, edita las variables del archivo Makefile según tu configuración:
```bash
# Variables de Makefile
PROJECT_ID      ?= <PROJECT_ID>
REGION          ?= <REGION>
TF_BUCKET_NAME  ?= $(PROJECT_ID)-terraform-state
SA_NAME         ?= sa-terraform
SA_EMAIL        = $(SA_NAME)@$(PROJECT_ID).iam.gserviceaccount.com
SA_KEY_FILE     ?= sa/sa-terraform.json
```
 y luego ejecuta los siguientes comandos:
```
# Configurar proyecto
make set-project PROJECT_ID=<YOUR_PROJECT_ID>

# Autenticarse en GCP
make auth-login

# Habilitar APIs necesarias
make enable-apis

# Crear cuenta de servicio para Terraform
make create-sa

# Asignar roles necesarios
make add-sa-roles

# Generar clave de cuenta de servicio (NO commitear)
make create-sa-key

# Crear bucket para estado de Terraform
make create-tf-bucket
```

#### 2. Configurar variables de Terraform:

```bash
# Copiar archivo de ejemplo
cp terraform.tfvars.example terraform.tfvars

# Editar terraform.tfvars con tus valores:
project_id        = "<YOUR_PROJECT_ID>"
repository_id     = "<YOUR_REPOSITORY_ID>"
environment       = "<dev|staging|prod>"
region            = "<YOUR_REGION>"
zone              = "<YOUR_ZONE>"
credentials_file  = "sa/sa-terraform.json"
```

#### 3. Desplegar infraestructura con Terraform:

```bash
# Inicializar Terraform
terraform init

# Revisar plan de ejecución
terraform plan

# Aplicar cambios
terraform apply
```

### Configuración CI/CD

En GitHub Repository Settings agregar:

**Secrets:**
- `SA_TERRAFORM_KEY`: JSON de cuenta de servicio Terraform
- `SA_DEPLOYMENT_KEY`: JSON de cuenta de servicio deployment

**Variables:**
- `PROJECT_ID`: `<YOUR_PROJECT_ID>`
- `REGION`: `<YOUR_REGION>`
- `ZONE`: `<YOUR_ZONE>`
- `ARTIFACT_REPO`: `<YOUR_ARTIFACT_REPO_NAME>`
- `IMAGE_NAME`: `<YOUR_IMAGE_NAME>`
- `CLOUD_RUN_JOB_NAME`: `<YOUR_JOB_NAME>`
- `ENVIRONMENT`: `<dev|staging|prod>`
- `REPOSITORY_ID`: `<YOUR_REPOSITORY_ID>`

## 💻 Uso del Sistema

### Ejecución Local

```bash
poetry install
export GOOGLE_APPLICATION_CREDENTIALS="<PATH_TO_SERVICE_ACCOUNT_KEY>.json"

# Ejecutar análisis específico
poetry run python src/main.py --question q1 --method time

# Ejecutar todo y guardar en BigQuery
poetry run python src/main.py --question all --method memory --save_bq

# Personalizar top N resultados
poetry run python src/main.py --question q2 --method time --top_n 5
```

### Ejecución en Cloud Run

```bash
# Ejecutar job con configuración por defecto
gcloud run jobs execute <YOUR_CLOUD_RUN_JOB_NAME> \
  --project=<YOUR_PROJECT_ID> \
  --region=<YOUR_REGION> \
  --wait

# Ejecutar análisis específico
gcloud run jobs execute <YOUR_CLOUD_RUN_JOB_NAME> \
  --project=<YOUR_PROJECT_ID> \
  --region=<YOUR_REGION> \
  --args="src/main.py,--question,q1,--method,memory,--save_bq" \
  --wait
```

### Docker Local

```bash
docker build -t <YOUR_IMAGE_NAME> .
docker run --rm \
  -v <PATH_TO_SERVICE_ACCOUNT_KEY>.json:/app/sa.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/sa.json \
  <YOUR_IMAGE_NAME> \
  python src/main.py --question all --method time
```

## 📊 Parámetros CLI (Interfaz de línea de comandos)

| Parámetro | Valores posibles | Default | Descripción |
|-----------|------------------|---------|-------------|
| `--question` | q1, q2, q3, all | all | Qué análisis ejecutar |
| `--method` | time, memory | time | Optimización por tiempo o memoria |
| `--top_n` | entero positivo | 10 | Número de resultados a retornar |
| `--save_bq` | (flag) | false | Guardar resultados en BigQuery |

## 📈 Rendimiento y Resultados

Basado en el análisis del notebook con 398MB de tweets:

### Q1 - Top fechas con más tweets
- **Método time**: ~5 segundos, ~207 MiB RAM
- **Método memory**: ~4.5 segundos, ~205 MiB RAM
- **Conclusión**: Rendimiento similar, ambos métodos son eficientes

### Q2 - Top emojis más usados  
- **Método time**: ~5.65 segundos, ~211 MiB RAM
- **Método memory**: ~70 segundos, ~210 MiB RAM
- **Conclusión**: El método optimizado para tiempo es ~12x más rápido sin penalizar el uso de memoria

### Q3 - Usuarios más mencionados
- **Método time**: ~5.49 segundos, ~210 MiB RAM
- **Método memory**: ~4.58 segundos, ~210 MiB RAM
- **Conclusión**: Rendimiento prácticamente idéntico

### Formato de Resultados

**Q1**: Lista de tuplas (fecha, usuario)
```python
[(datetime.date(2021, 2, 12), "narendramodi"), ...]
```

**Q2**: Lista de tuplas (emoji, conteo)
```python
[("🙏", 5049), ("😂", 3072), ...]
```

**Q3**: Lista de tuplas (usuario, menciones)
```python
[("narendramodi", 2265), ...]
```

## ☁️ Recursos GCP Creados

**Buckets:**
- `<YOUR_PROJECT_ID>-terraform-state`: Estado de Terraform
- `<YOUR_DATA_BUCKET_NAME>`: Almacenamiento de datos

**BigQuery:**
- Dataset: `<YOUR_BIGQUERY_DATASET>`
- Tablas: `q1_results`, `q2_results`, `q3_results`

**Service Accounts:**
- `sa-terraform`: Gestión de infraestructura
- `sa-deployment`: Ejecución de aplicación

**Cloud Run:**
- Job con 2 CPU, 4Gi memoria
- Timeout: 1 hora
- Environment: gen2

## 🔄 Pipeline CI/CD

El pipeline se activa con push a main o develop:

1. **Terraform**: Planifica y aplica cambios de infraestructura
2. **Docker**: Construye imagen y la sube a Artifact Registry
3. **Deploy**: Actualiza Cloud Run Job
4. **Ejecuta**: Corre análisis automáticamente

## 🧹 Limpieza

Para eliminar archivos sensibles locales:
```bash
cd terraform && make clean
```

Para destruir infraestructura:
```bash
cd terraform && terraform destroy
```

## ⚙️ Archivos de Configuración

**config.json** - Configuración del proyecto:
```json
{
  "BUCKET": "<YOUR_DATA_BUCKET_NAME>",
  "DATASET_ID": "<YOUR_BIGQUERY_DATASET>", 
  "FILENAME": "farmers-protest-tweets-2021-2-4.json",
  "PROJECT_ID": "<YOUR_PROJECT_ID>"
}
```

**pyproject.toml** - Dependencias principales:
- `pandas`: Procesamiento de datos
- `google-cloud-bigquery`: Integración con BigQuery
- `google-cloud-storage`: Manejo de archivos en GCS
- `memory-profiler`: Análisis de consumo de memoria

## 📓 Notebooks y Análisis

`notebooks/challenge_analysis.ipynb` contiene:
- Exploración inicial del dataset
- Comparación detallada entre métodos time y memory
- Análisis de rendimiento con memory-profiler
- Visualización de resultados
- Conclusiones y recomendaciones

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---
