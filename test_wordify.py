# wordify exercise
#
# Demonstrates a function which turns a numeric currency string into english words
#
# E.g., "$207.32" is converted to "two hundred seven dollars and thirty-two cents"

# Let's give our money the respect of a proper Decimal, instead of stinky fluctuating floats
from decimal import Decimal, InvalidOperation
import pytest

# Ranges define how large a number we can convert, and how each portion of the number is treated during conversion
#   Name = what these are called
#   Upper = the maximum value
#   Lower = the minimum value
#   Plural = is the name pluralized when not "1"?
#   Mandatory = is this name mandatory even when value is 0?
ranges = [
    {
        "name": "million",
        "upper": Decimal("1000000000"),
        "lower": Decimal("1000000"),
        "plural": False,
        "mandatory": False,
    },
    {
        "name": "thousand",
        "upper": Decimal("1000000"),
        "lower": Decimal("1000"),
        "plural": False,
        "mandatory": False,
    },
    {
        "name": "dollar",
        "upper": Decimal("1000"),
        "lower": Decimal("1"),
        "plural": True,
        "mandatory": True,
    },
    {
        "name": "cent",
        "upper": Decimal("1"),
        "lower": Decimal("0.01"),
        "plural": True,
        "mandatory": False,
    },
]

# Word Dictionaries tell us which words go with which numbers!
words_dicts = {
    "singles": {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        0: "zero",
    },
    "tens": {
        2: "twenty",
        3: "thirty",
        4: "forty",
        5: "fifty",
        6: "sixty",
        7: "seventy",
        8: "eighty",
        9: "ninety",
    },
    "teens": {
        0: "ten",
        1: "eleven",
        2: "twelve",
        3: "thirteen",
        4: "fourteen",
        5: "fifteen",
        6: "sixteen",
        7: "seventeen",
        8: "eighteen",
        9: "nineteen",
    },
}

# Accepts an integer between 0 - 999
#
# Returns the english words for that number
def intToWord(number):
    if (number < 0) or (number > 999):
        raise ValueError(f"Cannot convert {number} to English; only 0-999 is allowed!")

    words = ""

    if number == 0:
        return words_dicts["singles"][number]

    # Get digits
    hundreds = number // 100
    tens = (number%100) // 10
    singles = number%10

    if hundreds > 0:
        words = " ".join((words, words_dicts["singles"][hundreds], "hundred"))
    # If we have teens:
    if tens == 1:
        words = " ".join((words, words_dicts["teens"][singles]))
    elif tens > 1:
            words = " ".join((words, words_dicts["tens"][tens]))
            if singles > 0:
                words = "-".join((words, words_dicts["singles"][singles]))
    elif singles > 0:
        words = " ".join((words, words_dicts["singles"][singles]))

    words = words.strip()
    return str(words)

# Accepts a string representing a positive number, up to 2 decimal precision, and no larger than the largest range.
# Input is restricted as:
# - Number must be positive
# - Number must be smaller than the largest defined Range
# - Optional "." denotes fractional dollars
# - Cents precision of 0 to 2 places is permitted
# - No non-numeric characters besides "$" and "," characters are permitted
#
# Returns a string describing the entire number
def wordify(numberstring):
    # Turn the string into a malleable decimal
    numberstring = numberstring.replace('$', '')
    numberstring = numberstring.replace(',', '')
    numberstring = numberstring.strip()

    num = Decimal(numberstring)
    if num >= ranges[0]["upper"]:
        raise ValueError(f"{numberstring} is too large for me to handle, sorry!")
    if num < 0:
        raise ValueError(f"{numberstring} must be positive, sorry!")
    if num.as_tuple().exponent < -2:
        raise ValueError(f"{numberstring} has too much precision; in 'Murka we only use 2-decimal place cents!")

    # prep wordstring
    wordstring = ""

    for r in ranges:
        # find the piece for this range
        piece = (num % r["upper"])//r["lower"]

        # If this piece is nothing, and it's not mandatory, ignore it and go to the next
        if not (piece or r["mandatory"]):
            continue

        # Include "and" if:
        # - we already have at least 1 piece,
        # - the amount is > 0
        # - and this is the last piece
        if (len(wordstring)>0) and (num % r["lower"] == 0) and (piece):
            wordstring = " ".join([wordstring, "and"])

        # prepare the piece name
        if r["plural"] and piece != 1:
            piece_label = r["name"] + "s"
        else:
            piece_label = r["name"]

        # add the piece if:
        # - The value is >0, or
        # - this is the first piece
        if piece or (len(wordstring) < 1):
            words = intToWord(piece)
            wordstring = " ".join([wordstring, words, piece_label]).strip()
        # Otherwise, we only need the label
        else:
            wordstring = " ".join([wordstring, piece_label]).strip()
    return wordstring


# Brilliant comprehensive tests
def test_1():
    assert wordify("$1,234.56") == "one thousand two hundred thirty-four dollars and fifty-six cents"
def test_2():
    assert wordify('0') == "zero dollars"
def test_3():
    assert wordify('0.33') == "zero dollars and thirty-three cents"
def test_4():
    assert wordify('.01') == "zero dollars and one cent"
def test_4():
    assert wordify('1.00') == "one dollar"
def test_5():
    assert wordify('15') == "fifteen dollars"
def test_6():
    assert wordify('9000000') == "nine million dollars"
def test_7():
    assert wordify('1,000,000.01') == "one million dollars and one cent"
def test_8():
    assert wordify('1.1') == "one dollar and ten cents"
def test_9():
    assert wordify('$520.19') == "five hundred twenty dollars and nineteen cents"
# We're all about positivity at GQAssurance
def test_e1():
    with pytest.raises(ValueError):
        wordify("-3")
# Only numbers allowed!
def test_e2():
    with pytest.raises(InvalidOperation):
        wordify("3-fiddy")
# Too expensive for this demo
def test_e3():
    with pytest.raises(ValueError):
        wordify("$1000000000")
# Nobody has time for bankers precision these days.
def test_e4():
    with pytest.raises(ValueError):
        wordify('10.123')
