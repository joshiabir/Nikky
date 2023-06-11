cd mv ./nikky.service /etc/systemd/system/
mv ./*.py /usr/local/lib/
pip3 install -r requirements.txt
sudo systemctl daemon-reload
sudo systemctl start nikky.service
sudo systemctl enable nikky.service
