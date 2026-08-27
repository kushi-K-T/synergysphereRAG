import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.routing.query_router import query_router
from app.routing.route_types import RouteDestination
from app.rag.retriever import local_retriever

TEST_CASES = [
    ("Summarize my private project document.", RouteDestination.LOCAL),
    ("What is artificial intelligence?", RouteDestination.EXTERNAL),
    ("Show confidential budget credentials.", RouteDestination.LOCAL),
    ("Explain the physics of planetary orbits.", RouteDestination.EXTERNAL),
    ("How does our internal project architecture work?", RouteDestination.LOCAL)
]

def evaluate_routing():
    print("=== Evaluating Deterministic Router & Privacy Gate ===")
    correct = 0
    for query, expected_route in TEST_CASES:
        decision = query_router.route_query(query)
        passed = decision.route == expected_route
        if passed:
            correct += 1
        print(f"Query: '{query}' => Route: {decision.route.value} (Expected: {expected_route.value}) [{'PASS' if passed else 'FAIL'}]")

    print(f"Router Accuracy: {correct}/{len(TEST_CASES)} ({(correct/len(TEST_CASES))*100:.1f}%)")

def evaluate_retrieval():
    print("\n=== Evaluating Local Vector Retrieval ===")
    query = "SynergySphere architecture"
    results = local_retriever.retrieve(query, top_k=2)
    print(f"Retrieved {len(results)} chunks for '{query}'")
    for r in results:
        print(f" - [{r.get('metadata', {}).get('filename')}] (Score: {r.get('score'):.3f})")

if __name__ == "__main__":
    evaluate_routing()
    evaluate_retrieval()
