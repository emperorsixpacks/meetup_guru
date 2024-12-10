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
func (this RedisClient) Get(key string, output interface{}) (interface{}, error) {
	// NOTE this works
	_, err := this.rdb.JSONGet(ctx, key).Expanded()
	if err != nil {
		return nil, err
	}
	return nil, nil
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
  err := client.Ping(ctx).Err()
  if err != nil{
    message :=fmt.Sprintf("could not connect on %s \n%v", conn.Addr, err)
    fmt.Println(message)
    return nil
  }
	return &RedisClient{rdb: client}
}
