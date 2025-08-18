#BlockChain File Storage

##Commands to run

Remove the -d(detached) if you wan to see what happens for each process
Start the PostgreSQL container
'''bash
sudo docker run -d \
  --name blockchain-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=blockchain_db \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:14
'''

Build the blockchain from the code
'''bash
sudo docker build -t blockchain-app .
'''
Start running the container

'''bash
sudo docker run -d \
  --name blockchain-app \
  --link blockchain-db:db \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://postgres:password@db:5432/blockchain_db \
  -v $(pwd)/uploads:/app/uploads \
  blockchain-app
'''

Delete all running services
'''bash
sudo docker rm -f $(sudo docker ps -aq)
'''
