# Method

Because the claim remained LOW confidence after discovery, the campaign used
exactly three materially different verification routes and one mandatory
falsification route:

1. Search for an author-released implementation and prediction cache.
2. Audit whether the exact predictions can be faithfully regenerated.
3. Test whether published aggregates uniquely reconstruct the raw result.
4. Seek an assumption-matching contradiction to the exact finite experiment.

`route_evidence.json` records the interpretation, commands, result, control,
and unresolved limitation for each route. `verifier.py` fails unless all four
routes are present, materially distinct, and honestly support `BLOCKED`.
`independent_checker.py` uses no production aggregation code.
