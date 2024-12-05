package server 

import (
	"meetUpGuru/m/controllers"
	"meetUpGuru/m/duncan"
)

// Add the base router here, can import sub routes from other routers, they should have teh same interface, so that we can easily add them here, so in the other routers we ill just do Router.NewRouter(), then here, we can do douter.add_sub_router()
var (
	DuncanServer = duncan.Defualt()
	DuncanRouter = duncan.NewRouter()
	Connection   = PostgresConnection{
		host:     "localhost",
		port:     "5432",
		user:     "postgres",
		password: "12345",
		database: "meetups_guru",
		debug:    true,
	}
	_ = controllers.NewConnection(&Connection)
)

func Run(){
  DuncanServer.LoadTemplates("../public/serverTemplates")
  DuncanServer.AddRouter(DuncanRouter)
  DuncanServer.Start()
}

// TODO return a 500 then log message for template errors
// TODO I preferethis approach to panic and stoping the excution
