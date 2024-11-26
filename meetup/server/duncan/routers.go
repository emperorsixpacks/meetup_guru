package duncan

import (
	"net/http"
)

type Router struct {
  duncan *duncan
  routes []Route
}

type Route struct{
}

func (this Route) GET(pattern string, handler http.HandlerFunc) http.HandlerFunc {
	return func(res http.ResponseWriter, req *http.Request) {
		_, err := this.isValidRequestMethod(http.MethodGet, req)
		if err != nil {
			HttpErrMethodNoAllowed(res)
		}
		http.HandleFunc(pattern, handler)
	}
}

func (this Route) POST(pattern string, handler http.HandlerFunc) http.HandlerFunc {
	return func(res http.ResponseWriter, req *http.Request) {
		_, err := this.isValidRequestMethod(http.MethodPost, req)
		if err != nil {
			HttpErrMethodNoAllowed(res)
		}
		http.HandleFunc(pattern, handler)
	}
}

func (this Route) isValidRequestMethod(method string, r *http.Request) (bool, error) {
	if method != r.Method {
		return false, ErrMethodNoAllowed
	}
	return true, nil
}
