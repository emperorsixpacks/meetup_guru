package duncan

type ConnnectionConfig struct {
	Name     string `yaml:"name"`
	Host     string `yaml:"host"`
	Port     string `yaml:"port"`
	password string `yaml:"password"`
}

type DatabaseConfig struct {
	Master ConnnectionConfig `yaml:"master"`
	Slave  ConnnectionConfig `yaml:"slave"`
}

type Conections struct {
	Redis    ConnnectionConfig `yaml:"redis"`
	Database DatabaseConfig    `yaml:"database"`
}

type DuncanConfig struct {
	app         ConnnectionConfig
	connections ConnnectionConfig
}
