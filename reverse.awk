BEGIN { RS="\f\n"; i = 0 }
{
        sort[++i] = $0
}
END {
        for (x = i; x > 0; x--) {
               print sort[x] "\f";
        }
}
