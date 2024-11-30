package duncan

import (
	"net/http"

	"github.com/gorilla/mux"
)

type Router struct {
	r *mux.Router
}

// TODO look into the http.handler interface, I do not like passing this functions up and dan like this 

func (this Router) GET(pattern string, handler func(res http.ResponseWriter, req *http.Request)) { 
  this.r.HandleFunc(pattern, handler).Methods("GET")
}

func (this Router) POST(pattern string, handler func(res http.ResponseWriter, req *http.Request)) {
	this.r.HandleFunc(pattern, handler).Methods("POST")
}
func (this Router) PUT(pattern string, handler func(res http.ResponseWriter, req *http.Request)) {
	this.r.HandleFunc(pattern, handler).Methods("PUT")
}
func (this Router) DELETE(pattern string, handler func(res http.ResponseWriter, req *http.Request)) {
	this.r.HandleFunc(pattern, handler).Methods("DELETE")
}
func (this Router) AddMethod(request_method []string, pattern string, handler func(res http.ResponseWriter, req *http.Request))  {
  this.r.HandleFunc(pattern, handler).Methods(request_method...)
}

func (this *Router) GetHandler() *mux.Router {
	return this.r
}

func NewDuncanRouter() *Router {
	return &Router{r: mux.NewRouter()}
}
