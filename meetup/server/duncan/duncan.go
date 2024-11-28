package duncan 

import (
	"fmt"
	"log"
	"net/http"
)

const DEFAULT_PORT = 5000 
const DEFAULT_HOST = "127.0.0.1"

type duncan struct{
  name string
  host string
  port int
}

func (this *duncan) Start(){
  err := http.ListenAndServe(this.getServerAddress(), nil)

  log.Print("Server has started on : ", this.getServerAddress())
  if err != nil{
    log.Fatal("could not start server : ", err)
    return
  }
}

func (this *duncan) Stop() {
  return
}


func (this *duncan) getServerAddress() string{
  return fmt.Sprintf("%v:%v", this.host, this.port)
}

func New() *duncan{
  // add refreences here to read sever config from yml file
  return &duncan{
   name: "Meetups Guru",
   host: DEFAULT_HOST,
   port: DEFAULT_PORT,
 } 
}
