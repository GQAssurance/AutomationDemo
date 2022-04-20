package main

import "testing"

func TestWordifyBasic(t *testing.T) {
	input := "100"
	result := wordify(input)
	expected := "one hundred dollars"

	if result != expected {
		t.Errorf("For input '%s' the result was '%s' and we expected '%s'", input, result, expected)
	}
}

func TestWordifyZero(t *testing.T) {
	input := "0"
	result := wordify(input)
	expected := "zero dollars"

	if result != expected {
		t.Errorf("For input '%s' the result was '%s' and we expected '%s'", input, result, expected)
	}
}

func TestWordifyCents(t *testing.T) {
	input := "10.15"
	result := wordify(input)
	expected := "ten dollars and fifteen cents"

	if result != expected {
		t.Errorf("For input '%s' the result was '%s' and we expected '%s'", input, result, expected)
	}
}

func TestWordifyLarge(t *testing.T) {
	input := "175505670.99"
	result := wordify(input)
	expected := "one hundred seventy-five million, five hundred five thousand, six hundred seventy dollars and ninety-nine cents"

	if result != expected {
		t.Errorf("For input '%s' the result was '%s' and we expected '%s'", input, result, expected)
	}
}

func TestWordifySingles(t *testing.T) {
	input := "1.01"
	result := wordify(input)
	expected := "one dollar and one cent"

	if result != expected {
		t.Errorf("For input '%s' the result was '%s' and we expected '%s'", input, result, expected)
	}
}

func TestWordifyCentsOnly(t *testing.T) {
	input := ".11"
	result := wordify(input)
	expected := "zero dollars and eleven cents"

	if result != expected {
		t.Errorf("For input '%s' the result was '%s' and we expected '%s'", input, result, expected)
	}
}
