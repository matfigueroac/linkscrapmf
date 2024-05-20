# install_chromedriver.sh
#!/bin/sh
set -e

# Descargar e instalar ChromeDriver
if [ ! -f /usr/local/bin/chromedriver ]; then
  wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
  unzip /tmp/chromedriver.zip -d /usr/local/bin/
  rm /tmp/chromedriver.zip
fi

# Asegurarse de que ChromeDriver sea ejecutable
chmod +x /usr/local/bin/chromedriver

# Exportar la ruta de ChromeDriver como una variable de entorno
export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
