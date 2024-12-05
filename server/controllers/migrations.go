package controllers

import (
	"fmt"
)

// TODO add a connecion pool

func MakeMigrations() {
	err := baseDB.AutoMigrate(&user{})
	if err != nil {
		fmt.Println("Could not run migrations")
	}

}
