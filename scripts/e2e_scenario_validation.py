"""ThreatWeave Phase 12F: End-to-End API & Scenario Workflow Validator.

Systematically validates TC-01 through TC-10, error handling, explanation binding,
and data consistency across all endpoints.
"""
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

def fetch(endpoint):
    url = f"{BASE_URL}{endpoint}"
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

def run_e2e_validation():
    results = {}

    print("================================================================")
    print("PHASE 12F: END-TO-END SCENARIO & API VALIDATION MATRIX")
    print("================================================================")

    # 1. Scenarios Catalogue Check
    print("\n[CHECK 1] Scenario Catalogue Verification (/api/demo/scenarios)")
    status, cat = fetch("/api/demo/scenarios")
    assert status == 200 and len(cat) == 10, f"Failed catalogue: {status}, count={len(cat)}"
    print(f"  PASS: Catalogue returned {len(cat)} scenarios.")
    results["Catalogue_10_Scenarios"] = "PASS"

    # 2. TC-01 through TC-10 Individual Validations
    expected_modes = {
        "TC-01": "LIVE_INFERENCE",
        "TC-02": "LIVE_INFERENCE",
        "TC-03": "LIVE_INFERENCE",
        "TC-04": "LIVE_INFERENCE",
        "TC-05": "DISABLED",
        "TC-06": "LIVE_INFERENCE",
        "TC-07": "LIVE_INFERENCE",
        "TC-08": "RECORDED_EVALUATION",
        "TC-09": "RECORDED_EVALUATION",
        "TC-10": "CONTROLLED_REPLAY"
    }

    for sid, mode in expected_modes.items():
        print(f"\n[VALIDATING {sid}] Expected Mode: {mode}")
        if sid == "TC-05":
            status_sc, d_sc = fetch(f"/api/demo/scenario/{sid}")
            status_ex, d_ex = fetch(f"/api/demo/explanation?scenario_id={sid}")
            assert status_sc == 404, f"TC-05 scenario expected 404, got {status_sc}"
            assert status_ex == 404, f"TC-05 explanation expected 404, got {status_ex}"
            assert "autoencoder model weights do not exist" in d_sc.get("detail", "").lower()
            print(f"  PASS: {sid} is safely disabled (HTTP 404 with diagnostic explanation).")
            results[f"{sid}_Workflow"] = "PASS (DISABLED AS REQUIRED)"
            continue

        # Enabled scenario check
        status_sc, d_sc = fetch(f"/api/demo/scenario/{sid}")
        assert status_sc == 200, f"{sid} scenario failed with status {status_sc}"
        assert d_sc.get("scenario_id") == sid, f"{sid} scenario_id mismatch: {d_sc.get('scenario_id')}"
        assert d_sc.get("execution_mode") == mode, f"{sid} mode mismatch: {d_sc.get('execution_mode')}"
        assert len(d_sc.get("events", [])) > 0, f"{sid} events empty"

        status_ex, d_ex = fetch(f"/api/demo/explanation?scenario_id={sid}")
        assert status_ex == 200, f"{sid} explanation failed with status {status_ex}"
        assert d_ex.get("scenario_id") == sid, f"{sid} explanation scenario_id mismatch"
        assert len(d_ex.get("summary", "")) > 0, f"{sid} explanation summary empty"

        # Scenario-specific semantic checks
        if sid == "TC-01":
            assert d_sc.get("correlation_score", 0.0) == 0.0
            assert len(d_sc.get("edges", [])) == 0
            assert len(d_sc.get("mitre_mappings", [])) == 0
            for ev in d_sc["events"]:
                assert ev["detection_source"] == "NONE"
                assert ev["supervised_score"] < 0.01
                assert ev["anomaly_score"] < 0.009427
            print(f"  PASS: {sid} verified benign baseline (0 alerts, 0 edges, 0 MITRE).")

        elif sid == "TC-02":
            assert len(d_sc.get("edges", [])) > 0
            assert len(d_sc.get("mitre_mappings", [])) > 0
            for ev in d_sc["events"]:
                assert ev["detection_source"] == "SUPERVISED"
                assert ev["supervised_score"] >= 0.99
            print(f"  PASS: {sid} verified high-confidence exploit attacks.")

        elif sid == "TC-06":
            assert len(d_sc.get("edges", [])) > 0
            for ev in d_sc["events"]:
                assert ev["detection_source"] == "BOTH"
            print(f"  PASS: {sid} verified consensus agreement (all BOTH).")

        elif sid == "TC-07":
            sources = {ev["detection_source"] for ev in d_sc["events"]}
            assert "SUPERVISED" in sources and "ANOMALY" in sources
            print(f"  PASS: {sid} verified disagreement split (SUPERVISED and ANOMALY).")

        elif sid == "TC-08":
            assert d_sc["detection_summary"]["holdout_family"] == "Fuzzers"
            assert d_sc["detection_summary"]["fuzzers_recall"] == "68.64%"
            print(f"  PASS: {sid} verified Held-Out Fuzzers evaluation (68.64% recall).")

        elif sid == "TC-09":
            assert d_sc["detection_summary"]["holdout_family"] == "Reconnaissance"
            assert d_sc["detection_summary"]["reconnaissance_recall"] == "100.0%"
            print(f"  PASS: {sid} verified Held-Out Reconnaissance evaluation (100.0% recall).")

        elif sid == "TC-10":
            assert d_sc["incident_id"] == "INC_1"
            assert len(d_sc["events"]) == 8
            assert len(d_sc["edges"]) == 20
            assert len(d_sc["mitre_mappings"]) == 4
            print(f"  PASS: {sid} verified full multi-stage replay (8 events, 20 edges, 4 MITRE).")

        results[f"{sid}_Workflow"] = "PASS"

    # 3. Security & Error Handling Checks
    print("\n[CHECK 3] Security & Error Handling Validation")
    # Path traversal
    st_trav, d_trav = fetch("/api/demo/explanation?scenario_id=../../secrets")
    assert st_trav == 400 and "invalid scenario identifier" in d_trav.get("detail", "").lower()
    print("  PASS: Path traversal rejected with HTTP 400.")
    results["Security_Path_Traversal"] = "PASS"

    # Shell injection characters
    st_inj, d_inj = fetch("/api/demo/explanation?scenario_id=TC-10;cat")
    assert st_inj == 400 and "invalid scenario identifier" in d_inj.get("detail", "").lower()
    print("  PASS: Invalid characters rejected with HTTP 400.")
    results["Security_Shell_Injection"] = "PASS"

    # Nonexistent scenario
    st_404, d_404 = fetch("/api/demo/scenario/NONEXISTENT_999")
    assert st_404 == 404
    print("  PASS: Nonexistent scenario returns HTTP 404.")
    results["Error_Handling_404"] = "PASS"

    print("\n================================================================")
    print("ALL 14 E2E PROGRAMMATIC CHECKS PASSED WITH ZERO FAILURES")
    print("================================================================")
    for k, v in results.items():
        print(f"  {k:30s}: {v}")

if __name__ == "__main__":
    run_e2e_validation()
