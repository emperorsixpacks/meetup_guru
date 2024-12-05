package server

import (
	"fmt"
	"meetUpGuru/m/duncan"
	"os"

	"gorm.io/gorm"
)

// Add the base router here, can import sub routes from other routers, they should have teh same interface, so that we can easily add them here, so in the other routers we ill just do Router.NewRouter(), then here, we can do douter.add_sub_router()
var (
	DuncanServer = duncan.Defualt()
	DuncanRouter = duncan.NewRouter()
	PGConnection = PostgresConnection{
		host:     "localhost",
		port:     "5432",
		user:     "postgres",
		password: "12345",
		database: "meetups_guru",
		debug:    true,
	}
	BaseDB = GetConnection()
)

func GetConnection() *gorm.DB {
	baseDB, err := getConnection(&PGConnection)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	return baseDB
}

func Run() {
	DuncanServer.LoadTemplates("../public/serverTemplates")
	DuncanServer.AddRouter(DuncanRouter)
	DuncanServer.Start()
}

// TODO return a 500 then log message for template errors
// TODO I preferethis approach to panic and stoping the excution
// TODO conneectin params should come from an env for from duncan connection
