package main 

import (
  "gorm.io/driver/postgres"
  "gorm.io/gorm"
)
func main()  {
  dsn := "host=localhost user=gorm password=gorm dbname=gorm port=9920 sslmode=disable TimeZone=Asia/Shanghai"
  conns, err := gorm.Open(postgres.Open(dsn))
}
