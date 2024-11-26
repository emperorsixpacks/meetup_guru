package duncan 

import (
	"fmt"
	"log"
	"net/http"
)

const DEFAULT_PORT = 8000
const DEFAULT_HOST = "127.0.0.1"

type duncan struct{
  is_started bool
  name string
  host string
  port int
}

func (this *duncan) start(){
  err := http.ListenAndServe(this.getServerAddress(), nil)
  if err != nil{
    log.Fatal("could not start server : ", err)
    return
  }
  log.Print("Server has started on : ", this.getServerAddress())
}

func (this *duncan) stop() {
  return
}


func (this *duncan) getServerAddress() string{
  return fmt.Sprintf("%v:%v", this.host, this.port)
}
func New() *duncan{

}
