package duncan

import "github.com/redis/go-redis/v9"

type Redis

type Redisclient struct{
  rdb *redis.Client
}

func NewredisClient(conn *RedisConnetion) *Redisclient{
  options := redis.Options{
    Addr: conn.Addr,
    Password:  conn.Password,
    DB: conn.DB, // Don't you think this is a bit repititve
    
  }
}
