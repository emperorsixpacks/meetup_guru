package goenv

import (
	"bytes"
	"io"
)

func toBytes(src io.Reader) ([]byte, error) {
  var b bytes.Buffer 
  _, err := io.Copy(&b, src)
  if err != nil{
    return nil, err
  }
  return b.Bytes(), nil
}

func parse(src []byte){
}
