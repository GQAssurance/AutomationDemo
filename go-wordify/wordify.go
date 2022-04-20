package main

import (
	"fmt"
	"math"
	"os"
	"strings"

	"github.com/shopspring/decimal"
)

type dollarRange struct {
	// What is the english word for this range?  e.g. "thousand"
	description string
	// What power of 10 does this range start?  e.g., thousand is 10^3
	startingPower int
	// Does the description get an "s" when the value is other than 1?
	pluralized bool
	// What is the value of this range?
	value int
	// Shall we include words if the value is zero?
	zero bool
	// What is the value in words?
	words string
}

func cleanInput(input string) decimal.Decimal {
	input = strings.ReplaceAll(input, "$", "")
	input = strings.ReplaceAll(input, ",", "")
	num, err := decimal.NewFromString(input)
	if err != nil {
		fmt.Println("Your input must be a number, with only periods, commas, and dollar signs allowed!")
		os.Exit(1)
	}
	maxRange := decimal.NewFromFloat(math.Pow10(9))
	if num.Cmp(maxRange) >= 0 {
		fmt.Println("Your number must be smaller than", maxRange)
		os.Exit(1)
	}
	return num
}

func setupRanges() []dollarRange {
	r := []dollarRange{}
	r = append(r, dollarRange{
		description:   "billion",
		startingPower: 9,
		pluralized:    false,
		zero:          false,
	})
	r = append(r, dollarRange{
		description:   "million",
		startingPower: 6,
		pluralized:    false,
		zero:          false,
	})
	r = append(r, dollarRange{
		description:   "thousand",
		startingPower: 3,
		pluralized:    false,
		zero:          false,
	})
	r = append(r, dollarRange{
		description:   "dollar",
		startingPower: 0,
		pluralized:    true,
		zero:          true,
	})
	r = append(r, dollarRange{
		description:   "cent",
		startingPower: -2,
		pluralized:    true,
		zero:          false,
	})
	return r
}

func getRanges(num decimal.Decimal) []dollarRange {
	ranges := setupRanges()
	for i, r := range ranges {
		// is the number larger than the bottom of the range?
		minInRange := decimal.NewFromFloat(math.Pow10(r.startingPower))
		if num.Cmp(minInRange) >= 0 {
			// extract the portion within the range
			piece := num.Div(minInRange).Truncate(0)
			ranges[i].value = int(piece.IntPart())
			num = num.Sub(piece.Mul(minInRange))
		}
	}
	return ranges
}

// convert integers up to 999 into words
func getWordsFromInt(num int) string {

	singles := map[int]string{
		1:  "one",
		2:  "two",
		3:  "three",
		4:  "four",
		5:  "five",
		6:  "six",
		7:  "seven",
		8:  "eight",
		9:  "nine",
		10: "ten",
		11: "eleven",
		12: "twelve",
		13: "thirteen",
		14: "fourteen",
		15: "fifteen",
		16: "sixteen",
		17: "seventeen",
		18: "eighteen",
		19: "nineteen",
	}

	tens := map[int]string{
		2: "twenty",
		3: "thirty",
		4: "forty",
		5: "fifty",
		6: "sixty",
		7: "seventy",
		8: "eighty",
		9: "ninety",
	}

	words := ""
	if num == 0 {
		words = "zero"
	}
	if num > 99 {
		hundredsDigit := num / 100
		words = words + singles[hundredsDigit] + " hundred"
		num = num - (hundredsDigit * 100)
		if num > 0 {
			words = words + " "
		}
	}
	if num > 19 {
		tensDigit := num / 10
		words = words + tens[tensDigit]
		num = num - (tensDigit * 10)
		if num > 0 {
			words = words + "-"
		}
	}
	if num > 0 {
		words = words + singles[num]
	}
	return words
}

func setWords(ranges []dollarRange) {
	for i, r := range ranges {
		if r.value > 0 || r.zero {
			if ranges[i].value != 1 && r.pluralized {
				r.description = r.description + "s"
			}
			ranges[i].words = getWordsFromInt(r.value) + " " + r.description
		}
	}
}

func getWordString(ranges []dollarRange) string {
	ws := ""
	for _, r := range ranges {
		if len(r.words) > 0 {
			if r.startingPower < 0 { // pennies start with 'and'
				ws = ws + " and "
			} else if len(ws) > 0 { // everything else might need to start with a comma separator
				ws = ws + ", "
			}
			ws = ws + r.words
		}
	}
	return ws
}

func wordify(inputNumber string) string {
	num := cleanInput(inputNumber)
	dollarRanges := getRanges(num)
	setWords(dollarRanges)
	return getWordString(dollarRanges)
}
