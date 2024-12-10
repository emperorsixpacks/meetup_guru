package main

import "meetUpGuru/m/duncan"

/*
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
*/

func main(){
  
  _ = duncan.NewRedisclient(duncan.RedisConnetion{

    Addr: "localhost:9379",
    Password: "",
    DB: 0,
  })
}
// TODO why is this slow
// TODO learn how to ans why we use github to import packages
