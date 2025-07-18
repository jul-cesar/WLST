import sys
from java.io import FileInputStream
from java.util import Properties

# Cargar propiedades desde archivo
propFile = sys.argv[1]
props = Properties()
props.load(FileInputStream(propFile))

# Leer propiedades
domain_name = props.get("DOMAIN_NAME")
admin_port = int(props.get("ADMIN_PORT"))
admin_password = props.get("ADMIN_PASSWORD")
soa_server_name = props.get("SOA_SERVER_NAME")
soa_port = int(props.get("SOA_PORT"))
nm_address = props.get("NM_LISTEN_ADDRESS")
nm_port = int(props.get("NM_PORT"))

# Cargar plantilla base
readTemplate("C:/Oracle/Middleware/Oracle_Home/wlserver/common/templates/wls/wls.jar")

# Configurar AdminServer
cd('/Servers/AdminServer')
set('ListenAddress', 'localhost')
set('ListenPort', admin_port)

# Configurar contraseña del usuario weblogic
cd('/Security/base_domain/User/weblogic')
cmo.setPassword(admin_password)

# Crear SOA Server
cd('/')
create(soa_server_name, 'Server')
cd('/Servers/' + soa_server_name)
set('ListenAddress', 'localhost')
set('ListenPort', soa_port)

# Configurar NodeManager
cd('/')
create('MachineScript', 'Machine')
cd('/Machines/MachineScript')
create('NodeManager', 'NodeManager')
cd('/Machines/MachineScript/NodeManager/NodeManager')
set('ListenAddress', nm_address)
set('ListenPort', nm_port)

# Guardar dominio
setOption('OverwriteDomain', 'true')
writeDomain('C:/Oracle/Middleware/Oracle_Home/user_projects/domains/' + domain_name)
closeTemplate()

print('Domain created successfully: ' + domain_name)
