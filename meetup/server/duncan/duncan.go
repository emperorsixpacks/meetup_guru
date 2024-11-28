package duncan

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

const DEFAULT_PORT = 5000
const DEFAULT_HOST = "127.0.0.1"

type duncan struct {
	name   string
	host   string
	port   int
	server *http.Server
}

func (this *duncan) Start() {
	err := http.ListenAndServe(this.getServerAddress(), nil)

	log.Print("Server has started on : ", this.getServerAddress())
	if err != nil {
		log.Fatal("could not start server : ", err)
		return
	}
}

func (this *duncan) Stop() {
	return
}

func (this *duncan) getServerAddress() string {
	return fmt.Sprintf("%v:%v", this.host, this.port)
}

func initHTTPserver() *http.Server {
	return &http.Server{
		// look at adding my own mux
		Handler:      nil,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
	}

}

func New() *duncan {
	duncan_server := duncan{
		name:   "Meetups Guru",
		host:   DEFAULT_HOST,
		port:   DEFAULT_PORT,
		server: initHTTPserver(),
	}
	duncan_server.server.Addr = duncan_server.getServerAddress()

	// add refreences here to read sever config from yml file
	return &duncan_server
}
