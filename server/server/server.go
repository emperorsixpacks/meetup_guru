package server

import (
	"fmt"
	"meetUpGuru/m/duncan"
	"net/http"
)

type Person struct {
	Name string
}

// Add the base router here, can import sub routes from other routers, they should have teh same interface, so that we can easily add them here, so in the other routers we ill just do Router.NewRouter(), then here, we can do douter.add_sub_router()
var (
	DuncanServer = duncan.Defualt()
	DuncanRouter = duncan.NewRouter()
)

// we wil have to write a separate function to load all the templates
// TODO return a 500 then log message for template errors
// TODO I preferethis approach to panic and stoping the excution

func homePagehandler(res http.ResponseWriter, req *http.Request) {
	// need to fix put it in a smaller method
	err := DuncanServer.RenderHtml(res, "home.html", Person{
		Name: "Andrew",
	})
	if err != nil {
		fmt.Println(err)
		return
	}
}
func Run() {
	DuncanRouter.GET("/", homePagehandler)
	DuncanServer.AddRouter(DuncanRouter)
	DuncanServer.LoadTemplates("../public/serverTemplates")
	DuncanServer.Start()
	// this function is what we will use to run the server based
	// on what we have created
}
