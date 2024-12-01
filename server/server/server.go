package server

import (
	"meetUpGuru/m/duncan"
	"net/http"
)

var (
  DuncanServer = duncan.Defualt()
  DuncanRouter = duncan.NewDuncanRouter()
)

func homePagehandler(res http.ResponseWriter, req *http.Request) {}

func Run() {
  DuncanServer.AddRouter(DuncanRouter)
	// this function is what we will use to run the server based
	// on what we have created
}
