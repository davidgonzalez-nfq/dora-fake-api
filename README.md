# fake-api (FastAPI)

API minimal para generar actividad de desarrollo y despliegues (para DORA con DevLake).

## Endpoints
- `GET /health`: estado simple.
- `POST /send-email`: simula envío de email (usa SMTP si está configurado).
- `GET /items`: lista items ficticios.

## Ejecutar localmente
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## Docker
```bash
docker build -t fake-api .
docker run -p 8080:8080 fake-api
```

## CI/CD
El workflow `deploy.yml` ejecuta tests y crea un **GitHub Deployment** sobre el entorno `production`. 
- Si el commit o el PR tiene la etiqueta `deploy-fail`, marca el deployment como `failure`.
- También se puede forzar fallo con el input `fail=true` del `workflow_dispatch`.

> Asegúrate de activar los permisos del workflow: `contents: write` y `deployments: write`.
