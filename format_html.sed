s,(https?://|mailto:)[^ ]+,<a href='&'>&</a>,g
s,^\.\[([0-9]+)\] (.*)$,<sup id='\1'>\1</sup> \2,
s,\[([0-9]+)\],<sup><a href='#\1'>\1</a></sup>,g
s,\[\[([0-9]+)\]\],[\1],g
