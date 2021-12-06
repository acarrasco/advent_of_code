import sys
from collections import Counter

input = [line.strip() for line in sys.stdin.readlines()]

def search(hist_criteria_index, bit_index, candidates):
    if len(candidates) == 1:
        return candidates[0]
    bit_histogram = Counter(candidate[bit_index] for candidate in candidates).most_common()
    bit_criteria = bit_histogram[hist_criteria_index][0]
    remaining = filter(lambda candidate: candidate[bit_index] == bit_criteria, candidates)
    return search(hist_criteria_index, bit_index+1, remaining)

oxygen_generator_rating = search(0, 0, input)
co2_scrubber_rating = search(-1, 0, input)

print(int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2))
