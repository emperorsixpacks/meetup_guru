package controllers

import (
	"errors"
	"fmt"
	"os"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var baseDB *gorm.DB

type Base struct {
	CreatedAt time.Time
	UpdatedAt time.Time // in the documentation, they used an int64, I wonder why
	Updated   int64     `gorm:"autoUpdateTime:nano"`
	Created   int64     `gorm:"autoCreateTime"`
}

type Connection interface {
	GetConnectionName() string
	ConnectionString() string
}

func NewConnection(conn ...Connection) error {
	if baseDB == nil {
		if len(conn) == 0 {
			return errors.New("Could not establish connection")
		}
		err := newConnection(conn[0])
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
	}
	return nil
}

func newConnection(conn Connection) error {
	// TODO when we make this largers, we can add switch
	if conn.GetConnectionName() == "postgres" {
		db, err := newPostgresConnection(conn)
		if err != nil {
			return err
		}
		baseDB = db
    return nil
	}
	return errors.New("Could not create connection")
}

func newPostgresConnection(conn Connection) (*gorm.DB, error) {
	db, err := gorm.Open(postgres.New(postgres.Config{
		DSN:                  conn.ConnectionString(),
		PreferSimpleProtocol: true, // disables implicit prepared statement usage
	}), &gorm.Config{}) // direct from the docs
	if err != nil {
		return nil, err
	}
	return db, nil
}

// TODO add other connections for other types of connections
// TODO do we need only one connection