server {
    listen 80;
    listen [::]:80;

    server_name bfactors.ovmwan.com;
    client_max_body_size 300M;

    location / {
        proxy_pass http://localhost:5001;
    }

    location /socket {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_connect_timeout       600;
        proxy_send_timeout          600;
        proxy_read_timeout          600;
        send_timeout                600;
    }
}
