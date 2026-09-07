# ============================================================
# ALGORITHM 11
# CONVERT_TO_FLOAT(seed)
# ============================================================

import random


def convert_to_float(seed):
   """Generates a random float between 3.57 and 4.0 using the seed.

   Uses an independent generator so call order doesn't mess up values.
   """
   # Create an isolated random instance
   rng = random.Random(seed)

   # Generate random float between 3.57 and 4.0
   random_float = rng.uniform(3.57, 4.0)


   return random_float