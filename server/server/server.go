package server

import (
	"fmt"
	"html/template"
	"net/http"
	"meetUpGuru/m/duncan"
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
func LoadFromGlobal() (*template.Template, error) {
  parsed_template, err := findAndParseTemplates("../public/serverTemplates")
	//parsed_template, err := template.New("").ParseGlob("/home/adavid/Documents/GitHub/meetup_guru/public/**/*")
	if err != nil {
		return nil, err
	}
	return parsed_template, nil
}

func homePagehandler(res http.ResponseWriter, req *http.Request) {
	parsed_template, err := LoadFromGlobal()
	if err != nil {
		fmt.Println("Could not load template", err)
		return
	}
	err = parsed_template.ExecuteTemplate(res, "pages/page1.html", Person{
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
	DuncanServer.Start()
	// this function is what we will use to run the server based
	// on what we have created
}
