package controllers

import (

	"gorm.io/gorm"
)

type Controller struct {
	connection *gorm.DB
}

func (this *Controller) GetConnection() *gorm.DB {
	return this.connection
}

func (this *Controller) CreateUserController(user *UserSchema) {
  this.connection.Create(user)
}
