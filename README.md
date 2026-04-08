# Market News Monitor

A real-time crypto market monitoring agent built with CrewAI. It detects BTC/EUR price movements exceeding 2% over 5 minutes, searches for related news, and sends a WhatsApp alert via Twilio.

---

## Prerequisites

### 1. Install Python 3.12 and venv

```bash
sudo apt update && sudo apt install -y python3.12 python3.12-venv
```

### 2. Clone the repository

```bash
git clone https://github.com/viviancpy/market-news-monitor.git
cd market-news-monitor
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
nano .env
```

Fill in your credentials:

```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
MY_PHONE_NUMBER=whatsapp:+your_number
STARROCKS_HOST=your_starrocks_host_ip
STARROCKS_USER=your_db_user
STARROCKS_PASSWORD=your_db_password
STARROCKS_DB=your_database_name
```

> Get API keys at: [serper.dev](https://serper.dev) | [platform.openai.com](https://platform.openai.com) | [twilio.com](https://twilio.com)

---

## Running the Program

```bash
source .venv/bin/activate
python main.py
```

The monitor runs every 5 minutes automatically.

---

## Testing Without Live Market Data

The code includes a mock mode in `tools.py` that simulates a 2.94% BTC/EUR price move and prints the WhatsApp alert to the console instead of sending it.

To enable mock mode, ensure the `# --- MOCK MODE ---` blocks in `tools.py` are uncommented (they are on by default).

To switch to production, delete the mock blocks in `tools.py`.

---

## Running as a Background Service (optional)

To keep the monitor running after you disconnect from the VM:

```bash
sudo nano /etc/systemd/system/market-monitor.service
```

Paste the following (update paths if needed):

```ini
[Unit]
Description=Market News Monitor

[Service]
WorkingDirectory=/home/azureuser/market-news-monitor
ExecStart=/home/azureuser/market-news-monitor/.venv/bin/python main.py
EnvironmentFile=/home/azureuser/market-news-monitor/.env
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now market-monitor
sudo journalctl -fu market-monitor   # view live logs
```
