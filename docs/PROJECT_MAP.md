# Project Map

This is a small research workspace with several distinct code areas. Keep changes inside the area they belong to and update the SOP when a run step changes.

## Runtime

`docker-compose.yml` owns the local four-validator Hyperledger Besu 23.4.1 network. `networkFiles/genesis.json` defines chain ID 1337 and QBFT timing. `networkFiles/static-nodes.json` and `networkFiles/keys/` support local peer identity and discovery.

## Benchmarks

`benchmark.js` is the primary JavaScript benchmark. It deploys the embedded contract bytecode, creates a group, and measures repeated read-only membership checks.

`benchmark.py` is a separate Web3 smoke benchmark for ten receipt-confirmed transactions. Do not combine its latency output with the JavaScript read-path output.

The embedded ABI and bytecode in `benchmark.js` are a frozen test artifact. If the contract changes, regenerate both together and record the compiler version.

## Analysis

`generate_graphs.py` produces the two checked-in figures from the hard-coded Phase 3 result arrays. It is reporting code, not a live metrics collector. Keep raw measurements separately when extending the experiment.

## Caliper Reference

`caliper/` contains an older network configuration, contract artifact, and Dockerfile. Its configuration points to a workload path that is not present in this checkout, so it is labeled reference/incomplete until that workload is restored.

## Change Guide

- Change validator count, consensus timing, or chain ID: update `docker-compose.yml`, `networkFiles/genesis.json`, and this map/SOP together.
- Change benchmark endpoint or credentials: use `BENCHMARK_RPC_URL` and `BENCHMARK_PRIVATE_KEY`; do not add real credentials to source.
- Change benchmark duration: use `BENCHMARK_DURATION_SECONDS` for one-off runs or edit the documented default deliberately.
- Change result figures: update `generate_graphs.py` and retain the source measurements and run metadata.
- Add a new experiment: give it a descriptive script name, add an npm command, and document its reset/cleanup behavior in `SOP.md`.
