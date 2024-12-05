package controllers

import (
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type UserSchema struct {
	Base
	User_id   uuid.UUID `gorm:"type:uuid;primary_key"`
	FirstName string    `form:"first_name"`
	LastName  string    `form:"last_name"`
	Username  string    `form:"username" gorm:"unique"`
	Email     string    `form:"email" gorm:"type:varchar(110);unique"`
	password  string
}

func (this *UserSchema) SetPassword(password string) {
	this.password = password
}

type user struct {
	gorm.Model
	user         UserSchema
	Passord_hash string `form:"password"`
}

func (u *user) BeforeCreate(tx *gorm.DB) (err error) {
	u.user.User_id = uuid.New()
	u.Passord_hash = u.user.password
	return
}

func (u *UserSchema) FullName() string {
	full_name := fmt.Sprintf("%v %v", u.FirstName, u.LastName)
	return full_name

}

// look at a way of passin the current db context

func New() {
	return
}
