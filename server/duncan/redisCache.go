package duncan

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"

	"github.com/redis/go-redis/v9"
)

var ctx = context.Background() // I do not know, should I put this in the struct
// TODO look into making this a singleton
type RedisClient struct {
	rdb *redis.Client
}

func (this *RedisClient) clearDB() error {
	if err := this.rdb.FlushAll(ctx).Err(); err != nil {
		return err
	}
  return nil
}

// TODO try to make this simpler
func (this RedisClient) GetJSON(k string, o interface{}) error {
	// NOTE this works
	val, err := this.getJSON(k)
	str_val, ok := val.(string) // TODO read on how this guy works
	if !ok {
		return errors.New("Internal error")
	}
	if err = json.Unmarshal([]byte(str_val), o); err != nil {
		return err
	}

	return nil
}

func (this RedisClient) getJSON(k string, inner_key ...string) (interface{}, error) {
	if len(inner_key) == 0 {
		inner_key[0] = "$"
	}
	val, err := this.rdb.JSONGet(ctx, k, inner_key[0]).Result()
	if err != nil {
		return nil, err
	}
	return val, nil
}

// we can even expand this further to get the data in a nestad json
// let us go ahead now and create some hidden methods to handle this
func (this RedisClient) SetJSON(key string, value interface{}) error {
	if err := this.setJSON(key, value); err != nil {
		return err
	}

	return nil
}

func (this RedisClient) setJSON(key string, value interface{}, inner_key ...string) error {
	val, err := json.Marshal(value)
	if err != nil {
		return err
	}
	if len(inner_key) == 0 {
		inner_key[0] = "$"
	}
	err = this.rdb.JSONSet(ctx, key, inner_key[0], val).Err()
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
