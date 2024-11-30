package duncan

import (
	"net/http"

	"github.com/gorilla/mux"
)

type Router struct {
	r *mux.Router
}

func (this Router) GET(pattern string, handler func(res http.ResponseWriter, req *http.Request)) {
	this.r.HandleFunc(pattern, handler).Methods("GET")
}
func (this Router) POST(pattern string, handler func(res http.ResponseWriter, req *http.Request)) {
	this.r.HandleFunc(pattern, handler).Methods("POST")
}

// Add an add route method and pass the verb explicity by default
func (this Router) isValidRequestMethod(method string, r *http.Request) error {
	if method != r.Method {
		return ErrMethodNoAllowed
	}
	return nil
}

func (this *Router) GetHandler() *mux.Router {
	return this.r
}

func NewDuncanRouter() *Router {
	return &Router{r: mux.NewRouter()}
}
