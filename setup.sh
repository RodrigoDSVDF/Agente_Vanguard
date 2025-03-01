mkdir -p ~/.streamlit/

cat <<EOL > ~/.streamlit/config.toml
[server]
headless = true
port = $PORT
enableCORS = false
EOL


