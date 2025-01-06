# Development

### Build docker image
```bash
docker build -t jtrfaker .
```

### Run docker container in interactive mode
```bash
docker compose up -d
```

```bash
docker exec -it jtrfaker bash
```

### Run tests
```bash
docker exec -it jtrfaker pytest
```

### Run linting
```bash
docker exec -it jtrfaker flake8
```
