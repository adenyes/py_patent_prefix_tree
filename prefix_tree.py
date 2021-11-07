# andr00 wrote this because it was faster than trying to read that whole trademark application
from typing import Dict, List

import click
import xml.etree.ElementTree as ET


def pt_add(ptree: Dict, seq: List[str]):
    next_root = ptree
    prefix_exceeded = False
    for token in seq:
        if not prefix_exceeded:
            if token in next_root.keys():
                next_root = next_root[token]
            else:
                prefix_exceeded = True

        if prefix_exceeded:
            next_root[token] = {}
            next_root = next_root[token]


def make_prefix_tree(purposes):
    ptree = {}
    for purpose in purposes:
        pt_add(ptree, purpose.strip().replace(",", " ").split())
    return ptree


def print_tree(prefix_tree, level=0):
    prefixes = prefix_tree.keys()
    for prefix in prefixes:
        print(" " * level + prefix)
        print_tree(prefix_tree[prefix], level + 2)


# concatenates keys in this prefix tree until they have 0 or multiple levels
def compact(prefix_tree):
    oldkeys = list(prefix_tree.keys())
    for key in oldkeys:
        while len(prefix_tree[key].keys()) == 1:
            subkey = list(prefix_tree[key].keys())[0]
            newkey = key + " " + subkey
            prefix_tree[newkey] = prefix_tree[key][subkey]
            del prefix_tree[key]
            key = newkey
        compact(prefix_tree[key])


@click.command()
@click.argument('src_text', type=click.Path(exists=True, dir_okay=False))
@click.option('--xpath', type=click.STRING)
def pre_tree(src_text: str, xpath: str):
    print(f"Printing prefix tree for separated strings in {src_text}")
    tree = ET.parse(src_text)
    root = tree.getroot()
    rtext = root.findtext(xpath)
    purposes = sorted(rtext.split(';'))

    prefix_tree = make_prefix_tree(purposes)
    compact(prefix_tree)
    print_tree(prefix_tree, 0)


if __name__ == "__main__":
    pre_tree()
