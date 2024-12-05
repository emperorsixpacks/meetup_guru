package controllers

func CreateUserController(new_user *UserSchema) {
	new_db_user := &user{UserSchema: *new_user}
	baseDB.Create(new_db_user)

}
