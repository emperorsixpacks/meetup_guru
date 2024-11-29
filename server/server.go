package main

import (
	"meetUpGuru/m/duncan"
	"net/http"
)

func main() {
	d := duncan.New()
	router := duncan.NewDuncanRouter()
	router.GET("/", func(w http.ResponseWriter, r *http.Request) {
		msg := "Hello world"
		w.Write([]byte(msg))
	})
	d.AddRouter(router)
	d.InitHTTPserver()
	d.Start()
}
