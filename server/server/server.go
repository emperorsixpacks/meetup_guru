package server

import (
	"fmt"
	"html/template"
	"io/fs"
	"net/http"
	"os"
	"path/filepath"
	"strings"

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

func findAndParseTemplates(rootDir string) (*template.Template, error) {
	cleanRoot := filepath.Clean(rootDir)
	pfx := len(cleanRoot) + 1 // I do not know what this does
	rootTemplate := template.New("")
	err := filepath.Walk(cleanRoot, func(path string, info fs.FileInfo, err error) error {
		if !info.IsDir() && strings.HasSuffix(path, ".html") {
			if err != nil {
				return err
			}
			file, err2 := os.ReadFile(path)
			if err2 != nil {
				return err2
			}
			name := path[pfx:]
			t := rootTemplate.New(name)
			_, err2 = t.Parse(string(file))
      if err2 != nil{
        return err2
      }
		}
    return nil
	})
  return rootTemplate, err
}

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
