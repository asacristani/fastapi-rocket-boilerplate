# trunk-ignore-all(terrascan/AC_DOCKER_0047)
FROM python:3.11

WORKDIR /app

COPY . /app

# Install dependencies following best practices
RUN pip install --no-cache-dir .

# Port
EXPOSE 8000

# Health Check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD [ "curl", "-f", "http://localhost:8000/check_health" ]

# Create a non-root user 'appuser' and switch to this user
RUN useradd --create-home appuser
USER appuser

# CMD with JSON notation
CMD ["./entrypoint.sh"]
