package models

import (
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type UserSchema struct {
	Base
	FirstName string `form:"first_name" json:"first_name"`
	LastName  string `form:"last_name" json:"last_name"`
	Username  string `form:"username" gorm:"unique" json:"username"`
	Email     string `form:"email" gorm:"type:varchar(110);unique" json:"email"`
	password  string
}

func (this *UserSchema) SetPassword(password string) {
	this.password = password
}

type User struct {
	gorm.Model
	UserSchema
  User_id      uuid.UUID `gorm:"type:uuid;primary_key" json:"user_id"`
	Passord_hash string    `form:"password"`
}

func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
	u.User_id = uuid.New()
	u.Passord_hash = u.password
	return
}

func (u *UserSchema) FullName() string {
	full_name := fmt.Sprintf("%v %v", u.FirstName, u.LastName)
	return full_name

}
