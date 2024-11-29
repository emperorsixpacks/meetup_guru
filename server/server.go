package main

import (
  "net/http"
	"meetUpGuru/m/duncan"
)

func main() {
  router := duncan.NewDuncanRouter()
  router.GET("/", func(w http.ResponseWriter, r *http.Request) {
    msg := "Hello world"
    w.Write([]byte(msg))
  })
}
