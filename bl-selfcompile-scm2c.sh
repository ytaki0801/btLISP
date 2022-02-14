SRC="bl-comp.scm"
BOOT="chibi-scheme -m chibi"
VM="./blSECD"; VMSRC="blSECD.c"
BIN="bl-comp.blSECD_scm2c"
S0="out-0"
S1="out-1"
S2="out-2"

if [ ! -e "$VM" ]; then cc -o "$VM" "$VMSRC"; fi && \
eval "$BOOT" "$SRC" < "$SRC" > "$S0" && \
eval "$VM" "$S0" < "$SRC" > "$S1" && \
eval "$VM" "$S1" < "$SRC" > "$S2" && \
diff -u "$S0" "$S1" && diff -u "$S1" "$S2" && diff -u "$S2" "$S0" && \
cp -p "$S2" "$BIN" && rm "$S0" "$S1" "$S2"

