[Unit]
Description=A utility Discord bot for a few servers I am in.
After=network.target
Wants=network-online.target

[Service]
Restart=always
Type=simple
User=${owner}
Group=${group}
ExecStart=${poetry_path} run monty
WorkingDirectory=${monty_root}
Environment=

[Install]
WantedBy=multi-user.target
