# An implementation of proof of work algorithm. This algorithm was used in block chain to prevent Distributed Denial of Service Attacks.

Steps to build solution
-----------------------------
1. From the TORRE_WORK main folder, go to the Torr_Server folder. Build the server by using the docker command.
cd Torr_Server
docker build -t torre_server .

2. From the TORRE_WORK main folder, go to the Torr_Client folder. Build the client using the docker command

docker build -t torre_client .

3. Run the torre server using the following command
docker run --network host torre_server:latest

4. Use the docker ps command to verify that the server is running. Then run the torre client using the following command
docker run --network host torre_client:latest

I have tested these steps on a Windows 10 host running Docker Desktop.