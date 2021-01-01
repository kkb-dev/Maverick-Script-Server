# Maverick-Script-Server

Django based server.
Creates interface that uses User AD to login and interact with SecureCRT scripting method.

## Scripts 
- Create SSID
  * Checks SQL server for current shows. 
  * SSID Name, SSID Nickname
  * SSID Password 
  * VLAN
  
- Remove SSID
- Whitelist MAC
- Remove MAC

## Inventory Management
- Incomplete

## Auditing
- User actions recorded in remote SQL Server controlled by system administrators. 

## Security
- Only accessible on admin VLAN and AD with access to SecureCRT 
