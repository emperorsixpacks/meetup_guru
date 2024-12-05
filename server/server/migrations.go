package server

import (
	"fmt"
	"meetUpGuru/m/models"
)

// TODO add a connecion pool
func MakeMigrations() {

	err := BaseDB.AutoMigrate(&models.User{})
	if err != nil {
		fmt.Println("Could not run migrations")
		fmt.Print(err)
	}

}
