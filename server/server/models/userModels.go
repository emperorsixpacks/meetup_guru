package models

import "gorm.io/gorm"

type User struct {
	gorm.Model
	Base
	FirstName string `form:"first_name"`
	LastName  string `form:"last_name"`
	Username  string `form:"username" gorm:"unique"`
	Email     string `form:"email" gorm:"type:varchar(110);unique"`
	Passord_hash  string `form:"password"`
}
