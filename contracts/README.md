# SecureDefenseComm Contract

`SecureDefenseComm.sol` is the main authorization contract for the Block Teleplan trust/control plane.

It provides:

- HQ-only group creation and membership administration
- Membership checks for client authorization
- Membership and group audit events
- Reverse lookup of groups for a user
- HQ administrator transfer

The compiled ABI, bytecode, metadata, and compiler build-info are kept under `artifacts/`. The benchmark currently embeds the ABI and bytecode in `benchmark.js` for a self-contained local run. When this contract changes, recompile it and update the benchmark artifact together.

## Important Design Note

The current contract is the source artifact used by the existing benchmark and is preserved as-is. Before production use, review access-control policy, reverse-index cleanup after `removeMember`, event coverage, upgrade policy, and formal security tests. This repository is a research testbed, not a production defence deployment.
