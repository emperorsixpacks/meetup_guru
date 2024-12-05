package main

import (
	"fmt"
	"meetUpGuru/m/controllers"
	"meetUpGuru/m/server"
	"os"
)

func main() {
	switch os.Args[1] {
	case "run":
		server.Run()
	case "migrate":
    fmt.Println("Runnig migrations")
		controllers.MakeMigrations()
    fmt.Println("Done runnig migrations")
	default:
		fmt.Println("No argument provided")
	}
}
// TODO why is this slow
