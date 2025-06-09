<div align="right">

![Version](https://img.shields.io/badge/Version-0.0.1-blue?style=flat) 
![License](https://img.shields.io/badge/License-MIT-blue?style=flat) 
![Python](https://img.shields.io/badge/Language-Python-blue?style=flat) 

</div>

# Desafío LATAM Airlines
Este proyecto resuelve el desafío de ingeniería de datos enfocado en procesamiento eficiente de grandes volúmenes de tweets (~398MB), optimizando tanto memoria como tiempo de ejecución para el análisis de datos de Twitter.

**Repositorio GitHub:** [latam-data-challenge](https://github.com/landerox/latam-data-challenge)

### Descripción del Challenge

El desafío consiste en procesar un dataset de tweets para resolver tres problemas principales:

1. **Top 10 fechas con más tweets** y el usuario más activo por día
2. **Top 10 emojis más usados** con su conteo respectivo  
3. **Top 10 usuarios más influyentes** basado en menciones (@)

Cada problema debe implementarse con **dos enfoques**:
- **Optimización de tiempo**: Máxima velocidad de procesamiento
- **Optimización de memoria**: Uso mínimo de recursos de memoria

### Estructura del Repositorio

```
.
├── Dockerfile                      # Configuración para containerización
├── LICENSE                         # Licencia del proyecto
├── README.md                       # Documentación principal
├── exploration/                    # Scripts de exploración de datos
│   ├── explore_tweets_q1.py
│   ├── explore_tweets_q2.py
│   └── explore_tweets_q3.py
├── notebooks/                      # Análisis detallado en Jupyter
│   └── challenge_analysis.ipynb
├── poetry.lock                     # Lock file de Poetry
├── pyproject.toml                  # Configuración del proyecto
├── requirements.txt                # Dependencies para pip
├── src/                           # Código fuente principal
│   ├── config.json                # Configuración GCP y dataset
│   ├── main.py                    # CLI principal con argparse
│   ├── q1_memory.py               # Pregunta 1 - optimizado para memoria
│   ├── q1_time.py                 # Pregunta 1 - optimizado para tiempo
│   ├── q2_memory.py               # Pregunta 2 - optimizado para memoria
│   ├── q2_time.py                 # Pregunta 2 - optimizado para tiempo
│   ├── q3_memory.py               # Pregunta 3 - optimizado para memoria
│   ├── q3_time.py                 # Pregunta 3 - optimizado para tiempo
│   └── utils.py                   # Utilidades: GCS, BigQuery, config
└── terraform/                     # Infraestructura como Código
    ├── Makefile                   # Comandos de automatización
    ├── backend.tf                 # Configuración del backend
    ├── main.tf                    # Recursos principales
    ├── modules/                   # Módulos reutilizables
    │   ├── bigquery/             # Módulo BigQuery
    │   │   ├── dataset/          # Creación de dataset
    │   │   └── tables/           # Creación de tablas
    │   │       └── tables_schemas/  # Esquemas JSON
    │   │           ├── q1_results.json
    │   │           ├── q2_results.json
    │   │           └── q3_results.json
    │   ├── bucket/               # Módulo Cloud Storage
    │   └── serviceAccount/       # Módulo Service Account
    ├── outputs.tf                # Outputs de Terraform
    ├── variables.tf              # Variables de configuración
    ├── terraform.tfvars.example  # Ejemplo de configuración
    └── versions.tf               # Versiones de providers
```

### Flujo de Trabajo Completo

### 1. Setup Inicial (Una sola vez)
```bash
# Clonar repositorio
git clone https://github.com/landerox/latam-data-challenge
cd latam-data-challenge

# Configurar infraestructura
cd terraform
make set-project PROJECT_ID=tu-project-id
make enable-apis
make create-sa
make add-sa-roles
make create-sa-key
make create-tf-bucket

# Configurar variables
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars

# Aplicar infraestructura
make init
make apply
```

### 2. Configuración CI/CD (Una sola vez)
```bash
# En GitHub Repository Settings:
# 1. Agregar Secrets: SA_TERRAFORM_KEY, SA_DEPLOYMENT_KEY
# 2. Agregar Variables: PROJECT_ID, REGION, etc.
# 3. Push a main/develop activa el pipeline automático
```

### 3. Ejecución de Análisis
```bash
# Automático via CI/CD (push a main/develop)
git push origin main

# Manual via Cloud Run Job
gcloud run jobs execute latam-data-challenge-job \
  --project=latam-data-challenge \
  --region=us-east1 \
  --args="src/main.py,--question,q1,--method,time,--save_bq" \
  --wait

# Local para desarrollo
poetry run python src/main.py --question all --method memory
```

### Configuración de Infraestructura (IaC)

#### Setup Inicial

1. **Configuración de Terraform:**
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edita terraform.tfvars con tus configuraciones
   ```

### Setup Inicial con Makefile

1. **Configuración de proyecto:**
   ```bash
   cd terraform
   make set-project PROJECT_ID=tu-project-id
   make enable-apis
   ```

2. **Creación de Service Account:**
   ```bash
   make create-sa
   make add-sa-roles
   make create-sa-key  # ⚠️ NO commitear este archivo
   ```

3. **Bucket de Terraform:**
   ```bash
   make create-tf-bucket
   ```

4. **Configuración de variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edita terraform.tfvars con tus valores
   ```

#### Recursos Creados

La infraestructura automatizada crea:

- **Bucket de Terraform State:** `gs://latam-data-challenge-terraform-state`
- **Bucket de datos:** `gs://latam-data-challenge-data`
- **Dataset BigQuery:** `challenge_data` con 3 tablas:
  - `q1_results`: Fechas con más tweets y usuario más activo
  - `q2_results`: Ranking de emojis más usados
  - `q3_results`: Usuarios más mencionados
- **Cuenta de servicio:** `sa-deployment` con roles:
  - BigQuery Data Editor
  - Storage Object Admin
  - Cloud Run Developer

#### Esquemas de BigQuery

**Tabla q1_results:**
```json
{
  "tweet_date": "DATE",
  "top_user": "STRING", 
  "method": "STRING",
  "ingested_at": "TIMESTAMP"
}
```

**Tabla q2_results:**
```json
{
  "emoji": "STRING",
  "count": "INTEGER",
  "method": "STRING", 
  "ingested_at": "TIMESTAMP"
}
```

**Tabla q3_results:**
```json
{
  "username": "STRING",
  "mention_count": "INTEGER",
  "method": "STRING",
  "ingested_at": "TIMESTAMP"
}
```

#### CI/CD Automático

El pipeline ejecuta automáticamente en cada push a `main` o `develop`:

**Job 1: Terraform Workflow**
- `terraform plan` - Planificación de cambios
- `terraform apply` - Aplicación de infraestructura (solo main/develop)

**Job 2: Build & Deploy**
- Build de imagen Docker
- Push a Artifact Registry
- Deploy como Cloud Run Job
- Ejecución automática del análisis

### Variables de Entorno Requeridas

**GitHub Repository Variables:**
```bash
PROJECT_ID=latam-data-challenge
REGION=us-east1
ZONE=us-east1-b
ARTIFACT_REPO=latam-data-challenge-repo
IMAGE_NAME=latam-data-challenge
CLOUD_RUN_JOB_NAME=latam-data-challenge-job
ENVIRONMENT=dev
REPOSITORY_ID=latam-data-challenge
```

**GitHub Repository Secrets:**
```bash
SA_TERRAFORM_KEY      # Service Account key para Terraform
SA_DEPLOYMENT_KEY     # Service Account key para deployment
```

### Despliegue en Cloud Run Job

El proyecto se despliega automáticamente como un **Cloud Run Job** mediante GitHub Actions. Una vez desplegado, el job puede ser ejecutado manualmente con diferentes parámetros.

#### Configuración del Cloud Run Job

```yaml
# Configuración automática via CI/CD
Resource: 2 CPU, 4Gi memoria
Timeout: 3600s (1 hora)
Service Account: sa-deployment@latam-data-challenge.iam.gserviceaccount.com
Execution Environment: gen2
Max Retries: 1
```

#### Ejecución Manual desde Cloud Shell

Una vez desplegado, puedes ejecutar el job con diferentes configuraciones:

```bash
# Análisis completo (todas las preguntas, método tiempo)
gcloud run jobs execute latam-data-challenge-job \
  --project=latam-data-challenge \
  --region=us-east1 \
  --wait

# Solo pregunta 1 optimizada para memoria
gcloud run jobs execute latam-data-challenge-job \
  --project=latam-data-challenge \
  --region=us-east1 \
  --overrides='
  {
    "spec": {
      "template": {
        "spec": {
          "template": {
            "spec": {
              "containers": [
                {
                  "args": ["src/main.py", "--question", "q1", "--method", "memory", "--save_bq"]
                }
              ]
            }
          }
        }
      }
    }
  }' \
  --wait

# Top 5 emojis con método tiempo
gcloud run jobs execute latam-data-challenge-job \
  --project=latam-data-challenge \
  --region=us-east1 \
  --overrides='
  {
    "spec": {
      "template": {
        "spec": {
          "template": {
            "spec": {
              "containers": [
                {
                  "args": ["src/main.py", "--question", "q2", "--method", "time", "--top_n", "5", "--save_bq"]
                }
              ]
            }
          }
        }
      }
    }
  }' \
  --wait
```

#### Comandos Simplificados

Para facilitar la ejecución, puedes usar estos comandos más simples:

```bash
# Variables de entorno
export PROJECT_ID="latam-data-challenge"
export REGION="us-east1"
export JOB_NAME="latam-data-challenge-job"

# Ejecutar análisis específico
gcloud run jobs execute $JOB_NAME \
  --project=$PROJECT_ID \
  --region=$REGION \
  --args="src/main.py,--question,q3,--method,memory,--top_n,15,--save_bq" \
  --wait
```

### Configuración Local para Desarrollo

#### Ejecución Local

```bash
# Instalar dependencias
poetry install

# Configurar variable de entorno para testing local
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"

# Ejecutar localmente
poetry run python src/main.py --question q1 --method time --top_n 5

# Con archivo local (sin Cloud Storage)
poetry run python src/main.py --question all --method memory --top_n 10
```

#### Docker Local

```bash
# Build imagen localmente
docker build -t latam-data-challenge .

# Ejecutar contenedor
docker run --rm \
  -v /path/to/service-account.json:/app/sa.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/sa.json \
  latam-data-challenge \
  python src/main.py --question q2 --method time --save_bq
```

#### Ejemplos de Uso

```bash
# Ejecutar pregunta 1 optimizada para tiempo
poetry run python src/main.py --question q1 --method time

# Ejecutar todas las preguntas optimizadas para memoria y guardar en BigQuery
poetry run python src/main.py --question all --method memory --save_bq

# Ejecutar pregunta 2 con top 5 resultados
poetry run python src/main.py --question q2 --method time --top_n 5

# Análisis completo: todas las preguntas con ambos métodos
poetry run python src/main.py --question all --method time --save_bq
poetry run python src/main.py --question all --method memory --save_bq
```

#### Estructura de Salida

**Q1 - Top fechas con más tweets:**
```python
[(datetime.date(2021, 2, 12), "narendramodi"), 
 (datetime.date(2021, 2, 13), "SatyagrahF"), ...]
```

**Q2 - Top emojis más usados:**
```python  
[("🙏", 5049), ("😂", 3072), ("🔥", 2972), ...]
```

**Q3 - Usuarios más mencionados:**
```python
[("narendramodi", 2265), ("Kisanektamorcha", 1840), ...]
```

### Estrategias de Optimización

#### Time Optimization
- **Pandas DataFrame**: Carga completa del dataset en memoria para operaciones vectorizadas
- **Agregaciones eficientes**: Uso de `groupby()` y `value_counts()` de pandas
- **Procesamiento por lotes**: Manejo de todo el dataset de una vez
- **Indexación automática**: Aprovecha los índices internos de pandas para búsquedas rápidas

#### Memory Optimization  
- **Streaming line-by-line**: Procesamiento secuencial del archivo JSON Lines
- **Collections.Counter**: Estructura de datos eficiente para conteos incrementales
- **Liberación inmediata**: Variables se procesan y liberan línea por línea
- **Sin carga completa**: El dataset nunca se carga completamente en memoria

#### Implementaciones Específicas

**Q1 - Top fechas y usuarios más activos:**
- **Time**: Pandas groupby con agregaciones múltiples por fecha y usuario
- **Memory**: Dict anidado `{date: {username: count}}` con procesamiento línea por línea

**Q2 - Top emojis más usados:**
- **Time**: Pandas Series con `str.findall()` y `explode()` para extraer emojis
- **Memory**: Regex pattern con Counter incremental por cada tweet

**Q3 - Usuarios más mencionados:**
- **Time**: Lista plana de menciones con pandas `value_counts()`
- **Memory**: Counter directo sobre el campo `mentionedUsers` de cada tweet

### Buenas Prácticas Aplicadas

- ✅ **Arquitectura modular**: Separación clara entre optimizaciones de tiempo y memoria
- ✅ **Manejo robusto de errores**: Validación de JSON y campos requeridos
- ✅ **Configuración centralizada**: `config.json` para parámetros de infraestructura
- ✅ **Documentación completa**: Docstrings detallados en todas las funciones
- ✅ **GitFlow workflow**: Ramas de desarrollo separadas del main
- ✅ **Infrastructure as Code**: Terraform con módulos reutilizables
- ✅ **CI/CD automatizado**: GitHub Actions para deploy continuo
- ✅ **Logging estructurado**: Seguimiento detallado de ejecución
- ✅ **Timezone awareness**: Manejo correcto de husos horarios
- ✅ **Escalabilidad**: Diseño preparado para datasets más grandes
- ✅ **Testing de integración**: Validación con datos reales
- ✅ **Cleanup automático**: Eliminación de datos previos por partición

### Supuestos del Proyecto

- **Formato de datos**: JSON Lines con estructura de Twitter API v1
- **Campos requeridos**: 
  - `date`: Timestamp ISO 8601 del tweet
  - `user.username`: Usuario autor del tweet
  - `content`: Contenido textual para análisis de emojis
  - `mentionedUsers`: Array de usuarios mencionados
- **Encoding**: UTF-8 para caracteres especiales y emojis
- **Timezone**: America/Santiago para timestamps de ingestión
- **Manejo de errores**: Líneas malformadas se omiten silenciosamente
- **Permisos GCP**: Service Account con acceso a Storage y BigQuery
- **Recursos disponibles**: Suficiente memoria/CPU para dataset de ~398MB

### Librerías Clave

```python
# Procesamiento de datos
pandas>=1.5.0              # Análisis de datos y agregaciones
numpy>=1.21.0              # Operaciones numéricas

# Google Cloud Platform
google-cloud-storage>=2.7.0   # Descarga desde Cloud Storage
google-cloud-bigquery>=3.4.0  # Inserción de resultados

# Análisis y profiling
memory-profiler>=0.60.0    # Análisis de memoria (opcional)

# Utilidades del sistema
pathlib                    # Manejo de rutas (stdlib)
tempfile                   # Archivos temporales (stdlib)
collections.Counter        # Conteos eficientes (stdlib)
json                       # Parsing JSON Lines (stdlib)
re                         # Regex para emojis (stdlib)
datetime                   # Manejo de fechas (stdlib)
zoneinfo                   # Timezone Santiago (stdlib)
```

#### Configuración del Proyecto

El archivo `src/config.json` contiene:
```json
{
  "BUCKET": "latam-data-challenge-data",
  "DATASET_ID": "challenge_data", 
  "FILENAME": "farmers-protest-tweets-2021-2-4.json",
  "PROJECT_ID": "latam-data-challenge"
}
```

### Monitoreo y Logs

#### Cloud Logging

Todos los logs se almacenan en Cloud Logging con etiquetas:
```bash
# Ver logs del Cloud Run Job
gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=latam-data-challenge-job" \
  --project=latam-data-challenge \
  --format="table(timestamp,severity,textPayload)" \
  --limit=50

# Filtrar por severidad
gcloud logging read "resource.type=cloud_run_job AND severity>=WARNING" \
  --project=latam-data-challenge
```

#### Métricas Disponibles

- **Tiempo de ejecución** por método (time vs memory)
- **Uso de memoria** durante procesamiento
- **Resultados por pregunta** guardados en BigQuery
- **Logs estructurados** con timestamps y contexto

#### Consultas BigQuery

```sql
-- Comparar rendimiento entre métodos
SELECT 
  method,
  COUNT(*) as total_results,
  MAX(ingested_at) as last_execution
FROM `latam-data-challenge.challenge_data.q1_results`
GROUP BY method;

-- Ver evolución temporal de resultados
SELECT 
  DATE(ingested_at) as execution_date,
  method,
  COUNT(*) as records_processed
FROM `latam-data-challenge.challenge_data.q2_results`
GROUP BY execution_date, method
ORDER BY execution_date DESC;
```

### Contribución

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -am 'Agrega nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

### Contacto

**Autor:** Fernando Landero  
**Email:** landerox@gmail.com  
**GitHub:** [@landerox](https://github.com/landerox)

---
