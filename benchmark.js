const { ethers } = require("ethers");

const PROVIDER_URL = process.env.BENCHMARK_RPC_URL || "http://127.0.0.1:8545";
// This key belongs to the disposable local test network only.
const PRIVATE_KEY = process.env.BENCHMARK_PRIVATE_KEY || "0xcd0df6fa5d0bd9f0e4240b024878d1612a7900bc19c09f8989a3e57e44986a9a";
const DURATION_SECONDS = Number(process.env.BENCHMARK_DURATION_SECONDS || 60);
const contractArtifact = require("./contracts/artifacts/SecureDefenseComm.json");
const CONTRACT_ABI = contractArtifact.abi;
const CONTRACT_BYTECODE = `0x${contractArtifact.data.bytecode.object}`;

let latencies = [];
let successCount = 0;
let failCount = 0;

async function getProvider() {
    const provider = new ethers.JsonRpcProvider(PROVIDER_URL);
    await provider.getNetwork();
    return provider;
}

async function deployContract() {
    console.log("Connecting to node...");
    const provider = await getProvider();
    const network = await provider.getNetwork();
    console.log(`Connected. Node reports Chain ID: ${network.chainId}`);

    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
    console.log("Deploying SecureDefenseComm...");

    const factory = new ethers.ContractFactory(CONTRACT_ABI, CONTRACT_BYTECODE, wallet);
    const deployTx = await factory.getDeployTransaction();
    deployTx.chainId = network.chainId;
    deployTx.type = 0;
    deployTx.gasPrice = 0;
    deployTx.gasLimit = 10000000;

    const txResponse = await wallet.sendTransaction(deployTx);
    await txResponse.wait();

    const receipt = await provider.getTransactionReceipt(txResponse.hash);
    const contractAddress = txResponse.contractAddress || receipt.contractAddress;
    console.log(`SecureDefenseComm deployed at: ${contractAddress}`);

    return new ethers.Contract(contractAddress, CONTRACT_ABI, wallet);
}

async function runResilienceTest() {
    console.log(`\n=== STARTING FAULT TOLERANCE TEST (${DURATION_SECONDS} seconds) ===`);

    try {
        const contract = await deployContract();

        console.log("Seeding initial group...");
        const tx = await contract.createGroup("ResilienceGroup", { gasPrice: 0, gasLimit: 1000000 });
        await tx.wait();
        console.log("Seed complete. Starting load...");

        const testStart = Date.now();
        const endAt = testStart + DURATION_SECONDS * 1000;
        let requestCount = 0;

        const reporter = setInterval(() => {
            const elapsed = ((Date.now() - testStart) / 1000).toFixed(0);
            console.log(`[${elapsed}s] Instant requests: ${requestCount} | Status: ${requestCount > 0 ? "running" : "stalled"}`);
            requestCount = 0;
        }, 1000);

        while (Date.now() < endAt) {
            try {
                const start = process.hrtime();
                await contract.isMember(1, contract.runner.address);
                const elapsed = process.hrtime(start);
                latencies.push(elapsed[0] * 1000 + elapsed[1] / 1e6);
                requestCount++;
                successCount++;
            } catch (error) {
                failCount++;
            }
        }

        clearInterval(reporter);
        calculateStats();
    } catch (error) {
        console.error("\nFATAL ERROR:", error);
        process.exitCode = 1;
    }
}

function calculateStats() {
    console.log("\n=== TEST COMPLETE ===");
    if (latencies.length === 0) {
        console.log("No successful requests.");
        return;
    }

    latencies.sort((a, b) => a - b);
    const mean = latencies.reduce((total, value) => total + value, 0) / latencies.length;
    const p95 = latencies[Math.min(Math.floor(latencies.length * 0.95), latencies.length - 1)];

    console.log("\n--- Final Metrics ---");
    console.log(`Total Requests: ${successCount}`);
    console.log(`Failed Requests: ${failCount}`);
    console.log(`Mean Latency: ${mean.toFixed(2)} ms`);
    console.log(`95th Percentile: ${p95.toFixed(2)} ms`);
}

runResilienceTest();
