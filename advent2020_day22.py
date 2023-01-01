from utils import read_data
from collections import deque
from typing import Tuple, Deque, List


def read_input(data: str) -> Tuple[List[int], ...]:
    queues = ([], [])
    playercards = [x.split("\n") for x in data.split("\n\n")]
    for i, card_list in enumerate(playercards):
        # Remove the initial "Player #:" line
        for line in card_list[1:]:
            queues[i].append(int(line))
    return queues


def calc_score(winning_deck: Deque[int]) -> int:
    total_score = 0
    while winning_deck:
        value = len(winning_deck)
        card = winning_deck.popleft()
        total_score += value*card
    return total_score


def run_game_part_one(decks: Tuple[List[int], ...]) -> Deque[int]:
    deck_queues = tuple(deque(x) for x in decks)
    while all(x for x in deck_queues):
        cards = tuple(x.popleft() for x in deck_queues)
        winner = cards.index(max(cards))
        deck_queues[winner].append(cards[winner])
        deck_queues[winner].append(cards[0 if winner else 1])
    return deck_queues[0] if deck_queues[0] else deck_queues[1]


def run_game_part_two(decks: Tuple[List[int], ...], game_num: int = 0) -> Tuple[Tuple[Deque[int], ...], int]:
    deck_queues = tuple(deque(x) for x in decks)
    seen_states = set()
    while all(x for x in deck_queues):
        # Before cards are dealt, if we've seen this order before, exit with player 1 (index 0) as the winner
        state = tuple(tuple(x) for x in deck_queues)
        if state in seen_states:
            return deck_queues, 0
        seen_states.add(state)
        cards = tuple(x.popleft() for x in deck_queues)
        # If there are enough cards to start a subgame, do so
        if all(cards[i] <= len(deck_queues[i]) for i in range(len(deck_queues))):
            game_num += 1
            new_game_state = tuple(list(deck_queues[i])[:cards[i]] for i in range(len(deck_queues)))
            _, winner = run_game_part_two(new_game_state, game_num)
        else:
            winner = cards.index(max(cards))
        deck_queues[winner].append(cards[winner])
        deck_queues[winner].append(cards[0 if winner else 1])
    winner = 0 if deck_queues[0] else 1
    return deck_queues, winner


def main():
    decks = read_input(read_data())
    winning_deck = run_game_part_one(decks)
    print(f"Part one: {calc_score(winning_deck)}")
    final_decks, winner_index = run_game_part_two(decks)
    print(f"Part two: {calc_score(final_decks[winner_index])}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
