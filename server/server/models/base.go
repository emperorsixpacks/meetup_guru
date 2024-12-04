package models

import (
	"time"

)

type Base struct{
  CreatedAt  int64 `gorm:"autoCreateTime"`
  UpdatedAt time.Time
}
