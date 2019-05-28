from floptimizer import DKAPIClient

dk_client = DKAPIClient()
dk_client.mlb.get_contests()
assert(dk_client.mlb.all_contests)
