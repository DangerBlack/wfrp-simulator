# wfrp-simulator
A python tools for simulating a battle in the wfrp II edition world

###install
sudo apt-get install python-yaml
pip3 install Pillow
pip3 install pyyaml

###usage
Put in **fighters** folder all the *.yaml* files edited as following
each file represent a single fighter.
```yaml
#name
name: 'Wolf'
#WS BS S T AG Int WP FEL
primary: [30,0,30,30,40,14,25,0]
#A W SB TB M Mag  IP  FP
secondary: [1,10,3,3,6,0,0,0]
#name kind function reloadTime
#name: the name of the weapon
#kind: sword (hand weapon) or bow (distance weapon)
#function: a string that represent the function
#reloadTime: how long I had to wait till next hit
weapon:  ['claws','sword','sword',0]
#armor strenght
armor: 0
#faction
faction: 'A'
skill: []
```

in the skill fields you can add some quality as following

```yaml
skill: 
- 'isSharpshooter()'
- 'maxNumberOfFend(1)'
- 'canDodge()'
```

remove from *config.yaml* all the text if you want the tools in english,
for italian user only keep the file as it is.

for running the tools call

```bash
python3 wfrp.py
```
