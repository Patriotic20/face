FROM python:3.12-slim
WORKDIR /face

# Install uv
RUN pip install uv

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies system-wide (no venv needed in container)
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the application
COPY . .

# Copy and configure entrypoint script
COPY execute.sh .
RUN chmod +x execute.sh

COPY run_migration.sh .
RUN chmod +x run_migration.sh

ENTRYPOINT ["/bin/sh", "/face/run_migration.sh"]
CMD ["/face/execute.sh"]