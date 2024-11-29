package duncan

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

const DEFAULT_PORT = 5000
const DEFAULT_HOST = "127.0.0.1"

type Duncan struct {
	name   string
	host   string
	port   int
	server *http.Server
	router *Router
}

func (this *Duncan) Start() {
	err := this.server.ListenAndServe()
	log.Print("Server has started on : ", this.getServerAddress())
	if err != nil {
		log.Fatal("could not start server : ", err)
		return
	}
}

func (this *Duncan) Stop() {
	return
}

func (this *Duncan) getServerAddress() string {
	return fmt.Sprintf("%v:%v", this.host, this.port)
}

func (this *Duncan) AddRouter(router *Router) {
	this.router = router
}

func (this *Duncan) InitHTTPserver() {
	this.server = &http.Server{
		Handler:      this.router.r,
		Addr:         this.getServerAddress(),
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
	}
	fmt.Println(this.router.r)
}

func New() *Duncan {
	duncan_server := new(Duncan)
	duncan_server.name = "Meetups Guru"
	duncan_server.host = DEFAULT_HOST
	duncan_server.port = DEFAULT_PORT

	// add refreences here to read sever config from yml file
	return duncan_server
}
