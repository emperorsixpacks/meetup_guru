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
		if _, err := this.isValidRequestMethod(http.MethodPost, req); err != nil {
			RaiseHTTPError(ErrMethodNoAllowed, res)
		}
		http.HandleFunc(pattern, handler)
	}
}

func (this Router) POST(pattern string, handler http.HandlerFunc) http.HandlerFunc {
	return func(res http.ResponseWriter, req *http.Request) {
		if _, err := this.isValidRequestMethod(http.MethodPost, req); err != nil {
			RaiseHTTPError(ErrMethodNoAllowed, res)
		}
		http.HandleFunc(pattern, handler)
	}
}

func (this Router) isValidRequestMethod(method string, r *http.Request) (bool, error) {
	if method != r.Method {
		return false, ErrMethodNoAllowed
	}
	return true, nil
}
