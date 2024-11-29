package duncan

import (
	"net/http"

	"github.com/gorilla/mux"
)

type Router struct {
	r *mux.Router
}

func (this Router) GET(pattern string, handler http.HandlerFunc) http.HandlerFunc {
	return func(res http.ResponseWriter, req *http.Request) {
		if err := this.isValidRequestMethod(http.MethodPost, req); err != nil {
			RaiseHTTPError(ErrMethodNoAllowed, res)
		}
		this.r.HandleFunc(pattern, handler)
	}
}

func (this Router) POST(pattern string, handler http.HandlerFunc) http.HandlerFunc {
	return func(res http.ResponseWriter, req *http.Request) {
		if err := this.isValidRequestMethod(http.MethodPost, req); err != nil {
			RaiseHTTPError(ErrMethodNoAllowed, res)
		}
		this.r.HandleFunc(pattern, handler)
	}
}

func (this Router) isValidRequestMethod(method string, r *http.Request) error {
	if method != r.Method {
		return ErrMethodNoAllowed
	}
	return nil
}

func (this *Router) GetHandler() *mux.Router{
  return this.r
}

func NewDuncanRouter() *Router {
	return &Router{r: mux.NewRouter()}
}
