# GRU Temporal Experiment Status

## 1. Objective
Create a CPU-friendly GRU experiment demonstrating sequential event modelling as a complement to deterministic correlation.

## 2. Experimental Verdict
**GRU experiment not scientifically validated because the available production dataset lacks reliable temporal ground truth.**

## 3. Explanation
The NF-UNSW-NB15-v2 dataset does not provide the absolute chronological timestamps required to window events into ordered sequences for Recurrent Neural Network (RNN/GRU) training. While a single controlled synthetic sequence (8 events) exists for correlation testing (Phase 3/4), this is severely insufficient for training a neural network, which requires thousands of genuine chronological sequences. 

Fabricating timestamps or randomly shuffling data to simulate sequences was explicitly forbidden by project integrity rules. Thus, the experiment was correctly halted to preserve scientific validity.
