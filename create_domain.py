import os
import sys

print "=== CREANDO DOMINIO SOA ==="

# Validar argumentos
if len(sys.argv) != 2:
    print "Uso: wlst.cmd create_domain.py <archivo_propiedades>"
    exit()

properties_file = sys.argv[1]
print "Cargando propiedades: " + properties_file

# Verificar que el archivo existe
if not os.path.exists(properties_file):
    print "ERROR: Archivo no encontrado: " + properties_file
    exit()

# Cargar propiedades
try:
    loadProperties(properties_file)
    print "Propiedades cargadas correctamente"
except Exception, e:
    print "ERROR cargando propiedades: " + str(e)
    exit()

# Obtener y validar propiedades
domain_name = get('domain_name')
port_base_str = get('port_base')

print "DEBUG - domain_name: " + str(domain_name)
print "DEBUG - port_base_str: " + str(port_base_str)

if domain_name is None or domain_name == '':
    print "ERROR: domain_name no encontrado en propiedades"
    exit()

if port_base_str is None or port_base_str == '':
    print "ERROR: port_base no encontrado en propiedades"
    exit()

# Convertir puerto a entero
try:
    admin_port = int(port_base_str)
    soa_port = admin_port + 2
except ValueError:
    print "ERROR: port_base debe ser un numero, recibido: " + str(port_base_str)
    exit()

print "Dominio: " + domain_name
print "Puerto Admin: " + str(admin_port)
print "Puerto SOA: " + str(soa_port)

# Rutas
oracle_home = 'C:/Oracle/Middleware/Oracle_Home'
domain_path = oracle_home + '/user_projects/domains/' + domain_name

print "Ruta dominio: " + domain_path

# Verificar plantillas
wls_template = oracle_home + '/wlserver/common/templates/wls/wls.jar'
soa_template = oracle_home + '/soa/common/templates/wls/oracle.soa_template.jar'

print "Verificando plantilla WLS: " + wls_template
if not os.path.exists(wls_template):
    print "ERROR: Plantilla WLS no encontrada: " + wls_template
    exit()

print "Verificando plantilla SOA: " + soa_template
if not os.path.exists(soa_template):
    print "ERROR: Plantilla SOA no encontrada: " + soa_template
    exit()

# Crear dominio
print "Leyendo plantillas..."
readTemplate(wls_template)
addTemplate(soa_template)

print "Configurando AdminServer..."
cd('/Security/base_domain/User/weblogic')
cmo.setPassword('Welcome123')

cd('/Server/AdminServer')
set('ListenPort', admin_port)

print "Creando SOA Server..."
cd('/')
create('soa_server1', 'Server')
cd('/Server/soa_server1')
set('ListenPort', soa_port)
setServerGroups(['SOA-MGD-SVRS'])

print "Configurando Node Manager..."
cd('/')
create('LocalMachine', 'Machine')
cd('/Machine/LocalMachine')
create('LocalMachine', 'NodeManager')
cd('NodeManager/LocalMachine')
set('ListenAddress', 'localhost')
set('NMType', 'PerDomain')

assign('Server', 'AdminServer', 'Machine', 'LocalMachine')
assign('Server', 'soa_server1', 'Machine', 'LocalMachine')

print "Guardando dominio..."
setOption('DomainName', domain_name)
setOption('OverwriteDomain', 'true')
writeDomain(domain_path)
closeTemplate()

print "=== DOMINIO CREADO EXITOSAMENTE ==="
print "Nombre: " + domain_name
print "Ruta: " + domain_path
print "AdminServer: localhost:" + str(admin_port)
print "SOA Server: localhost:" + str(soa_port)

exit()