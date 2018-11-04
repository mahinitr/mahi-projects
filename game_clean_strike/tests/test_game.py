"""
Module: Test cases for game clean strike
Author: Maheshwar Reddy
"""
import os
import pytest
import sys

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_CASES_FOLDER = os.path.join(CURRENT_DIR, 'test_cases')
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)
from game import Game

INPUT_FILES = []
if os.path.isdir(TEST_CASES_FOLDER):
    for file_ in os.listdir(TEST_CASES_FOLDER):
        file_path = os.path.join(TEST_CASES_FOLDER, file_)
        INPUT_FILES.append(file_path)

@pytest.fixture(params = INPUT_FILES)
def file_path(request):
    return request.param

def _read_from_file(file_path):
    with open(file_path) as fp:
        assert fp.readline().startswith("INPUT") == True
        line = fp.readline()
        assert line.startswith("TURNS") == True
        turns = int(line.split(" ")[1])
        input_outcomes = []
        for i  in range(1, turns + 1):
            line = fp.readline().strip()
            outcome = line.split(" ")[1]
            input_outcomes.append(int(outcome))
        assert fp.readline().startswith("OUTPUT") == True
        expected_result = fp.readline().strip()
        return input_outcomes, expected_result

# Test Case to read input from file
def test_play_game_from_files(file_path):
    print "for input file - ", file_path
    input_outcomes, expected_result = _read_from_file(file_path)
    game = Game()
    loaded = game.init_game(input_outcomes)
    assert loaded == True
    game.play()
    result = game.get_result()
    assert result == expected_result
