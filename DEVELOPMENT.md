# Development

### Build docker image
```bash
docker build -t flask-inputfilter .
```

### Run docker container in interactive mode
```bash
docker compose up -d
```

```bash
docker exec -it flask-inputfilter /bin/bash
```

### Run tests
```bash
docker exec -it flask-inputfilter pytest
```

### Run linting
```bash
docker exec -it flask-inputfilter sh -c "isort ."
docker exec -it flask-inputfilter sh -c "autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports --recursive ."
docker exec -it flask-inputfilter black .
```
