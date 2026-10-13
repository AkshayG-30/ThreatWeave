# GNN Graph Reasoning Experiment Status

## 1. Objective
Demonstrate learned graph reasoning over the existing controlled attack graph using a CPU-friendly GNN (PyTorch Geometric or custom message-passing).

## 2. Experimental Verdict
**Meaningful training/evaluation cannot be completed safely in the remaining time. GNN integration remains future work.**

## 3. Explanation
1. **Infrastructure Risk:** The core dependency, `torch`, is not present in the current production environment. Downloading and installing PyTorch and its geometric ecosystem requires substantial time and bandwidth, posing an unacceptable risk of environment corruption just 30 minutes before the final demo freeze.
2. **Scientific Validity:** The available controlled attack sequence contains only 9 nodes (8 true positive, 1 noise). Training a highly-parameterized neural network (GNN) on a single 9-node topology results in catastrophic overfitting. It cannot demonstrate meaningful generalizable reasoning over deterministic NetworkX logic, which elegantly and correctly filters the noise node without training.

NetworkX currently provides perfect (100%) precision bounding on this topology natively. Consequently, a GNN does not add measurable value to the MVP and is correctly deferred to future work when massive, multi-incident temporal graph datasets are available.
