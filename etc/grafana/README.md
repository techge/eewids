# Grafana Config files

These files are included/loaded into the Grafana container (at least if the [docker-compose.yml](/docker-compose.yml) is used).

If you like to automatically add a specific datasource on startup, you most likely wants to look into [provisioning/datasources](provisioning/datasources) and wants to read [Grafana's docu](http://docs.grafana.org/administration/provisioning/#datasources) about it.

Furthermore, you can save your previously created dashboards in the [dashboards folder](dashboards) as json file (there is an export function in Grafana's web interface). After saving it there it will be loaded into Grafana on every start as well.

## The Data Folder

Since Version 5.1 Grafana is started as user grafana (with id 472) instead of root. While starting the application with user rights is surely a good idea, this has a downside in how Grafana handles folder bindings (as used in the [docker-compose.yml](/docker-compose.yml)). To use persistent storage - saved in folder "data" - Eewids will just change the owner rights of the folder "date/grafana" to the user id of the grafana user (472, see above). This is done automatically by the [simple start script](/doc/getting-started.md), but has to be keept in mind in case you adapt the setup to your own infrastructure.
