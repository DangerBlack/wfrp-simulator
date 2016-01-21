# wfrp-simulator
A python tools for simulating a battle in the wfrp II edition world

![preview](https://raw.githubusercontent.com/DangerBlack/wfrp-simulator/master/doc/preview.png)


###install

```bash
sudo apt-get install python3-pyqt4
sudo apt-get install python-yaml
pip3 install pyyaml
```

###usage

Add using the add button the fighter form the *Database* to the *Active Fighters* section.
Edit them simply clicking on them and pressing the *Update* button.
When you are ready click on *Run Simulation* and wait till something appear in the output section.

In the section after she sharpshooter box option you can add some magic in the form

```yaml
["SPELL NAME","kind of spell","function name",action_time]
```

remove from *config.yaml* all the text if you want the tools in english,
for italian user only keep the file as it is.

for running the tools call

```bash
python3 gui.py
```

If you want to run without the guy add the call to main function and run with

```bash
python3 wfrp.py
```
