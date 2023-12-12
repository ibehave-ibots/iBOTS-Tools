import pytest
from typing import List, Sequence, Tuple
from datetime import datetime

cases = [
    [(4, 3)],
    [(54.2, 54.1), (32, 1)],
]
@pytest.mark.parametrize("tranges", cases)
def test_validate_a_lessthan_b(tranges):
    with pytest.raises(ValueError):    
        merge_timeranges(tranges)


cases = [
    [],
    [(7, 12)],
    [(3, 5), (6, 9)],
    [(1, 2), (3, 4), (5, 6)]
]
@pytest.mark.parametrize("tranges", cases)
def test_nonoverlapping_inputs_passes_through_unchanged(tranges):
    merged = merge_timeranges(tranges)
    assert merged == tranges


cases = [
    [[(6, 9), (3, 5)], [(3, 5), (6, 9)]],
    [[(3, 4), (1, 2), (5, 6)], [(1, 2), (3, 4), (5, 6)]],
    [[(3, 4), (5, 6), (1, 2)], [(1, 2), (3, 4), (5, 6)]]
]
@pytest.mark.parametrize("tranges,merged", cases)
def test_nonoverlapping_inputs_are_sorted(tranges, merged):
    merged_obs = merge_timeranges(tranges)
    assert merged == merged_obs


cases = [
    [[(3, 5), (5, 9)], [(3, 9)]],
    [[(1, 2), (2, 4), (4, 6)], [(1, 6)]],
    [[(2, 4), (1, 2), (4, 6)], [(1, 6)]],
]
@pytest.mark.parametrize("tranges,merged", cases)
def test_butting_inputs_are_completely_merged(tranges, merged):
    merged_obs = merge_timeranges(tranges)
    assert merged == merged_obs


cases = [
    [[(3, 5), (4, 9)], [(3, 9)]],
    [[(1, 2), (1, 4), (3, 6)], [(1, 6)]],
    [[(1, 2), (1, 4), (5, 6)], [(1, 4), (5, 6)]],
    [[(1, 2), (1, 4), (5, 6), (7, 8), (7, 9)], [(1, 4), (5, 6), (7, 9)]],
    [[(7, 9), (5, 6), (1, 4), (7, 8), (1, 2)], [(1, 4), (5, 6), (7, 9)]],
]
@pytest.mark.parametrize("tranges,merged", cases)
def test_overlapping_inputs_are_merged(tranges, merged):
    merged_obs = merge_timeranges(tranges)
    assert merged == merged_obs


dt = datetime
cases = [
 [
     [(dt(2023, 1,1), dt(2023, 1,5))], 
     [(dt(2023, 1,1), dt(2023, 1,5))]
 ],
 [
     [(dt(2023, 3, 1), dt(2023, 3, 15)), (dt(2023, 3, 15), dt(2023, 3, 16)), (dt(2023, 3, 16), dt(2023, 3, 17))], 
     [(dt(2023, 3, 1), dt(2023, 3, 17))]
 ]
]
@pytest.mark.parametrize("tranges,merged", cases)
def test_with_datetimes(tranges, merged):
    merged_obs = merge_timeranges(tranges)
    assert merged == merged_obs
    

######### Source Code ###########

def merge_timeranges(ranges: Sequence[Tuple]) -> List[Tuple]:
    """
    Merges overlapping time ranges.
    Each time range is a tuple of two elements, where the first element is the start time and the second is the end time. 

    Args:
        ranges (Sequence[Tuple]): A sequence of tuples representing time ranges. Each tuple contains two elements: (start_time, end_time).

    Returns:
        List[Tuple]: A list of merged time ranges. Each tuple in the list contains two elements: (start_time, end_time).

    Raises:
        ValueError: If any time range has a start time greater than its end time.

    Examples:
        >>> merge_timeranges([(1, 3), (2, 5), (6, 8)])
        [(1, 5), (6, 8)]
    """

    if len(ranges) == 0:
        return []

    # Input Validation
    for start, end in ranges:
        if start > end:
            raise ValueError("First element should be smaller than the second element")
        
    # Calculate
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    for current_start, current_end in sorted_ranges[1:]:
        ref_start, ref_end = merged[-1]
        if current_start <= ref_end:
            merged[-1] = (ref_start, max(current_end, ref_end))
        else:
            merged.append((current_start, current_end))

    return merged
        
