s,(https?://|mailto:)[^ ]+,<a href='&'>&</a>,g
s,^\.\[([0-9]+)\] (.*)$,<sup id='\1'>\1</sup> \2,
s,\[([0-9]+)\],<a href='#\1'><sup>\1</sup></a>,g
