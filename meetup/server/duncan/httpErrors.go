package duncan

import (
	"errors"
	"net/http"
)

var (
	errCouldnotStartServer = errors.New("Could not start http server") // how to pass arguments to the error
  ErrMethodNoAllowed = errors.New("Method not allowed")
)

type methodNotAllowed struct {
	code int
	err  error
}

func (this methodNotAllowed) Error() string {
	return this.err.Error()
}

func newMethodNotAllowed() *methodNotAllowed {
	status_code := http.StatusForbidden
  err := ErrMethodNoAllowed
	return &methodNotAllowed{code: status_code, err: err}

}
func HttpErrMethodNoAllowed(res http.ResponseWriter) {
	e := newMethodNotAllowed()
  http.Error(res, e.Error(), e.code)
}
