import DiscordNations as n

#examples
nation1 = n.Nation("USB",5,"Seb",5)
nation1.addRepresentative("tom")
nation1.addRepresentative("shaun")
nation1.removeRepresentative("tom")
nation1.addRepresentative("benny")
if len(nations)<1:
    nations = n.readRecovery("Nation:The United States of America,1000,Joe Bidome, 5|Nation:Germany,500,Merkel,2");
nations.append(nation1)
print(n.printRecovery(nations))