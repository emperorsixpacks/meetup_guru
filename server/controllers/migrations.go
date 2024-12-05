package controllers

import (
	"fmt"

	"gorm.io/gorm"
)

const DSN = "host=localhost user=postgres password=12345 dbname=meetups_guru port=5432 sslmode=disable TimeZone=Africa/Lagos"

// TODO add a connecion pool

func MakeMigrations(connection *gorm.DB) {
	err := connection.AutoMigrate(&user{})
	if err != nil {
		fmt.Println("Could not run migrations")
	}

}
