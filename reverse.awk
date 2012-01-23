BEGIN {
        RS=""
        FS="\n\f\n"
}
END {
        for (i = NF; i > 0; i--) {
                print $(i) "\n\f"
        }
}
