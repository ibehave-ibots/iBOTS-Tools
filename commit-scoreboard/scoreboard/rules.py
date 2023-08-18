def should_play_sound(interval: int, old_score: int, new_score: int) -> bool:
    return new_score // interval > old_score // interval
