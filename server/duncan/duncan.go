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
	log.Print("Starting Duncan Server")
	this.initHTTPserver()
	log.Print("Server has started on : ", this.getServerAddress())
	err := this.server.ListenAndServe()
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

// return a new html struct
func (this Duncan) RenderHtml(name string, data any) {
}

func (this *Duncan) initHTTPserver() {
	this.server = &http.Server{
		Handler:      this.router.r,
		Addr:         this.getServerAddress(),
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
	}
}

func LoadfromConfig(pathToconfig string) {
}

func Defualt() *Duncan {
	return &Duncan{
		name: "MeetUps Guru",
		host: DEFAULT_HOST,
		port: DEFAULT_PORT,
	}
}

// TODO do not know if it will work, but how about using factory here
