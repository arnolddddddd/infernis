# Contributing to INFERNIS

Thanks for your interest in contributing to INFERNIS! This project predicts wildfire risk across British Columbia using machine learning and open data.

## Architecture

INFERNIS is an **open-core** project:

- **This repo (public)** — The engine: data pipelines, ML models, FWI computation, REST API, training scripts, tests, deployment config
- **Private repo** — Landing page, dashboard, Firebase auth, model weights, raw data

Your contributions to this public repo power the live API at [infernis.ca](https://infernis.ca). Changes merged here get pulled into the production deployment.

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 16 with PostGIS 3.4
- Redis 7
- GDAL/GEOS/PROJ system libraries

### Setup

```bash
# Clone and enter the repo
git clone https://github.com/argonBIsystems/infernis.git
cd infernis

# Run the dev setup script (creates venv, installs deps, copies .env)
./scripts/dev_setup.sh

# Start databases
make db-up

# Run migrations
make migrate

# Run tests to verify everything works
make test
```

### Environment

Copy `.env.example` to `.env` and fill in the required values. For local development, the defaults work with `docker-compose.yml`.

## How to Contribute

### Reporting Issues

- Use [GitHub Issues](https://github.com/argonBIsystems/infernis/issues)
- Include steps to reproduce, expected vs actual behavior
- For data quality issues, include the coordinates and endpoint you queried

### Pull Requests

1. **Fork the repo** and create a branch from `main`
2. **Write tests** for new features or bug fixes
3. **Follow existing code style** — Ruff handles formatting (line length 100)
4. **Keep PRs focused** — one feature or fix per PR
5. **Write clear commit messages** — imperative mood, short first line

```bash
# Before submitting
make fmt       # Auto-format with ruff
make test      # Run the test suite
ruff check src/ tests/   # Lint check
```

### What We're Looking For

**High-impact contributions:**
- New data source integrations (weather, satellite, fire history)
- Model improvements (training pipeline, feature engineering, architectures)
- API endpoint enhancements
- Performance optimizations for the grid/pipeline system
- Better FWI computation or calibration
- Documentation improvements

**Good first issues:**
- Look for issues labeled [`good first issue`](https://github.com/argonBIsystems/infernis/labels/good%20first%20issue)
- Adding tests for uncovered code paths
- Improving error messages or validation
- Documentation fixes

### Code Structure

```
src/infernis/
  api/          # FastAPI routes, auth middleware
  config.py     # Settings (env-based)
  db/           # SQLAlchemy models, engine
  grid/         # BC grid generation
  models/       # Pydantic schemas, enums
  pipelines/    # Data pipelines (ERA5, HRDPS, GDPS, Open-Meteo, GEE, etc.)
  services/     # FWI computation, caching
  main.py       # FastAPI app entry point
  admin.py      # CLI tools

scripts/
  download/     # 21 data download scripts
  train.py      # Model training
  backtest.py   # Historical backtesting

tests/          # Mirrors src/ structure
```

### Testing

```bash
make test                          # Run all tests
pytest tests/test_smoke.py -v      # Quick smoke tests
pytest tests/ -k "fwi" -v          # Run specific tests
```

Tests run against real PostgreSQL + Redis (via docker-compose), not mocks.

### API Development

The API has public demo endpoints at `/v1/demo/risk` and `/v1/demo/forecast` that return mock data at all danger levels. Use these for testing your integration without needing an API key.

For authenticated endpoints, create a local API key:
```bash
python -m infernis.admin create_key --name "dev-local" --tier free
```

## Code of Conduct

Be respectful, constructive, and collaborative. We're all here to help predict and prevent wildfires.

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Questions?

- Open a [Discussion](https://github.com/argonBIsystems/infernis/discussions)
- Check the [API Reference](docs/API_REFERENCE.md)
- Read the [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)
