
## Install JDK

```
sudo apt update
sudo apt install -y unzip xvfb libxi6 libgconf-2-4 
sudo apt install default-jdk 
```

## Install Google Chrome

```
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
sudo apt -y update 
sudo apt -y install google-chrome-stable 
```

## Check version with `google-chrome --version` and download corresponding version for `chromedriver`

```
wget https://chromedriver.storage.googleapis.com/97.0.4692.71/chromedriver_linux64.zip
unzip chromedriver_linux64.zip 
sudo mv chromedriver /usr/bin/chromedriver 
sudo chown root:root /usr/bin/chromedriver 
sudo chmod +x /usr/bin/chromedriver 
```

## Dow

```json
{
    "url": "https://abnamro.nl",
    "device": "iPhone"
}

```