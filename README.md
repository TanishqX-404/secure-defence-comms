# Block Teleplan Cluster

A reproducible local testbed for the permissioned blockchain authorization layer of the Block Teleplan research project. The active implementation in this folder is a four-validator Hyperledger Besu QBFT network plus small benchmark and analysis scripts.

📄 This work is based on the paper *"Blockchain-Based Secure Communication Platform for Defence Personnel,"* accepted and presented at **IEEE SPACE 2026**. Proceedings publication pending — citation will be added once available.

## Key Results

The paper reports a read-intensive authorization result of 3,140 TPS and a four-node QBFT write benchmark that reaches 342 TPS at a submitted load of 5,000 transactions. Those are paper results; this repository is the experiment harness and does not silently claim to reproduce them on every machine.

## Start Here

1. Install Docker Desktop with Docker Compose, Node.js 18 or newer, and Python 3.10 or newer.
2. Install the JavaScript dependencies: `npm install`.
3. Install the Python dependencies in a virtual environment: `python -m pip install -r requirements.txt`.
4. Start the local network: `npm run network:up`.
5. Check the containers: `npm run network:status`.
6. Run the JavaScript resilience/read benchmark: `npm run benchmark:js`.
7. Regenerate the research figures: `npm run graphs`.
8. Stop the network when finished: `npm run network:down`.

The full operating procedure, reset behavior, troubleshooting, and reproducibility checklist are in [SOP.md](SOP.md). The component ownership and change map is in [docs/PROJECT_MAP.md](docs/PROJECT_MAP.md).

## Command Map

| Command | Purpose |
| --- | --- |
| `npm run network:up` | Start the four Besu validators in Docker Compose |
| `npm run network:status` | Show validator container state |
| `npm run network:logs` | Show recent validator logs |
| `npm run benchmark:js` | Deploy the embedded access-control contract and run the 60-second read test |
| `npm run benchmark:python` | Send ten simple transactions through Web3 |
| `npm run graphs` | Recreate `throughput_analysis.png` and `latency_analysis.png` |
| `npm test` | Check JavaScript syntax |
| `npm run network:reset` | Stop the network and delete its Docker volumes |

`npm run network:reset` is intentionally destructive to the local chain state. Use it when a genesis, validator, or nonce reset is needed.

## Repository Labels

- `docker-compose.yml`: local four-validator Besu/QBFT runtime.
- `networkFiles/`: genesis, static peer list, and disposable local validator keys.
- `benchmark.js`: JavaScript contract deployment and read-path resilience benchmark.
- `benchmark.py`: small Python transaction latency smoke benchmark.
- `caliper/`: an earlier Caliper benchmark configuration and container definition; it is retained for reference but is not currently a complete runnable workflow because its workload module is not present in this checkout.
- `generate_graphs.py`: recreates the figures from the recorded Phase 3 values embedded in the script.
- `docs/PROJECT_MAP.md`: what belongs where and where to make future changes.
- `SOP.md`: the repeatable operator workflow.

## Important Scope Notes

This repository covers the blockchain trust/control-plane testbed only. The paper's VPN, E2EE mobile client, HQ dashboard, device containment controls, field deployment, and adversarial/DIL testing are not implemented here. The keys in the local network configuration are development fixtures with zero production value; never reuse them in a real deployment.

The benchmark scripts accept `BENCHMARK_RPC_URL` and `BENCHMARK_PRIVATE_KEY` environment variables when you need to point at a different local test network. Do not put real credentials in this repository.

## GitHub Publishing

This folder is prepared to be published as a source repository, but inspect `git status` and `git diff --cached` before the first push. Local validator private keys under `networkFiles/keys/**/key` are ignored. The keys embedded in `docker-compose.yml` and the benchmark defaults are disposable development fixtures only; replace them before using this configuration outside a throwaway local network.
