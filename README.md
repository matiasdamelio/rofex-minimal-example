# Ejemplo mínimo de conexión a ROFEX
## Ambiente de desarrollo: reMarkets

### Variables a modificar:
-   En ./conf/rofex.cfg
    -   SenderCompID=```USER``` 
    -   SocketConnectPort=```PORT``` 
-   En ./conf/config.ini
    -   sendercompid = ```USER```
    -   password = ```PASSWORD```
    -   account = ```ACCOUNT```

```
La variable PORT tiene que ser la que se setea en la configuración del Stunnel.
```

### Configuración de Stunnel
```
[rofex-dev]
client=yes
accept=localhost:PORT
connect=fix.remarkets.primary.com.ar:9876
```