package duncan

import (
	"context"

	"github.com/redis/go-redis/v9"
)

var ctx = context.Background() // I do not know, should I put this in the struct

type RedisClient struct {
	rdb *redis.Client
}

func (this RedisClient) Get(key string) string {
	val, err := this.rdb.Get(ctx, key).Result()
	if err != nil {
		panic(err)
	}
	return val // some type convertion has to come here because we are returning a string, but we are getting json

}

func newredisclient(conn RedisConnetion) *RedisClient {
	options := &redis.Options{
		Addr:     conn.Addr,
		Password: conn.Password,
		DB:       conn.DB,
	}
	client := redis.NewClient(options)
	return &RedisClient{rdb: client}
}
