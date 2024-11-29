package duncan

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

const DEFAULT_PORT = 5000
const DEFAULT_HOST = "127.0.0.1"

type duncan struct {
	name   string
	host   string
	port   int
	server *http.Server
	router *Router
}

func (this *duncan) Start() {
	err := this.server.ListenAndServe()
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

func (this *duncan) createNewRouter() {
	this.router = &Router{r: mux.NewRouter()}
}

func (this *duncan) Router() *mux.Router {}

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
	duncan_server.server.Handler = duncan_server.createNewRouter()

	// add refreences here to read sever config from yml file
	return &duncan_server
}
