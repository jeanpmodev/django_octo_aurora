# 🧪 Quality Assurance & Testing Methodology

[![Tests: pytest](https://img.shields.io/badge/Tests-pytest%20passed-2ea44f.svg)](#2-unit--query-count-validation-pytest)
[![BDD: Behave](https://img.shields.io/badge/BDD-Behave%20verified-009688.svg)](#3-behavioral--bdd-specifications-behave)
[![Load Test: Locust](https://img.shields.io/badge/Load_Test-11ms_median_%7C_0%25_fails-blueviolet.svg)](performance/locust_load_report.pdf)


---

## 1. Local QA Environment Setup
Synchronize the development dependencies using **Rye**:
```bash
rye sync
```

---

## 2. Unit & Query-Count Validation (`pytest`)
Verifies AST directory introspection, schema migrations, Django Admin snapshot refresh actions, and enforces the **Single Database Lookup (`django_assert_num_queries(1)`)** contract:
```bash
PYTHONPATH=src pytest
```

---

## 3. Behavioral / BDD Specifications (`behave`)
Executes Gherkin scenarios (`features/aurora_topology.feature`) validating single-query showcase rendering and administrative snapshot persistence end-to-end:
```bash
PYTHONPATH=src behave
```

---

## 4. Load & Concurrency Stress Benchmark (`locust`)
Simulates 50 concurrent users hitting the single-query Aurora showcase endpoint:

```bash
# Terminal 1: Start runtime service
PYTHONPATH=src python3 manage.py runserver --noreload

# Terminal 2: Execute 15s headless load test
locust -f performance/locustfile.py --headless -u 50 -r 10 --run-time 15s --host http://127.0.0.1:8000
```


📄 **[View Official Locust Load Test Report (PDF)](performance/locust_load_report.pdf)**

