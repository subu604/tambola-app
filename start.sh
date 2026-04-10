
#!/bin/bash
apt update -y && apt install -y docker.io
service docker start || true
docker build -t tambola .
docker rm -f tambola 2>/dev/null || true
docker run -d -p 8000:8000 --name tambola tambola
echo "Open URL: https://<killercoda-url>:8000"
