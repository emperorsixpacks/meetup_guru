package main

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
)

//import "meetUpGuru/m/server"

const DATABSE_URL = "postgresql://postgres:12345@localhost:5432/meetups_guru"

func connect_to_db() {
	conn, err := pgxpool.New(context.Background(), DATABSE_URL)
  if err != nil{
    fmt.Println("could not connnect to postgrs", err)
  }
  defer conn.Close()
  fmt.Println("Connection established")
}

func main() {
  connect_to_db()
	//server.Run()
}
