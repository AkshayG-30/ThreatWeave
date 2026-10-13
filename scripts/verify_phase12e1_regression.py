"""Phase 12E.1 Regression & Integrity Verification Script."""
import os
import json
import hashlib
import urllib.request
import urllib.error

def get_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    print("=== 1. PRODUCTION & ARTIFACT INTEGRITY ===")
    artifacts = [
        'models/xgboost_detector.json',
        'models/isolation_forest.joblib',
        'models/feature_columns.json',
        'experiments/unseen_attack/models/xgb_holdout_Fuzzers.json',
        'experiments/unseen_attack/models/xgb_holdout_Reconnaissance.json',
        'experiments/unseen_attack/results.json',
        'experiments/unseen_attack/config.json'
    ]
    for p in artifacts:
        assert os.path.exists(p), f"Missing {p}"
        h = get_hash(p)[:16]
        sz = os.path.getsize(p)
        print(f"  {p}: sha256={h}... ({sz} bytes)")

    def fetch(url):
        try:
            with urllib.request.urlopen(url) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode())

    print("\n=== 2. TC-10 VERIFICATION ===")
    status, d_tc10 = fetch('http://127.0.0.1:8000/api/demo/scenario/TC-10')
    assert status == 200, f"TC-10 status {status}"
    print(f"  TC-10 incident: {d_tc10['incident_id']}")
    print(f"  Events: {len(d_tc10['events'])}")
    print(f"  Edges: {len(d_tc10['edges'])}")
    print(f"  MITRE mappings: {len(d_tc10['mitre_mappings'])}")
    assert d_tc10['incident_id'] == 'INC_1'
    assert len(d_tc10['events']) == 8
    assert len(d_tc10['edges']) == 20
    assert len(d_tc10['mitre_mappings']) == 4

    print("\n=== 3. TC-05 DISABLED VERIFICATION ===")
    status_05, d_tc05 = fetch('http://127.0.0.1:8000/api/demo/scenario/TC-05')
    print(f"  TC-05 status: {status_05}, detail: {d_tc05.get('detail')}")
    assert status_05 == 404
    assert 'autoencoder model weights do not exist' in d_tc05.get('detail').lower()

    print("\n=== 4. SCENARIO-AWARE EXPLANATIONS ===")
    for sid in ['TC-01', 'TC-02', 'TC-08', 'TC-10']:
        status_exp, d_exp = fetch(f'http://127.0.0.1:8000/api/demo/explanation?scenario_id={sid}')
        assert status_exp == 200, f"Failed {sid}: {d_exp}"
        print(f"  {sid}: scenario_id={d_exp['scenario_id']}, incident_id={d_exp['incident_id']}, provider={d_exp['provider']}, fallback={d_exp['fallback_used']}")
        assert d_exp['scenario_id'] == sid

    print("\n=== 5. TC-08 PHYSICAL EVIDENCE CHECK ===")
    with open('experiments/unseen_attack/results.json') as f:
        unseen_res = json.load(f)
    fuz_res = unseen_res['Fuzzers']
    print(f"  Holdout Family: {fuz_res['Holdout_Family']}")
    print(f"  Test Support: {fuz_res['Support']} Fuzzers flows, {fuz_res['Test_Size']} total test flows")
    print(f"  Recall: {fuz_res['Recall'] * 100:.2f}% ({fuz_res['True_Positives']}/{fuz_res['Support']})")
    print(f"  Precision: {fuz_res['Precision'] * 100:.2f}%")
    print(f"  F1: {fuz_res['F1'] * 100:.2f}%")
    print(f"  FPR: {fuz_res['FPR'] * 100:.2f}%")

    print("\n=== ALL CHECKS PASSED SUCCESSFULLY ===")

if __name__ == '__main__':
    main()
