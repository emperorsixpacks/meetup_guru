package controllers

import (
	"meetUpGuru/m/models"
	"meetUpGuru/m/server"
)

func CreateUserController(new_user models.UserSchema) {
	new_db_user := &models.User{UserSchema: new_user}
	server.BaseDB.Create(new_db_user)

}
