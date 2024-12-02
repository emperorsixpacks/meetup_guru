package duncan

import (
	"os"
	"io/fs"
	"path/filepath"
	"strings"
	"html/template"
	"net/http"
)

// Define how we want our html render to look like
// Be able to load temples from a directory
// Be able to load a single template
// Be able to pass arguments, using structs
// Be able to call a Render method to send the new html to the page

// Based off the HTML struct from gin
type HTML struct {
	Name     string
	Data     any
	Template *template.Template
}

func (this HTML) Render(w http.ResponseWriter) error {
	return this.Template.ExecuteTemplate(w, this.Name, this.Data)

}

func findAndParseTemplates(rootDir string) (*template.Template, error) {
	cleanRoot := filepath.Clean(rootDir)
	pfx := len(cleanRoot) + 1 // The length of rootDir path
	rootTemplate := template.New("")
	err := filepath.Walk(cleanRoot, func(path string, info fs.FileInfo, err error) error {
    // Here we transverse through the dir looking for .html files
		if !info.IsDir() && strings.HasSuffix(path, ".html") {
      // We found a .html file
			if err != nil {
				return err
			}
			file, err2 := os.ReadFile(path)
      // Reading the html file contents
			if err2 != nil {
				return err2
			}
			name := path[pfx:] // Retriving the template name, after the last index of cleanRoot, meanig after "/"
			t := rootTemplate.New(name)
      // Something funny happens here, we parse the html string directly
			_, err2 = t.Parse(string(file))
      if err2 != nil{
        return err2
      }
		}
    return nil
	})
  return rootTemplate, err
}



// Now we need to create functions and methods to load the passd html
