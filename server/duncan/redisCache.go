package duncan

import (
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
)

var ctx = context.Background() // I do not know, should I put this in the struct
// TODO look into making this a singleton
type RedisClient struct {
	rdb *redis.Client
}

// this should return `json:""`
func (this RedisClient) Get(key string)  {
  // NOTE this works
	val, err := this.rdb.JSONGet(ctx, key).Expanded()
	if err != nil {
		panic(err)
	}
	fmt.Println(val)
}

// this should get json
func (this RedisClient) Set(key string, value interface{}) {}

func NewRedisclient(conn RedisConnetion) *RedisClient {
	options := &redis.Options{
		Addr:     conn.Addr,
		Password: conn.Password,
		DB:       conn.DB,
	}
	client := redis.NewClient(options)
	return &RedisClient{rdb: client}
}
