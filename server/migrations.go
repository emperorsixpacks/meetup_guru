package main

import (
	"fmt"
	"meetUpGuru/m/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

const DSN = "host=localhost user=postgres password=12345 dbname=meetups_guru port=5432 sslmode=disable TimeZone=Africa/Lagos"
// TODO add a connecion pool 
func main() {
	db, err := gorm.Open(postgres.New(postgres.Config{
		DSN:                  DSN,
		PreferSimpleProtocol: true,
	}), &gorm.Config{})
	if err != nil {
		err_message := fmt.Sprintf("Could not open database %v", err)
		panic(err_message)
	}
	err = db.AutoMigrate(&models.User{})
	if err != nil {
		fmt.Println("Could not run migrations")
	}

}
