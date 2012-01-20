BEGIN { i = 0 }
{
        do {
                sort[i] = sort[i] $0 "\n";
                getline;
        } while ($0 != "");
        sort[i] = sort[i] $0;
        i += 1;
}
END {
        for (x = i - 1; x > -1; x--) {
               print sort[x];
        }
}
