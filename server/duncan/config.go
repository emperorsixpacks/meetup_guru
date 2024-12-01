package duncan

type Connection interface {
	ConstructFromParams(host string, port string, password string) string
	ConstructFromUrl(url string) string
}

type AppConfig struct {
	name string
	host string
	port string
}

type ConnnectionConfig struct {
	Connections []Connection
}

type DuncanConfig struct {
	app         AppConfig
	connections ConnnectionConfig
}
