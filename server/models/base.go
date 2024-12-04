package models

import (
	"time"
)

type Base struct {
	CreatedAt time.Time
	UpdatedAt time.Time // in the documentation, they used an int64, I wonder why
	Updated   int64     `gorm:"autoUpdateTime:nano"`
	Created   int64     `gorm:"autoCreateTime"`
}
