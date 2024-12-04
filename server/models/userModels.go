package models

import (
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Base
	User_id      uuid.UUID `gorm:"type:uuid;primary_key"`
	FirstName    string    `form:"first_name"`
	LastName     string    `form:"last_name"`
	Username     string    `form:"username" gorm:"unique"`
	Email        string    `form:"email" gorm:"type:varchar(110);unique"`
	Passord_hash string    `form:"password"`
}

func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
	u.User_id = uuid.New()
	return
}

// look at a way of passin the current db context

func New() {
	return
}
