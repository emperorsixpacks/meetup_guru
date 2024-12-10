package duncan

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/redis/go-redis/v9"
)

var ctx = context.Background() // I do not know, should I put this in the struct
// TODO look into making this a singleton
type RedisClient struct {
	rdb *redis.Client
}

// TODO try to make this simpler
func (this RedisClient) GetJSON(k string, o interface{}) error {
	// NOTE this works
	val, err := this.rdb.JSONGet(ctx, k).Result()
	if err != nil {
		return err
	}
	if err = json.Unmarshal([]byte(val), o); err != nil {
		return err
	}

	return nil
}

// this should get json
func (this RedisClient) SetJSON(key string, value interface{}) error {
	val, err := json.Marshal(value)
	if err != nil {
		return err
	}
	err = this.rdb.JSONSet(ctx, key,"$", val).Err()
	if err != nil {
		return err
	}
	return nil
}
func (this RedisClient) DeleteJSON(key string, value interface{}) {}
func (this RedisClient) UpdateJSON(key string, value interface{}) {}

// this should be private, and later, we should have only getconnection, var, should com from duncan config
func NewRedisclient(conn RedisConnetion) (*RedisClient, error) {
	newClient := new(RedisClient)
	options := &redis.Options{
		Addr:     conn.Addr,
		Password: conn.Password,
		DB:       conn.DB,
	}
	client := redis.NewClient(options)
	err := client.Ping(ctx).Err()
	if err != nil {
		message := fmt.Sprintf("could not connect on %s \n%v", conn.Addr, err)
		fmt.Println(message)
		return nil, err
	}
	newClient.rdb = client
	return newClient, nil
}
