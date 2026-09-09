const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const artifactPath = path.join(root, "contracts", "artifacts", "SecureDefenseComm.json");
const sourcePath = path.join(root, "contracts", "SecureDefenseComm.sol");
const benchmarkPath = path.join(root, "benchmark.js");
const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
const source = fs.readFileSync(sourcePath, "utf8");
const benchmark = fs.readFileSync(benchmarkPath, "utf8");

if (!artifact.abi || !Array.isArray(artifact.abi)) {
  throw new Error("Contract artifact is missing an ABI array.");
}

if (!artifact.data || !artifact.data.bytecode || !artifact.data.bytecode.object) {
  throw new Error("Contract artifact is missing bytecode.");
}

const requiredFunctions = [
  "createGroup",
  "addMember",
  "removeMember",
  "isMember",
  "getGroupMembers",
  "getUserGroups",
  "transferAdmin",
];

const artifactFunctions = new Set(
  artifact.abi
    .filter((entry) => entry.type === "function")
    .map((entry) => entry.name),
);

const missingFunctions = requiredFunctions.filter((name) => !artifactFunctions.has(name));
if (missingFunctions.length > 0) {
  throw new Error(`Artifact is missing functions: ${missingFunctions.join(", ")}`);
}

if (!source.includes("contract SecureDefenseComm")) {
  throw new Error("Canonical Solidity source does not declare SecureDefenseComm.");
}

if (!benchmark.includes("./contracts/artifacts/SecureDefenseComm.json")) {
  throw new Error("benchmark.js is not loading the checked-in SecureDefenseComm artifact.");
}

console.log(`Contract artifact: PASS (${artifact.abi.length} ABI entries)`);
