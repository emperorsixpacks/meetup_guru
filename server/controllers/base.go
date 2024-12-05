package controllers

import (
	"errors"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var baseDB *BaseDB

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

type BaseDB struct {
	db   *gorm.DB
	conn Connection
} // not to be confused with db from gorm


func GetConnection(conn ...Connection) (*gorm.DB, error) {
	if baseDB == nil {
		if len(conn) <= 0 {
			return nil, errors.New("Could not establish connection")
		}
		newConnection(conn[0])
	}
	return baseDB.db, nil
}

func newConnection(conn Connection) error {
	// TODO when we make this largers, we can add switch
	if conn.GetConnectionName() == "postgres" {
		db, err := newPostgresConnection(conn)
		if err != nil {
			return err
		}
		baseDB = &BaseDB{db: db, conn: conn}
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
