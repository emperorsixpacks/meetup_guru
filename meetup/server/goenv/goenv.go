package goenv

import (
	"os"
)



func isValidFileExtention(filename string) (bool, error){}

func openFile(filePath string) (*os.File, error){
  file, err := os.Stat(filePath)
  if err != nil{
    if os.IsNotExist(err){
      return nil, err
    }
  } 
  if file.IsDir(){
    return nil, ErrNotaValidEnvFile 
  }
}

func readFile(filename string) ([]byte, error){
  file, err := os.Open(filename) // Add a check here to check if the file is valid
  file.Close()
  if err != nil{
    return nil, err 
  }
  data, err := toBytes(file)
  if err != nil{
    return nil, err
  }
  return data, nil
}
