ffuf -u https://api.example.com/FUZZ -w lists/api-common.txt -mc 200,204,301,302,401,403,405 -ac -t 150 -sa -of json -o data/ffuf_api.json
