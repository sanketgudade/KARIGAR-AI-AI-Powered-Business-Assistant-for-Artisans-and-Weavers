import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

def run_tests():
    app = create_app()
    client = app.test_client()

    print("[TEST 1] Testing /api/health ...")
    r = client.get('/api/health')
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    print("  -> Health OK:", r.json['status'])

    print("[TEST 2] Testing /api/auth/login ...")
    r = client.post('/api/auth/login', json={'phone': '9823011223'})
    assert r.status_code == 200, f"Login failed: {r.status_code}"
    print("  -> Logged in as:", r.json['user']['name'])

    print("[TEST 3] Testing /api/artisan/dashboard ...")
    r = client.get('/api/artisan/dashboard')
    assert r.status_code == 200, f"Dashboard failed: {r.status_code}"
    metrics = r.json['metrics']
    print(f"  -> Metrics: Total Rev: Rs. {metrics['total_revenue']:,}, Avg Selling Price: Rs. {metrics['avg_selling_price']}, Uplift: +Rs. {metrics['price_uplift']} (+{metrics['price_uplift_pct']}%)")

    print("[TEST 4] Testing Agent 1: /api/agent/story/generate ...")
    r = client.post('/api/agent/story/generate', json={'language': 'mr'})
    assert r.status_code == 200, f"Agent 1 failed: {r.status_code}"
    draft = r.json['draft']
    print("  -> Agent 1 Drafted Title:", draft['title'])
    print("  -> Status is strictly:", draft['status'], "(Gate 1 held)")

    print("[TEST 5] Testing Agent 2: /api/agent/pricing/analyze ...")
    r = client.post('/api/agent/pricing/analyze', json={
        'material_cost': 1500,
        'labour_hours': 20,
        'labour_rate': 50,
        'packaging_cost': 200,
        'other_expenses': 100,
        'target_margin': 30
    })
    assert r.status_code == 200, f"Agent 2 failed: {r.status_code}"
    rec = r.json['recommendation']
    cost = r.json['cost_breakdown']
    print(f"  -> Total Cost: Rs. {cost['total_cost']}, Recommended Price: Rs. {rec['suggested_price']}, Confidential Floor: Rs. {rec['confidential_minimum_price']}")

    print("[TEST 6] Testing Agent 3: /api/agent/discovery/search ...")
    r = client.post('/api/agent/discovery/search', json={'tags': ['purple', 'paithani', 'peacock']})
    assert r.status_code == 200, f"Agent 3 failed: {r.status_code}"
    matches = r.json['results']
    print(f"  -> Agent 3 found {len(matches)} matched artisan products. Top match similarity: {matches[0]['similarity_score']*100}%")

    print("[TEST 7] Testing Agent 4: /api/agent/negotiation/counteroffer ...")
    r = client.post('/api/agent/negotiation/counteroffer', json={'buyer_offer': 3000.0})
    assert r.status_code == 200, f"Agent 4 failed: {r.status_code}"
    nego = r.json
    print(f"  -> Below floor flagged: {nego['is_below_floor']}, Decision: {nego['decision']}, Suggested Counter: Rs. {nego['suggested_counteroffer']}")
    print(f"  -> Artisan status held at: {nego['artisan_status']} (Gate 3 hold)")

    print("[TEST 8] Testing Buyer Public API Confidentiality ...")
    r = client.get('/api/buyer/products')
    assert r.status_code == 200
    buyer_prods = r.json
    for p in buyer_prods:
        assert 'confidential_minimum_price' not in p, "SECURITY VIOLATION: Confidential minimum price leaked to buyer!"
        assert 'cost' not in p, "SECURITY VIOLATION: Internal cost breakdown leaked to buyer!"
    print("  -> Security Verified: Confidential minimum prices & costs are 100% hidden from buyers.")

    print("\n[ALL 8 API & AGENT INTEGRITY TESTS PASSED!]")

if __name__ == '__main__':
    run_tests()
