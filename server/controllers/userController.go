package controllers

import (
	"meetUpGuru/m/models"
)

func CreateUserController(new_user models.UserSchema) {
	new_db_user := &models.User{UserSchema: new_user}
	baseDb.Create(new_db_user)

}
