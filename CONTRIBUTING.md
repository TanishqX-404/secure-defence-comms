# Contributing

Keep this repository focused on reproducible research infrastructure for the Block Teleplan authorization-layer testbed.

Before opening a change:

1. Read [README.md](README.md), [SOP.md](SOP.md), and [docs/PROJECT_MAP.md](docs/PROJECT_MAP.md).
2. Run `npm test` and `python -m py_compile benchmark.py generate_graphs.py`.
3. Run `npm run graphs` when changing graph generation.
4. Never commit `.env` files, local validator private keys, Docker volumes, or generated caches.
5. Record changes to benchmark parameters and explain whether results are measured or illustrative.

Pull requests should describe the environment used, the commands run, and any limitation that prevents a Docker-backed validation.
