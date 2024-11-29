package main

import (
	"meetUpGuru/m/duncan"
	"net/http"
)

func main() {
	router := duncan.NewDuncanRouter()
	router.GET("/a", func(w http.ResponseWriter, r *http.Request) {
		msg := "Hello world"
		w.Write([]byte(msg))
	})
  srv := http.Server{
    Addr: "localhost:5000",
    Handler: router.GetHandler(),
  }
  srv.ListenAndServe()
}
