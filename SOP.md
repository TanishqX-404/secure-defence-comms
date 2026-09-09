# Standard Operating Procedure

## Purpose

Use this procedure to start, exercise, inspect, and shut down the Block Teleplan local Besu/QBFT testbed. It is for repeatable research work on a developer machine, not for operating a defence production network.

## Before You Start

- Confirm Docker Desktop is running and Docker Compose is available.
- Confirm Node.js 18+ and Python 3.10+ are available.
- Work from the repository root: `C:\Users\tanis\Desktop\Block-Teleplan-Cluster`.
- Do not copy the bundled private keys into another environment. They are public, disposable test fixtures.

## First-Time Setup

```powershell
npm install
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run the Python commands with the full interpreter path or use another shell. Activation is a convenience, not a requirement.

## Start and Verify the Network

```powershell
npm run network:up
npm run network:status
npm run network:logs
```

The host RPC endpoint is `http://127.0.0.1:8545`. The expected chain ID is `1337`. The network contains four validators and uses a two-second QBFT block period.

Before running a benchmark, verify that `validator1` is running and that the logs do not show a genesis, key, or peer-discovery error. The other validators do not publish host RPC ports; they communicate on the Docker network.

## Run the Benchmarks

JavaScript is the main benchmark path:

```powershell
npm run benchmark:js
```

It deploys the embedded access-control contract, seeds one group, and measures repeated `isMember()` view calls for 60 seconds. For a shorter smoke run:

```powershell
$env:BENCHMARK_DURATION_SECONDS = "10"
npm run benchmark:js
Remove-Item Env:BENCHMARK_DURATION_SECONDS
```

The Python script is a smaller transaction-latency smoke check:

```powershell
npm run benchmark:python
```

It sends ten zero-value self-transactions and waits for receipts. It is not the same experiment as the paper's throughput tables.

## Recreate Figures

```powershell
npm run graphs
```

The figures are generated from the values defined in `generate_graphs.py`. Treat them as recorded research-result visualizations, not live telemetry from the current run.

## Reset the Chain

Use a reset when changing genesis settings, recovering from a bad nonce, or starting a clean experiment:

```powershell
npm run network:reset
npm run network:up
```

This removes Docker volumes and therefore deletes the local chain state. It does not delete source files.

## Stop and Clean Up

```powershell
npm run network:down
```

Use `npm run network:logs` before shutdown when capturing a result or diagnosing a failure. Keep benchmark output, machine details, configuration changes, and the exact reset/start sequence with any result that may be cited later.

## Troubleshooting

`Cannot connect to node`: start Docker, run `npm run network:status`, then inspect `npm run network:logs`.

`insufficient funds` or a nonce error: reset the local chain with `npm run network:reset`, start it again, and rerun the benchmark.

`web3` import failure: activate the Python environment and run `python -m pip install -r requirements.txt`.

Caliper cannot find its workload: the current checkout retains Caliper configuration but does not contain the referenced `benchmarks/scenario/simple/open.js` workload. Treat that path as incomplete reference material until the workload is restored and a containerized run is verified.

## Reproducibility Checklist

- Record the commit or archive version of this folder.
- Record OS, Docker, Node.js, Python, Besu, and dependency versions.
- Record whether the chain was reset before the run.
- Record benchmark duration, RPC endpoint, transaction load, and output.
- Do not report the checked-in figure values as a new measurement without rerunning the experiment and retaining the raw output.
