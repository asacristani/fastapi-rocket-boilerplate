# trunk-ignore-all(terrascan/AC_DOCKER_0047)
FROM python:3.11

WORKDIR /app

# Crea un usuario no-root 'appuser' y cambia a este usuario
RUN useradd --create-home appuser
USER appuser

COPY . /app

# Instala dependencias con buenas prácticas
RUN pip install --no-cache-dir .

# Port
EXPOSE 8000

# Health Check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD [ "curl", "-f", "http://localhost:8000/check_health" ]

# CMD con notación JSON
CMD ["./entrypoint.sh"]
