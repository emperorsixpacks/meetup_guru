package server

import (
	"meetUpGuru/m/duncan"
	"net/http"
)

// Add the base router here, can import sub routes from other routers, they should have teh same interface, so that we can easily add them here, so in the other routers we ill just do Router.NewRouter(), then here, we can do douter.add_sub_router()
var (
  DuncanServer = duncan.Defualt()
  DuncanRouter = duncan.NewRouter()
)

func homePagehandler(res http.ResponseWriter, req *http.Request) {
}
func Run() {
  DuncanServer.AddRouter(DuncanRouter)
	// this function is what we will use to run the server based
	// on what we have created
}
