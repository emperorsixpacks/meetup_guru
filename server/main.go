package main

import (
	"fmt"
	"meetUpGuru/m/server"
	"os"
)

func main() {
	switch os.Args[1] {
	case "run":
		server.Run()
	case "migrate":
		fmt.Println("Runnig migrations")
		server.MakeMigrations()
		fmt.Println("Done runnig migrations")
	default:
		fmt.Println("No argument provided")
	}
}

// TODO why is this slow
