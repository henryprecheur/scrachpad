BEGIN { i = 0 }
{
        while ($0 != "\f") {
                sort[i] = sort[i] $0 "\n";
                getline;
        }
        i += 1;
}
END {
        for (x = i - 1; x > -1; x--) {
               print sort[x] "\f";
        }
}
