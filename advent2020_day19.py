from utils import read_data
from typing import Dict, List, Set, Iterable
from dataclasses import dataclass
from itertools import islice


@dataclass
class Rule:
    id: int
    chains: List[List[int]]
    matches: Set[str]
    fully_known: bool

    def can_be_known(self, known_rule_ids: Set[str]):
        return all(all(x in known_rule_ids for x in chain) for chain in self.chains)


def process_rules(data: List[str]) -> Dict[str, Rule]:
    rules_dict = {}
    for rule in data:
        id, rule_text = rule.split(": ")
        if rule_text.endswith("\""):
            rules_dict[id] = Rule(id=id, chains=[], matches=set(rule_text.replace("\"", "")), fully_known=True)
        else:
            chains = [x.split(" ") for x in rule_text.split(" | ")]
            rules_dict[id] = Rule(id=id, chains=chains, matches=set(), fully_known=False)
    return rules_dict


def fill_out_rules(rules_dict: Dict[str, Rule]):
    while len(known_rule_ids := {x.id for x in rules_dict.values() if x.fully_known}) < len(rules_dict):
        rules_what_can_be_known = [x for x in rules_dict.values() if not x.fully_known and x.can_be_known(known_rule_ids)]

        # if there's a recursive rule, this will stop the loop before trying to recurse
        if not rules_what_can_be_known:
            break

        for rule in rules_what_can_be_known:
            # For each rule, attempt to build a set of all possible strings it matches
            full_matches = set()
            for chain in rule.chains:
                # Process each or'd chain separately, then combine them at the end
                chain_texts = set()
                for ruleid in chain:
                    if not chain_texts:
                        # Start by copying the first chained rule's string set whole
                        chain_texts = rules_dict[ruleid].matches.copy()
                    else:
                        # Once we have something to start with, start appending other elements to the strings.
                        # Using list(chain_texts) to make a copy so it won't complain about us modifying the thing
                        # we're iterating through.
                        for text in list(chain_texts):
                            # Get rid of the old incomplete version before we start appending
                            chain_texts.discard(text)
                            for match in rules_dict[ruleid].matches:
                                chain_texts.add(text + match)
                # Add the per-chain text sets to the full rule text set
                full_matches.update(chain_texts)
            rule.matches = full_matches
            rule.fully_known = True
    return rules_dict


def check_text_part_one(text: str, rules_dict: Dict[str, Rule]) -> bool:
    return text in rules_dict['0'].matches


def check_text_part_two(text: str, rules_dict: Dict[str, Rule]) -> bool:
    def grouper(n: int, iterable: Iterable):
        it = iter(iterable)
        while True:
            chunk = tuple(islice(it, n))
            if not chunk:
                return
            yield ''.join(chunk)

    # First off, everything is done in chunks of 8, so early-invalidate anything that isn't a multiple of 8 long
    chunk_length = len(next(iter(rules_dict['42'].matches)))
    if len(text) % chunk_length != 0:
        return False

    # The rule is that there has to be at least one 42-set at the beginning, followed by a matched number of 42 and 31
    # The algorithm, therefore, is to start at the end, match 31 sets backwards, and then once we've stopped match
    # 42 sets until we've hit at least n+1 of them
    reversed_chunks = tuple(reversed(tuple(grouper(chunk_length, text))))
    num_31s = 0
    for chunk in reversed_chunks:
        if chunk in rules_dict['31'].matches:
            num_31s += 1
        else:
            break
    num_42s = 0
    for chunk in reversed_chunks[num_31s:]:
        if chunk in rules_dict['42'].matches:
            num_42s += 1
        else:
            # Once we've run out of 31s, it has to be 42s all the way to the start
            return False
    # There has to be at least 1 num_31s, and num_42s has to be greater than num_31s
    return 1 <= num_31s < num_42s


rules, texts = (x.split("\n") for x in read_data().split("\n\n"))
blank_rules = process_rules(rules)
full_rules = fill_out_rules(blank_rules)
print(f"Part one: {sum(check_text_part_one(x, full_rules) for x in texts)}")
print(f"Part two: {sum(check_text_part_two(x, full_rules) for x in texts)}")
