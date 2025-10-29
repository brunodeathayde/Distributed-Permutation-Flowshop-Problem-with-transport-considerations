# 🧠 Scheduling Optimization Models: MILP & CP

This repository contains Python implementations of scheduling models using both Mixed Integer Linear Programming (MILP) and Constraint Programming (CP). The models are designed to solve flow shop scheduling problems with transport times and job families.

---

## ⚙️ Optimization Models

| File         | Description |
|--------------|-------------|
| `MILP.py`    | MILP model implemented using Gurobi and CPLEX solvers |
| `CP_IBM.py`  | CP model implemented using IBM ILOG CPLEX CP Optimizer |
| `CP_HEXALY.py` | CP model implemented using Hexaly (Python CP solver) |

Each model defines decision variables, constraints, and objective functions tailored to minimize makespan and/or total tardiness in flow shop environments.

---

## 🧪 Test Scripts

| File              | Description |
|-------------------|-------------|
| `Test_MILP.py`    | Test script for evaluating the MILP model |
| `Test_CP_IBM.py`  | Test script for evaluating the IBM CP model |
| `Test_CP_HEXALY.py` | Test script for evaluating the Hexaly CP model |

These scripts load instance data, configure solver parameters, and execute the optimization routines. They also collect performance metrics such as execution time, solution quality, and feasibility status.

---

## 📦 Features

- Support for multiple solvers: Gurobi, CPLEX (MILP), IBM CP Optimizer, Hexaly (CP)
- Modular design for easy integration and benchmarking
- Compatible with instance datasets including transport times and job families
- Customizable objective functions and constraints

---

## 🚀 Getting Started

1. Install required solvers and Python packages:
   ```bash
   pip install gurobipy cplex docplex hexaly
