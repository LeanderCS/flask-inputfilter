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
docker exec -it flask-inputfilter black .
```
