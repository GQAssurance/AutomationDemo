package main

import (
	"fmt"
	"os"
)

func main() {
	input := getInputString()
	wordString := wordify(input)
	fmt.Println(wordString)
}

func getInputString() string {
	if len(os.Args) < 2 {
		fmt.Println("You need a number!")
		os.Exit(1)
	}
	return os.Args[1]
}
